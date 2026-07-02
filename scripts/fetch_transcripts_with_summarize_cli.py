#!/usr/bin/env python3
"""Fetch missing transcript/extract text through the optional summarize.sh CLI.

This is a fallback extractor for videos where the direct YouTube caption
pipeline fails or gets rate-limited. It requires the external `summarize`
command to be installed separately, but keeps that dependency optional for the
rest of the project.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import time
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAYLIST_PATH = ROOT / "data" / "playlist.json"
RAW_DIR = ROOT / "transcripts" / "raw"
CLEAN_DIR = ROOT / "transcripts" / "clean"
MANIFEST_PATH = ROOT / "transcripts" / "transcript_manifest.json"


@dataclass
class TranscriptRecord:
    index: int
    video_id: str
    title: str
    status: str
    track_name: str = ""
    language_code: str = ""
    is_auto_generated: bool = False
    word_count: int = 0
    raw_path: str = ""
    clean_path: str = ""
    error: str = ""


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def clean_extracted_text(text: str) -> str:
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def existing_records() -> dict[str, TranscriptRecord]:
    if not MANIFEST_PATH.exists():
        return {}
    manifest = load_json(MANIFEST_PATH)
    return {
        record["video_id"]: TranscriptRecord(**record)
        for record in manifest.get("records", [])
        if record.get("video_id")
    }


def select_videos(playlist: dict, records_by_id: dict[str, TranscriptRecord], args: argparse.Namespace) -> list[dict]:
    selected: list[dict] = []
    for video in playlist["videos"]:
        if video["index"] < args.start_index:
            continue
        existing = records_by_id.get(video["video_id"])
        if args.only_missing and existing and existing.status == "ok":
            continue
        selected.append(video)
        if args.limit and len(selected) >= args.limit:
            break
    return selected


def run_summarize(video: dict, args: argparse.Namespace) -> TranscriptRecord:
    url = video["url"]
    command = [
        args.command,
        url,
        "--extract",
        "--format",
        args.format,
    ]
    if args.language:
        command.extend(["--language", args.language])

    record = TranscriptRecord(
        index=video["index"],
        video_id=video["video_id"],
        title=video["title"],
        status="started",
        track_name="summarize.sh extract",
        language_code=args.language,
    )

    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            timeout=args.timeout,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError) as exc:
        record.status = "error"
        record.error = str(exc)
        return record

    clean_text = clean_extracted_text(result.stdout)
    count = word_count(clean_text)
    if count < args.min_words:
        record.status = "too_short"
        record.error = f"extracted text had only {count} words"
        return record

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    stem = f"{video['index']:03d}-{video['video_id']}"
    raw_path = RAW_DIR / f"{stem}.summarize.{args.format}"
    clean_path = CLEAN_DIR / f"{stem}.txt"
    raw_path.write_text(result.stdout, encoding="utf-8")
    clean_path.write_text(clean_text, encoding="utf-8")

    record.status = "ok"
    record.word_count = count
    record.raw_path = str(raw_path.relative_to(ROOT))
    record.clean_path = str(clean_path.relative_to(ROOT))
    return record


def write_manifest(playlist: dict, records_by_id: dict[str, TranscriptRecord]) -> None:
    records = [
        records_by_id.get(video["video_id"])
        or TranscriptRecord(
            index=video["index"],
            video_id=video["video_id"],
            title=video["title"],
            status="not_checked",
        )
        for video in playlist["videos"]
    ]
    payload = {
        "playlist_id": playlist["playlist_id"],
        "video_count_checked": sum(1 for record in records if record.status != "not_checked"),
        "caption_count": sum(1 for record in records if record.status == "ok"),
        "records": [asdict(record) for record in records],
    }
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", default="summarize", help="summarize.sh CLI command path")
    parser.add_argument("--limit", type=int, default=0, help="Fetch only N selected videos")
    parser.add_argument("--start-index", type=int, default=1)
    parser.add_argument("--only-missing", action="store_true", help="Skip existing ok transcript records")
    parser.add_argument("--format", default="md", choices=["md", "text", "json"])
    parser.add_argument("--language", default="", help="Optional summarize.sh language hint")
    parser.add_argument("--min-words", type=int, default=100)
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--sleep", type=float, default=1.0)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    playlist = load_json(PLAYLIST_PATH)
    records_by_id = existing_records()
    selected = select_videos(playlist, records_by_id, args)
    if not selected:
        print("No videos selected.")
        return 0

    command_path = shutil.which(args.command)
    if not command_path and not args.dry_run:
        print(
            "summarize CLI not found. Install it with: npm i -g @steipete/summarize",
        )
        return 2

    for video in selected:
        if args.dry_run:
            print(f"{video['index']:03d} would_fetch {video['url']} {video['title']}")
            continue
        record = run_summarize(video, args)
        records_by_id[record.video_id] = record
        print(f"{record.index:03d} {record.video_id} {record.status} words={record.word_count}")
        if args.sleep:
            time.sleep(args.sleep)

    if not args.dry_run:
        write_manifest(playlist, records_by_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Fetch available YouTube caption tracks for playlist videos.

This script stores full caption text locally under transcripts/raw and
transcripts/clean. Those directories are intentionally ignored by git.
Only the manifest is meant to be committed.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
from urllib.request import Request, urlopen

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:  # pragma: no cover - fallback path for base Python.
    YouTubeTranscriptApi = None


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


def request_text(url: str) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urlopen(request, timeout=45) as response:
        return response.read().decode("utf-8", errors="replace")


def extract_player_response(watch_html: str) -> dict:
    match = re.search(r"ytInitialPlayerResponse\s*=\s*(\{.*?\});", watch_html)
    if not match:
        raise RuntimeError("ytInitialPlayerResponse not found")
    return json.loads(match.group(1))


def choose_track(tracks: list[dict]) -> dict | None:
    if not tracks:
        return None

    def score(track: dict) -> tuple[int, int, int]:
        language = track.get("languageCode", "")
        name = track.get("name", {}).get("simpleText", "")
        is_asr = track.get("kind") == "asr" or "auto-generated" in name.lower()
        return (
            1 if language.startswith("en") else 0,
            0 if is_asr else 1,
            1 if track.get("baseUrl") else 0,
        )

    return sorted(tracks, key=score, reverse=True)[0]


def with_format(base_url: str, fmt: str) -> str:
    parsed = urlparse(base_url)
    query = parse_qs(parsed.query)
    query["fmt"] = [fmt]
    return urlunparse(parsed._replace(query=urlencode(query, doseq=True)))


def text_from_json3(payload: dict) -> str:
    lines: list[str] = []
    for event in payload.get("events", []):
        parts: list[str] = []
        for segment in event.get("segs", []):
            text = segment.get("utf8", "")
            if text:
                parts.append(text)
        line = "".join(parts).strip()
        if line:
            lines.append(line)
    return "\n".join(lines)


def clean_caption_text(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def fetch_caption(video: dict) -> TranscriptRecord:
    record = TranscriptRecord(
        index=video["index"],
        video_id=video["video_id"],
        title=video["title"],
        status="missing",
    )
    if YouTubeTranscriptApi is not None:
        try:
            return fetch_caption_with_package(video)
        except Exception as exc:  # noqa: BLE001 - fallback to watch page parser.
            record.error = f"youtube-transcript-api failed: {exc}"

    watch_url = f"https://www.youtube.com/watch?v={video['video_id']}"
    try:
        watch_html = request_text(watch_url)
        player = extract_player_response(watch_html)
        renderer = player.get("captions", {}).get("playerCaptionsTracklistRenderer", {})
        track = choose_track(renderer.get("captionTracks", []))
        if not track:
            record.status = "no_caption_track"
            return record

        track_name = track.get("name", {}).get("simpleText", "")
        record.track_name = track_name
        record.language_code = track.get("languageCode", "")
        record.is_auto_generated = track.get("kind") == "asr" or "auto-generated" in track_name.lower()

        raw_text = request_text(with_format(track["baseUrl"], "json3"))
        raw_payload = json.loads(raw_text)
        clean_text = clean_caption_text(text_from_json3(raw_payload))
        if not clean_text.strip():
            record.status = "empty_caption"
            return record

        RAW_DIR.mkdir(parents=True, exist_ok=True)
        CLEAN_DIR.mkdir(parents=True, exist_ok=True)
        stem = f"{video['index']:03d}-{video['video_id']}"
        raw_path = RAW_DIR / f"{stem}.json"
        clean_path = CLEAN_DIR / f"{stem}.txt"
        raw_path.write_text(json.dumps(raw_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        clean_path.write_text(clean_text, encoding="utf-8")

        record.status = "ok"
        record.word_count = len(re.findall(r"\b[\w'-]+\b", clean_text))
        record.raw_path = str(raw_path.relative_to(ROOT))
        record.clean_path = str(clean_path.relative_to(ROOT))
        return record
    except Exception as exc:  # noqa: BLE001 - manifest should capture per-video failures.
        record.status = "error"
        record.error = str(exc)
        return record


def fetch_caption_with_package(video: dict) -> TranscriptRecord:
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video["video_id"], languages=["en"])
    snippets = [
        {
            "text": snippet.text,
            "start": snippet.start,
            "duration": snippet.duration,
        }
        for snippet in transcript
    ]
    clean_text = clean_caption_text("\n".join(snippet["text"] for snippet in snippets))
    if not clean_text.strip():
        return TranscriptRecord(
            index=video["index"],
            video_id=video["video_id"],
            title=video["title"],
            status="empty_caption",
        )

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    stem = f"{video['index']:03d}-{video['video_id']}"
    raw_path = RAW_DIR / f"{stem}.json"
    clean_path = CLEAN_DIR / f"{stem}.txt"
    raw_payload = {
        "video_id": transcript.video_id,
        "language_code": transcript.language_code,
        "language": transcript.language,
        "is_generated": transcript.is_generated,
        "snippets": snippets,
    }
    raw_path.write_text(json.dumps(raw_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    clean_path.write_text(clean_text, encoding="utf-8")

    return TranscriptRecord(
        index=video["index"],
        video_id=video["video_id"],
        title=video["title"],
        status="ok",
        track_name=transcript.language,
        language_code=transcript.language_code,
        is_auto_generated=transcript.is_generated,
        word_count=len(re.findall(r"\b[\w'-]+\b", clean_text)),
        raw_path=str(raw_path.relative_to(ROOT)),
        clean_path=str(clean_path.relative_to(ROOT)),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="Fetch only the first N videos")
    parser.add_argument("--start-index", type=int, default=1, help="Start at this 1-based playlist index")
    parser.add_argument("--only-missing", action="store_true", help="Keep existing ok records and retry only missing")
    parser.add_argument("--sleep", type=float, default=0.2, help="Seconds to sleep between videos")
    args = parser.parse_args()

    playlist = json.loads(PLAYLIST_PATH.read_text(encoding="utf-8"))
    videos = [video for video in playlist["videos"] if video["index"] >= args.start_index]
    videos = videos[: args.limit or None]

    existing_by_id: dict[str, dict] = {}
    if args.only_missing and MANIFEST_PATH.exists():
        existing = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        existing_by_id = {record["video_id"]: record for record in existing.get("records", [])}

    records_by_id: dict[str, TranscriptRecord] = {}
    for record in existing_by_id.values():
        records_by_id[record["video_id"]] = TranscriptRecord(**record)

    for video in videos:
        existing = existing_by_id.get(video["video_id"])
        if args.only_missing and existing and existing.get("status") == "ok":
            print(f"{video['index']:03d} {video['video_id']} skip_existing words={existing.get('word_count', 0)}")
            continue
        record = fetch_caption(video)
        records_by_id[record.video_id] = record
        print(f"{record.index:03d} {record.video_id} {record.status} words={record.word_count}")
        if args.sleep:
            time.sleep(args.sleep)

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
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
    MANIFEST_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"caption_count={payload['caption_count']} checked={payload['video_count_checked']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

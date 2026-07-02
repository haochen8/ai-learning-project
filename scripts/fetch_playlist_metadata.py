#!/usr/bin/env python3
"""Fetch public YouTube playlist metadata into local study files."""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen


PLAYLIST_ID = "PLcfpQ4tk2k0V1LNigteMgExP1rb4Hy8wn"
PLAYLIST_URL = f"https://www.youtube.com/playlist?list={PLAYLIST_ID}"
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


@dataclass
class Video:
    index: int
    video_id: str
    title: str
    duration: str
    duration_seconds: int
    url: str


def parse_duration(value: str) -> int:
    parts = [int(part) for part in value.split(":")]
    if len(parts) == 2:
        minutes, seconds = parts
        return minutes * 60 + seconds
    if len(parts) == 3:
        hours, minutes, seconds = parts
        return hours * 3600 + minutes * 60 + seconds
    return 0


def format_hms(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours}:{minutes:02d}:{secs:02d}"


def fetch_html(url: str) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0.0.0 Safari/537.36"
            )
        },
    )
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def extract_initial_data(html: str) -> dict:
    match = re.search(r"var ytInitialData = (\{.*?\});</script>", html)
    if not match:
        raise RuntimeError("Could not find ytInitialData in YouTube response")
    return json.loads(match.group(1))


def get_contents(data: dict) -> list[dict]:
    try:
        return data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][0][
            "tabRenderer"
        ]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"][
            "contents"
        ]
    except KeyError as exc:
        raise RuntimeError("Could not find playlist contents in YouTube response") from exc


def extract_duration(lockup: dict) -> str:
    thumbnail = lockup.get("contentImage", {}).get("thumbnailViewModel", {})
    for overlay in thumbnail.get("overlays", []):
        badges = overlay.get("thumbnailBottomOverlayViewModel", {}).get("badges", [])
        for badge in badges:
            text = badge.get("thumbnailBadgeViewModel", {}).get("text", "")
            if re.match(r"^\d+:\d", text):
                return text
    return ""


def extract_videos(data: dict) -> list[Video]:
    videos: list[Video] = []
    for item in get_contents(data):
        lockup = item.get("lockupViewModel")
        if not lockup:
            continue

        metadata = lockup.get("metadata", {}).get("lockupMetadataViewModel", {})
        title = metadata.get("title", {}).get("content", "").strip()
        video_id = lockup.get("contentId", "").strip()
        duration = extract_duration(lockup)
        if not title or not video_id:
            continue

        videos.append(
            Video(
                index=len(videos) + 1,
                video_id=video_id,
                title=title,
                duration=duration,
                duration_seconds=parse_duration(duration) if duration else 0,
                url=f"https://www.youtube.com/watch?v={video_id}&list={PLAYLIST_ID}",
            )
        )
    return videos


def write_json(videos: list[Video], total_seconds: int) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "playlist_id": PLAYLIST_ID,
        "playlist_url": PLAYLIST_URL,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "video_count": len(videos),
        "total_seconds": total_seconds,
        "total_duration": format_hms(total_seconds),
        "videos": [asdict(video) for video in videos],
    }
    (DATA_DIR / "playlist.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_inventory(videos: list[Video], total_seconds: int) -> None:
    lines = [
        "# Playlist Inventory",
        "",
        f"Playlist: {PLAYLIST_URL}",
        f"Videos: {len(videos)}",
        f"Total duration: {format_hms(total_seconds)}",
        "",
        "| # | Duration | Title | Video ID |",
        "|---:|---:|---|---|",
    ]
    for video in videos:
        safe_title = video.title.replace("|", "\\|")
        lines.append(
            f"| {video.index} | {video.duration} | [{safe_title}]({video.url}) | `{video.video_id}` |"
        )
    lines.append("")
    (DATA_DIR / "playlist_inventory.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    html = fetch_html(PLAYLIST_URL)
    data = extract_initial_data(html)
    videos = extract_videos(data)
    if not videos:
        print("No videos found", file=sys.stderr)
        return 1

    total_seconds = sum(video.duration_seconds for video in videos)
    write_json(videos, total_seconds)
    write_inventory(videos, total_seconds)
    print(f"Fetched {len(videos)} videos, total duration {format_hms(total_seconds)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

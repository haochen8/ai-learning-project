#!/usr/bin/env python3
"""Create first-pass playlist analysis from fetched metadata."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "playlist.json"
ANALYSIS_PATH = ROOT / "data" / "playlist_analysis.md"
WATCH_ORDER_PATH = ROOT / "study-plan" / "watch_order.md"


THEMES = [
    (
        "Agents and agent architecture",
        ["agent", "agents", "agentic", "autonomous", "multi-agent", "recursive"],
    ),
    (
        "Evaluation and reliability",
        ["eval", "harness", "failed", "reproducing", "deterministic", "prod", "production"],
    ),
    (
        "Retrieval, memory, and context",
        ["retrieval", "memory", "context", "rag", "cache", "index", "tokens"],
    ),
    (
        "Developer workflow and coding",
        ["coding", "code", "development", "typescript", "workflow", "spec-driven"],
    ),
    (
        "Research automation",
        ["research", "autoresearch", "novel research", "frontier ml"],
    ),
    (
        "Product and organization",
        ["org", "product", "systems", "approval", "discernment", "room"],
    ),
]


def hms(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours}:{minutes:02d}:{secs:02d}"


def theme_for(title: str) -> str:
    lower_title = title.lower()
    for theme, keywords in THEMES:
        if any(keyword in lower_title for keyword in keywords):
            return theme
    return "Other"


def effort_for(seconds: int) -> str:
    if seconds >= 3600:
        return "Deep dive / chunk"
    if seconds >= 1800:
        return "Deep watch"
    if seconds <= 600:
        return "Skim or quick win"
    return "Watch"


def main() -> int:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    videos = data["videos"]

    longest = sorted(videos, key=lambda video: video["duration_seconds"], reverse=True)
    themed: dict[str, list[dict]] = {}
    for video in videos:
        themed.setdefault(theme_for(video["title"]), []).append(video)

    analysis_lines = [
        "# Playlist Analysis",
        "",
        f"Videos: {data['video_count']}",
        f"Total duration: {data['total_duration']}",
        "",
        "## Duration Buckets",
        "",
    ]

    buckets = [
        ("0-10 minutes", lambda seconds: seconds < 600),
        ("10-20 minutes", lambda seconds: 600 <= seconds < 1200),
        ("20-30 minutes", lambda seconds: 1200 <= seconds < 1800),
        ("30-60 minutes", lambda seconds: 1800 <= seconds < 3600),
        ("60+ minutes", lambda seconds: seconds >= 3600),
    ]
    for label, predicate in buckets:
        count = sum(1 for video in videos if predicate(video["duration_seconds"]))
        total = sum(video["duration_seconds"] for video in videos if predicate(video["duration_seconds"]))
        analysis_lines.append(f"- {label}: {count} videos, {hms(total)}")

    analysis_lines.extend(
        [
            "",
            "## Long Videos To Chunk",
            "",
            "| # | Duration | Title |",
            "|---:|---:|---|",
        ]
    )
    for video in longest:
        if video["duration_seconds"] < 1800:
            continue
        title = video["title"].replace("|", "\\|")
        analysis_lines.append(f"| {video['index']} | {video['duration']} | [{title}]({video['url']}) |")

    analysis_lines.extend(["", "## Theme Counts", ""])
    for theme in sorted(themed):
        total = sum(video["duration_seconds"] for video in themed[theme])
        analysis_lines.append(f"- {theme}: {len(themed[theme])} videos, {hms(total)}")

    analysis_lines.append("")
    ANALYSIS_PATH.write_text("\n".join(analysis_lines), encoding="utf-8")

    watch_lines = [
        "# Watch Order Draft",
        "",
        "Status: metadata-only draft. This should be revised after transcript analysis.",
        "",
        "## First Pass",
        "",
        "| Order | Effort | Duration | Theme | Title |",
        "|---:|---|---:|---|---|",
    ]
    ordered = sorted(
        videos,
        key=lambda video: (
            effort_for(video["duration_seconds"]) == "Deep dive / chunk",
            video["duration_seconds"],
        ),
    )
    for order, video in enumerate(ordered, start=1):
        title = video["title"].replace("|", "\\|")
        watch_lines.append(
            f"| {order} | {effort_for(video['duration_seconds'])} | {video['duration']} | "
            f"{theme_for(video['title'])} | [{title}]({video['url']}) |"
        )

    watch_lines.append("")
    WATCH_ORDER_PATH.write_text("\n".join(watch_lines), encoding="utf-8")
    print(f"Wrote {ANALYSIS_PATH.relative_to(ROOT)}")
    print(f"Wrote {WATCH_ORDER_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

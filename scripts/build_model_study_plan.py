#!/usr/bin/env python3
"""Build study-plan deliverables from local model-based notes."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAYLIST_PATH = ROOT / "data" / "playlist.json"
TRANSCRIPT_MANIFEST_PATH = ROOT / "transcripts" / "transcript_manifest.json"
SUMMARY_MANIFEST_PATH = ROOT / "data" / "local_summary_manifest.json"
STUDY_DIR = ROOT / "study-plan"


THEME_RULES = [
    (
        "Agent architecture and orchestration",
        [
            "agent",
            "agents",
            "agentic",
            "autonomous",
            "tool",
            "tools",
            "recursive",
            "liveness",
            "hallucinations",
        ],
    ),
    (
        "Production reliability and evals",
        [
            "eval",
            "evals",
            "production",
            "prod",
            "failed",
            "reproducing",
            "deception",
            "monitor",
            "review debt",
            "deterministic",
        ],
    ),
    (
        "Retrieval, memory, and context",
        [
            "retrieval",
            "memory",
            "context",
            "rag",
            "cache",
            "index",
            "tokens",
            "multimodal",
        ],
    ),
    (
        "Developer workflow and coding systems",
        [
            "coding",
            "code",
            "software",
            "workflow",
            "spec-driven",
            "mcp apps",
            "ci/cd",
            "idea velocity",
        ],
    ),
    (
        "Voice, browser, and multimodal UX",
        [
            "voice",
            "browser",
            "visual",
            "graphics",
            "frontier model",
        ],
    ),
    (
        "Product, domain, and organization",
        [
            "org",
            "product",
            "vertical",
            "compliance",
            "financial",
            "room",
            "launch",
        ],
    ),
]


MANUAL_THEMES = {
    1: "Agent architecture and orchestration",
    2: "Agent architecture and orchestration",
    3: "Production reliability and evals",
    4: "Production reliability and evals",
    5: "Developer workflow and coding systems",
    6: "Retrieval, memory, and context",
    7: "Agent architecture and orchestration",
    8: "Product, domain, and organization",
    9: "Production reliability and evals",
    10: "Product, domain, and organization",
    11: "Agent architecture and orchestration",
    12: "Agent architecture and orchestration",
    13: "Developer workflow and coding systems",
    14: "Production reliability and evals",
    15: "Retrieval, memory, and context",
    16: "Voice, browser, and multimodal UX",
    17: "Retrieval, memory, and context",
    18: "Voice, browser, and multimodal UX",
    19: "Retrieval, memory, and context",
    20: "Retrieval, memory, and context",
    21: "Production reliability and evals",
    22: "Retrieval, memory, and context",
    23: "Retrieval, memory, and context",
    24: "Product, domain, and organization",
    25: "Voice, browser, and multimodal UX",
    26: "Production reliability and evals",
    27: "Production reliability and evals",
    28: "Voice, browser, and multimodal UX",
    29: "Production reliability and evals",
    30: "Developer workflow and coding systems",
    31: "Developer workflow and coding systems",
    32: "Retrieval, memory, and context",
    33: "Voice, browser, and multimodal UX",
    35: "Product, domain, and organization",
    36: "Product, domain, and organization",
    37: "Production reliability and evals",
    38: "Production reliability and evals",
    39: "Agent architecture and orchestration",
    40: "Voice, browser, and multimodal UX",
    41: "Voice, browser, and multimodal UX",
    42: "Developer workflow and coding systems",
    43: "Production reliability and evals",
    44: "Developer workflow and coding systems",
    45: "Production reliability and evals",
    46: "Production reliability and evals",
    47: "Production reliability and evals",
    48: "Developer workflow and coding systems",
    49: "Production reliability and evals",
}


PRIORITY_TOPICS = [
    "Recursive Coding Agents",
    "The Log Is The Agent",
    "Production Evals For Agentic AI Systems",
    "Build Systems, Not Code",
    "The 100-Tool Agent Is a Trap",
    "AI System Design: From Idea to Production",
    "Deterministic Infra for Non-Deterministic AI Agents",
    "Stop Evaluating Models Like It's the 50s",
    "Enterprise Agents Have a Structure Problem",
    "Your Coding Agent Is Creating Review Debt",
    "Stop AI Agent Hallucinations: 5 Techniques + Production Patterns",
    "Every Solo Agent Builder Eventually Reinvents a Worse Version of CI/CD",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def title_topic(title: str) -> str:
    return re.split(r"\s+-\s+", title, maxsplit=1)[0].strip()


def theme_for(index: int, title: str) -> str:
    if index in MANUAL_THEMES:
        return MANUAL_THEMES[index]
    haystack = title.lower()
    scores: list[tuple[int, str]] = []
    for theme, keywords in THEME_RULES:
        scores.append((sum(1 for keyword in keywords if keyword in haystack), theme))
    score, theme = max(scores, key=lambda item: item[0])
    return theme if score else "General AI engineering"


def effort_for(seconds: int) -> str:
    if seconds <= 600:
        return "Quick skim"
    if seconds <= 1800:
        return "Standard watch"
    return "Deep watch"


def extract_section(text: str, heading: str) -> list[str]:
    pattern = rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        return []
    items: list[str] = []
    for line in match.group("body").splitlines():
        cleaned = line.strip()
        if cleaned.startswith("- "):
            cleaned = cleaned[2:].strip()
        elif re.match(r"^\d+\.\s+", cleaned):
            cleaned = re.sub(r"^\d+\.\s+", "", cleaned).strip()
        else:
            continue
        cleaned = re.sub(r"\*\*", "", cleaned).strip()
        if cleaned:
            items.append(cleaned)
    return items


def safe_link(path: str) -> str:
    return f"../{path}"


def source_label(transcript_record: dict, summary_record: dict) -> str:
    track = transcript_record.get("track_name", "")
    words = summary_record.get("transcript_words", 0)
    if "summarize.sh" in track:
        return f"fallback extract, {words} words"
    return f"YouTube transcript, {words} words"


def priority_for(video: dict, topic: str, summary_record: dict) -> int:
    words = summary_record.get("transcript_words", 0)
    if words < 500:
        return 3
    if topic in PRIORITY_TOPICS:
        return 1
    seconds = video.get("duration_seconds", 0)
    if seconds <= 900:
        return 2
    return 2


def build_items() -> tuple[list[dict], list[dict], list[dict]]:
    playlist = load_json(PLAYLIST_PATH)
    transcript_manifest = load_json(TRANSCRIPT_MANIFEST_PATH)
    summary_manifest = load_json(SUMMARY_MANIFEST_PATH)

    videos_by_index = {video["index"]: video for video in playlist["videos"]}
    transcripts_by_id = {record["video_id"]: record for record in transcript_manifest["records"]}
    summary_records = summary_manifest["records"]

    items: list[dict] = []
    skipped: list[dict] = []
    for record in summary_records:
        index = record["index"]
        video = videos_by_index.get(index)
        if not video:
            continue
        if record["status"] != "ok":
            skipped.append({"video": video, "record": record})
            continue
        note_path = ROOT / record["output_path"]
        if not note_path.exists():
            skipped.append({"video": video, "record": record})
            continue
        text = note_path.read_text(encoding="utf-8", errors="replace")
        topic = title_topic(video["title"])
        transcript = transcripts_by_id.get(video["video_id"], {})
        item = {
            "video": video,
            "record": record,
            "transcript": transcript,
            "topic": topic,
            "theme": theme_for(video["index"], video["title"]),
            "what_to_learn": extract_section(text, "What To Learn")[:5],
            "takeaways": extract_section(text, "Practical Takeaways")[:5],
            "questions": extract_section(text, "Review Questions")[:5],
            "concepts": extract_section(text, "Key Concepts")[:8],
            "note_path": record["output_path"],
            "priority": priority_for(video, topic, record),
        }
        items.append(item)

    missing = []
    ok_indexes = {item["video"]["index"] for item in items}
    skipped_indexes = {entry["video"]["index"] for entry in skipped}
    transcript_ok_ids = {
        record["video_id"]
        for record in transcript_manifest["records"]
        if record.get("status") == "ok" and record.get("clean_path")
    }
    for video in playlist["videos"]:
        if video["index"] in ok_indexes or video["index"] in skipped_indexes:
            continue
        if video["video_id"] not in transcript_ok_ids:
            missing.append({"video": video, "reason": "missing transcript"})
        else:
            missing.append({"video": video, "reason": "not summarized"})

    return sorted(items, key=lambda item: item["video"]["index"]), skipped, missing


def write_index(items: list[dict], skipped: list[dict], missing: list[dict]) -> None:
    lines = [
        "# Model-Based Study Index",
        "",
        "This index tracks the local open-source model notes in `summaries/model_based/`.",
        "",
        "## Coverage",
        "",
        f"- Model-based notes: {len(items)}",
        f"- Skipped model summaries: {len(skipped)}",
        f"- Playlist items still missing model notes: {len(missing)}",
        "- Large raw/clean transcript files are intentionally not tracked in git.",
        "",
        "## Notes",
        "",
        "| # | Priority | Theme | Source | Video | Notes |",
        "|---:|---:|---|---|---|---|",
    ]
    for item in items:
        video = item["video"]
        title = video["title"].replace("|", "\\|")
        note_path = item["note_path"]
        lines.append(
            f"| {video['index']} | P{item['priority']} | {item['theme']} | "
            f"{source_label(item['transcript'], item['record'])} | "
            f"[{title}]({video['url']}) | [{Path(note_path).name}]({safe_link(note_path)}) |"
        )

    lines.extend(["", "## Skipped Or Blocked", ""])
    if skipped:
        for entry in skipped:
            video = entry["video"]
            record = entry["record"]
            words = record.get("transcript_words", 0)
            lines.append(f"- {video['index']:03d}. {video['title']} - {record.get('status')} ({words} words)")
    else:
        lines.append("- None")

    lines.extend(["", "## Missing Transcript Queue", ""])
    for entry in missing[:40]:
        video = entry["video"]
        lines.append(f"- {video['index']:03d}. {video['title']} - {entry['reason']}")
    if len(missing) > 40:
        lines.append(f"- ... {len(missing) - 40} more")
    lines.append("")
    (STUDY_DIR / "model_based_index.md").write_text("\n".join(lines), encoding="utf-8")


def write_learning_path(items: list[dict]) -> None:
    by_theme: dict[str, list[dict]] = defaultdict(list)
    for item in items:
        by_theme[item["theme"]].append(item)

    theme_order = [
        "Agent architecture and orchestration",
        "Production reliability and evals",
        "Retrieval, memory, and context",
        "Developer workflow and coding systems",
        "Voice, browser, and multimodal UX",
        "Product, domain, and organization",
        "General AI engineering",
    ]

    lines = [
        "# Model-Based Learning Path",
        "",
        "This is the recommended route through the notes that have local model-based summaries.",
        "",
        "## How To Study Each Talk",
        "",
        "1. Read the note's Executive Summary and What To Learn sections.",
        "2. Watch only the transcript anchors first, then decide whether to watch the full video.",
        "3. Answer the Review Questions without looking back.",
        "4. Convert one Practical Takeaway into a tiny prototype, eval, or design note.",
        "",
        "## Priority Route",
        "",
    ]
    priority_items = sorted(items, key=lambda item: (item["priority"], item["video"]["index"]))
    for item in priority_items[:18]:
        video = item["video"]
        lines.append(
            f"- P{item['priority']} [{item['topic']}]({safe_link(item['note_path'])}) "
            f"({video['duration']}, {effort_for(video['duration_seconds'])})"
        )

    lines.extend(["", "## Modules", ""])
    module_number = 1
    for theme in theme_order:
        module_items = by_theme.get(theme, [])
        if not module_items:
            continue
        duration = sum(item["video"]["duration_seconds"] for item in module_items)
        lines.extend(
            [
                f"### Module {module_number}: {theme}",
                "",
                f"- Notes: {len(module_items)}",
                f"- Total watch time represented: {duration // 3600}:{duration % 3600 // 60:02d}:{duration % 60:02d}",
                "",
                "| # | Effort | Source | Talk | First learning target |",
                "|---:|---|---|---|---|",
            ]
        )
        for item in sorted(module_items, key=lambda entry: (entry["priority"], entry["video"]["duration_seconds"])):
            video = item["video"]
            first_target = item["what_to_learn"][0] if item["what_to_learn"] else "Review the note and transcript anchors."
            first_target = first_target.replace("|", "\\|")
            lines.append(
                f"| {video['index']} | {effort_for(video['duration_seconds'])} | "
                f"{source_label(item['transcript'], item['record'])} | "
                f"[{item['topic']}]({safe_link(item['note_path'])}) | {first_target} |"
            )
        lines.append("")
        module_number += 1

    lines.extend(
        [
            "## Four-Week Study Plan",
            "",
            "### Week 1: Agent foundations",
            "",
            "- Focus: logs, recursive coding agents, tool boundaries, deterministic orchestration.",
            "- Deliverable: a one-page architecture note for a small agent workflow.",
            "",
            "### Week 2: Production reliability",
            "",
            "- Focus: evals, replay, review debt, hallucination controls, monitor design.",
            "- Deliverable: a tiny eval suite with at least five failure cases.",
            "",
            "### Week 3: Context and developer workflow",
            "",
            "- Focus: retrieval, memory, token reduction, spec-driven workflows, MCP apps.",
            "- Deliverable: a prototype plan that separates model calls from deterministic code.",
            "",
            "### Week 4: Synthesis",
            "",
            "- Focus: choose 6 deep-watch talks, revisit transcript anchors, and build a capstone.",
            "- Deliverable: one working or pseudo-working agentic workflow with logs and review gates.",
            "",
        ]
    )
    (STUDY_DIR / "model_based_learning_path.md").write_text("\n".join(lines), encoding="utf-8")


def write_review_schedule(items: list[dict]) -> None:
    priority_items = sorted(items, key=lambda item: (item["priority"], item["video"]["index"]))
    schedule: list[tuple[int, str, dict]] = []
    day = 1
    for item in priority_items:
        video = item["video"]
        schedule.append((day, "First pass", item))
        if item["priority"] == 1:
            schedule.append((day + 2, "Recall questions", item))
            schedule.append((day + 7, "Prototype or design note", item))
        elif video["duration_seconds"] <= 900:
            schedule.append((day + 3, "Quick recall", item))
        day += 1

    lines = [
        "# Review Schedule",
        "",
        "Use this as a spaced repetition plan for the local model-based notes.",
        "",
        "| Day | Task | Notes |",
        "|---:|---|---|",
    ]
    for day_number, task, item in sorted(schedule, key=lambda entry: (entry[0], entry[2]["priority"], entry[2]["video"]["index"])):
        lines.append(f"| {day_number} | {task} | [{item['topic']}]({safe_link(item['note_path'])}) |")

    lines.extend(
        [
            "",
            "## Daily Review Loop",
            "",
            "- Spend 10 minutes on recall before reading.",
            "- Spend 20-40 minutes on the note and selected video anchors.",
            "- Write one production risk and one measurable check.",
            "- Move only strong talks into full-watch sessions.",
            "",
        ]
    )
    (STUDY_DIR / "review_schedule.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    STUDY_DIR.mkdir(parents=True, exist_ok=True)
    items, skipped, missing = build_items()
    write_index(items, skipped, missing)
    write_learning_path(items)
    write_review_schedule(items)
    print(f"Wrote model-based study plan for {len(items)} notes")
    print(f"Skipped: {len(skipped)}")
    print(f"Missing: {len(missing)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

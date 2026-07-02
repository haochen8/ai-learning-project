#!/usr/bin/env python3
"""Build derived notes and study materials from playlist metadata and transcripts."""

from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAYLIST_PATH = ROOT / "data" / "playlist.json"
MANIFEST_PATH = ROOT / "transcripts" / "transcript_manifest.json"
SUMMARIES_DIR = ROOT / "summaries"
STUDY_DIR = ROOT / "study-plan"
TRANSCRIPT_COVERAGE_PATH = ROOT / "data" / "transcript_coverage.md"


THEMES = [
    (
        "Agent architecture",
        ["agent", "agents", "agentic", "autonomous", "multi-agent", "recursive", "tool calls"],
    ),
    (
        "Evaluation and production reliability",
        ["eval", "evals", "harness", "failed", "reproducing", "deterministic", "prod", "production"],
    ),
    (
        "Retrieval, memory, and context",
        ["retrieval", "memory", "context", "rag", "cache", "index", "tokens"],
    ),
    (
        "Developer workflow and coding systems",
        ["coding", "code", "development", "typescript", "workflow", "spec-driven", "software factories"],
    ),
    (
        "Research automation",
        ["research", "autoresearch", "frontier ml", "novel research"],
    ),
    (
        "Product, UX, and organization",
        ["org", "product", "systems", "approval", "discernment", "ux", "users"],
    ),
    (
        "Voice and multimodal AI",
        ["voice", "visual", "multimodal", "browser", "eyes"],
    ),
]


STOPWORDS = {
    "a",
    "about",
    "actually",
    "after",
    "again",
    "all",
    "also",
    "am",
    "an",
    "and",
    "any",
    "are",
    "as",
    "at",
    "be",
    "because",
    "been",
    "but",
    "by",
    "can",
    "could",
    "do",
    "does",
    "doing",
    "for",
    "from",
    "get",
    "go",
    "going",
    "had",
    "has",
    "have",
    "how",
    "i",
    "if",
    "in",
    "into",
    "is",
    "it",
    "it's",
    "its",
    "just",
    "kind",
    "know",
    "like",
    "little",
    "make",
    "more",
    "not",
    "now",
    "of",
    "on",
    "one",
    "or",
    "our",
    "out",
    "really",
    "right",
    "so",
    "some",
    "that",
    "the",
    "their",
    "them",
    "then",
    "there",
    "these",
    "they",
    "thing",
    "things",
    "think",
    "this",
    "to",
    "use",
    "very",
    "want",
    "was",
    "we",
    "what",
    "when",
    "where",
    "which",
    "with",
    "you",
    "your",
}


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value[:80] or "video"


def theme_for(title: str) -> str:
    lower = title.lower()
    for theme, keywords in THEMES:
        if any(keyword in lower for keyword in keywords):
            return theme
    return "General AI engineering"


def effort_for(seconds: int) -> str:
    if seconds >= 3600:
        return "Chunk into separate sessions"
    if seconds >= 1800:
        return "Deep watch"
    if seconds <= 600:
        return "Quick skim"
    return "Standard watch"


def tokens(text: str) -> list[str]:
    return [
        token.lower()
        for token in re.findall(r"[A-Za-z][A-Za-z0-9'-]{2,}", text)
        if token.lower() not in STOPWORDS
    ]


def key_terms(text: str, limit: int = 12) -> list[str]:
    words = tokens(text)
    unigram_counts = Counter(words)
    bigrams = [
        f"{left} {right}"
        for left, right in zip(words, words[1:])
        if left not in STOPWORDS and right not in STOPWORDS
    ]
    bigram_counts = Counter(bigrams)
    candidates = []
    for term, count in bigram_counts.most_common(limit * 2):
        if count >= 2:
            candidates.append((term, count * 1.8))
    for term, count in unigram_counts.most_common(limit * 3):
        candidates.append((term, count))

    selected: list[str] = []
    seen_parts: set[str] = set()
    for term, _score in sorted(candidates, key=lambda item: item[1], reverse=True):
        parts = set(term.split())
        if parts and len(parts & seen_parts) > 1:
            continue
        selected.append(term)
        seen_parts.update(parts)
        if len(selected) >= limit:
            break
    return selected


def title_topic(title: str) -> str:
    return re.split(r"\s+-\s+", title, maxsplit=1)[0].strip()


def objectives(theme: str, topic: str) -> list[str]:
    by_theme = {
        "Agent architecture": [
            f"Explain the design problem behind {topic}.",
            "Identify the agent boundaries, tools, feedback loops, and failure modes.",
            "Decide which parts should be deterministic software rather than model behavior.",
        ],
        "Evaluation and production reliability": [
            f"Describe how {topic} changes testing or production readiness.",
            "Separate offline evals, live monitoring, replay, and incident debugging.",
            "Define measurable pass/fail criteria for an agentic workflow.",
        ],
        "Retrieval, memory, and context": [
            f"Understand the context or retrieval bottleneck addressed by {topic}.",
            "Compare memory, cache, indexing, and retrieval strategies.",
            "Estimate the impact on latency, cost, and answer quality.",
        ],
        "Developer workflow and coding systems": [
            f"Map {topic} to a real engineering workflow.",
            "Identify where automation can safely replace manual steps.",
            "Define guardrails for code generation, review, and deployment.",
        ],
        "Research automation": [
            f"Understand the research workflow behind {topic}.",
            "Distinguish search, hypothesis generation, validation, and synthesis.",
            "Design a reproducible research-agent loop.",
        ],
        "Product, UX, and organization": [
            f"Translate {topic} into product or organizational design choices.",
            "Identify user trust, adoption, and feedback-loop risks.",
            "Define what a useful human-in-the-loop process would look like.",
        ],
        "Voice and multimodal AI": [
            f"Understand the modality-specific constraints behind {topic}.",
            "Identify latency, interruption, perception, and rendering challenges.",
            "Connect multimodal UX to production system design.",
        ],
    }
    return by_theme.get(
        theme,
        [
            f"Explain the main engineering idea behind {topic}.",
            "Identify assumptions, tradeoffs, and implementation risks.",
            "Turn the idea into one concrete experiment or prototype.",
        ],
    )


def practice_tasks(theme: str, terms: list[str]) -> list[str]:
    term_text = ", ".join(terms[:4]) if terms else "the talk's main concepts"
    return [
        f"Write a one-page design note applying {term_text} to a small AI feature.",
        "List three production risks and one observable metric for each risk.",
        "Create a minimal prototype or pseudocode loop that tests the talk's central claim.",
    ]


def review_questions(topic: str, theme: str, terms: list[str]) -> list[str]:
    main_term = terms[0] if terms else topic
    return [
        f"What problem is {topic} trying to solve?",
        f"Why does {main_term} matter in {theme.lower()}?",
        "What would fail first if this idea were moved into production?",
        "What evidence would convince you that the approach works?",
    ]


def flashcards_for(video: dict, theme: str, terms: list[str]) -> list[tuple[str, str]]:
    topic = title_topic(video["title"])
    cards = [
        (f"What is the main learning target for video {video['index']}?", topic),
        (f"Which module does video {video['index']} belong to?", theme),
    ]
    for term in terms[:3]:
        cards.append((f"Why is '{term}' important in this session?", f"It is a recurring transcript signal connected to {topic}."))
    return cards


def load_clean_text(record: dict) -> str:
    clean_path = record.get("clean_path")
    if not clean_path:
        return ""
    path = ROOT / clean_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_video_note(video: dict, record: dict) -> dict:
    title = video["title"]
    topic = title_topic(title)
    theme = theme_for(title)
    text = load_clean_text(record)
    terms = key_terms(text)
    status = record.get("status", "not_checked")
    note_path = SUMMARIES_DIR / f"{video['index']:03d}-{slugify(topic)}.md"

    lines = [
        f"# {title}",
        "",
        f"- Playlist index: {video['index']}",
        f"- Duration: {video['duration']}",
        f"- Theme: {theme}",
        f"- Effort: {effort_for(video['duration_seconds'])}",
        f"- Transcript status: {status}",
        f"- Transcript words: {record.get('word_count', 0)}",
        f"- Video: {video['url']}",
        "",
        "## Learning Objectives",
        "",
    ]
    lines.extend(f"- {item}" for item in objectives(theme, topic))
    lines.extend(["", "## Core Notes", ""])
    if status == "ok":
        term_text = ", ".join(terms[:8]) if terms else "No strong repeated terms found."
        lines.extend(
            [
                f"- This session is filed under **{theme}** and should be studied as **{effort_for(video['duration_seconds']).lower()}**.",
                f"- The transcript's strongest recurring signals are: {term_text}.",
                "- Treat these notes as a structured first pass. They should be refined with model-assisted summarization after an API key is available.",
            ]
        )
    else:
        lines.extend(
            [
                "- Transcript is not available yet in the local workspace.",
                "- Keep this video in the plan, but prioritize caption retry or audio transcription before final semantic summarization.",
            ]
        )

    lines.extend(["", "## Key Terms", ""])
    if terms:
        lines.extend(f"- {term}" for term in terms)
    else:
        lines.append("- Pending transcript or no stable terms extracted.")

    lines.extend(["", "## Practice", ""])
    lines.extend(f"- {item}" for item in practice_tasks(theme, terms))

    lines.extend(["", "## Review Questions", ""])
    lines.extend(f"- {item}" for item in review_questions(topic, theme, terms))
    lines.append("")

    note_path.write_text("\n".join(lines), encoding="utf-8")
    return {
        "video": video,
        "record": record,
        "theme": theme,
        "terms": terms,
        "note_path": note_path,
    }


def write_coverage(videos: list[dict], records: list[dict]) -> None:
    lines = [
        "# Transcript Coverage",
        "",
        "| # | Status | Words | Duration | Title |",
        "|---:|---|---:|---:|---|",
    ]
    total_words = 0
    ok_count = 0
    for video, record in zip(videos, records):
        words = int(record.get("word_count", 0) or 0)
        total_words += words
        ok_count += 1 if record.get("status") == "ok" else 0
        title = video["title"].replace("|", "\\|")
        lines.append(f"| {video['index']} | {record.get('status')} | {words} | {video['duration']} | [{title}]({video['url']}) |")
    lines.extend(["", f"Captured transcripts: {ok_count}/{len(videos)}", f"Captured words: {total_words}", ""])
    TRANSCRIPT_COVERAGE_PATH.write_text("\n".join(lines), encoding="utf-8")


def write_learning_path(note_infos: list[dict]) -> None:
    by_theme: dict[str, list[dict]] = defaultdict(list)
    for info in note_infos:
        by_theme[info["theme"]].append(info)

    lines = [
        "# Learning Path",
        "",
        "Status: first complete study-plan draft from playlist metadata and available transcripts.",
        "",
        "## How To Use This Plan",
        "",
        "- Start with quick-skim videos to build vocabulary.",
        "- Move into deep-watch modules once the repeated terms are familiar.",
        "- Use each video's practice task before continuing to the next module.",
        "- Re-run transcript retries later for videos marked as missing or throttled.",
        "",
        "## Module Order",
        "",
    ]

    theme_order = [
        "Agent architecture",
        "Evaluation and production reliability",
        "Retrieval, memory, and context",
        "Developer workflow and coding systems",
        "Voice and multimodal AI",
        "Product, UX, and organization",
        "Research automation",
        "General AI engineering",
    ]
    for module_number, theme in enumerate(theme_order, start=1):
        items = by_theme.get(theme, [])
        if not items:
            continue
        duration = sum(item["video"]["duration_seconds"] for item in items)
        captured = sum(1 for item in items if item["record"].get("status") == "ok")
        lines.extend(
            [
                f"### Module {module_number}: {theme}",
                "",
                f"- Videos: {len(items)}",
                f"- Captured transcripts: {captured}/{len(items)}",
                f"- Total duration: {duration // 3600}:{duration % 3600 // 60:02d}:{duration % 60:02d}",
                "",
                "| # | Duration | Effort | Transcript | Video | Notes |",
                "|---:|---:|---|---|---|---|",
            ]
        )
        sorted_items = sorted(items, key=lambda item: (item["video"]["duration_seconds"] >= 3600, item["video"]["duration_seconds"]))
        for item in sorted_items:
            video = item["video"]
            note_rel = item["note_path"].relative_to(ROOT)
            title = video["title"].replace("|", "\\|")
            lines.append(
                f"| {video['index']} | {video['duration']} | {effort_for(video['duration_seconds'])} | "
                f"{item['record'].get('status')} | [{title}]({video['url']}) | [{note_rel.as_posix()}](../{note_rel.as_posix()}) |"
            )
        lines.append("")

    lines.extend(
        [
            "## Two-Week Route",
            "",
            "- Days 1-2: Quick skim all videos under 10 minutes and capture vocabulary.",
            "- Days 3-5: Agent architecture module.",
            "- Days 6-8: Evaluation and production reliability module.",
            "- Days 9-10: Retrieval, memory, and context module.",
            "- Days 11-12: Developer workflow and coding systems module.",
            "- Days 13-14: Product/UX, voice/multimodal, and research automation modules.",
            "",
            "## Four-Week Route",
            "",
            "- Week 1: Agent architecture fundamentals and quick skims.",
            "- Week 2: Production reliability, evals, and harness design.",
            "- Week 3: Retrieval, memory, context, and coding workflows.",
            "- Week 4: Long keynotes, project exercises, and final synthesis.",
            "",
        ]
    )
    (STUDY_DIR / "learning_path.md").write_text("\n".join(lines), encoding="utf-8")


def write_topic_map(note_infos: list[dict]) -> None:
    by_theme: dict[str, list[dict]] = defaultdict(list)
    global_terms: Counter[str] = Counter()
    for info in note_infos:
        by_theme[info["theme"]].append(info)
        global_terms.update(info["terms"][:8])

    lines = ["# Topic Map", "", "## Global Term Signals", ""]
    for term, count in global_terms.most_common(30):
        lines.append(f"- {term}: {count}")
    lines.extend(["", "## Themes", ""])
    for theme in sorted(by_theme):
        lines.append(f"### {theme}")
        lines.append("")
        theme_terms: Counter[str] = Counter()
        for info in by_theme[theme]:
            theme_terms.update(info["terms"][:8])
        if theme_terms:
            lines.append("Key recurring terms: " + ", ".join(term for term, _count in theme_terms.most_common(12)))
        else:
            lines.append("Key recurring terms: pending transcripts.")
        lines.append("")
        for info in sorted(by_theme[theme], key=lambda item: item["video"]["index"]):
            video = info["video"]
            lines.append(f"- {video['index']:02d}. {title_topic(video['title'])}")
        lines.append("")
    (STUDY_DIR / "topic_map.md").write_text("\n".join(lines), encoding="utf-8")


def write_flashcards(note_infos: list[dict]) -> None:
    lines = ["# Flashcards", "", "Format: question | answer", ""]
    for info in note_infos:
        for question, answer in flashcards_for(info["video"], info["theme"], info["terms"]):
            lines.append(f"- **Q:** {question}")
            lines.append(f"  **A:** {answer}")
    lines.append("")
    (STUDY_DIR / "flashcards.md").write_text("\n".join(lines), encoding="utf-8")


def write_exercises(note_infos: list[dict]) -> None:
    lines = ["# Exercises", "", "## Module Projects", ""]
    themes = sorted({info["theme"] for info in note_infos})
    for theme in themes:
        lines.append(f"### {theme}")
        lines.append("")
        lines.append("- Design a minimal system that demonstrates one core idea from this module.")
        lines.append("- Define inputs, outputs, success metrics, failure modes, and human review points.")
        lines.append("- Run a paper eval: write five test cases and expected behavior before building.")
        lines.append("")

    lines.extend(["## Capstone", ""])
    lines.append("Build a small agentic workflow with logging, replay, eval criteria, retrieval or memory, and a human-visible output layer.")
    lines.append("")
    lines.append("Deliverables:")
    lines.append("- system diagram")
    lines.append("- prompt/tool contract")
    lines.append("- eval set")
    lines.append("- failure-mode log")
    lines.append("- one-page reflection on what should remain deterministic")
    lines.append("")
    (STUDY_DIR / "exercises.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    playlist = json.loads(PLAYLIST_PATH.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    videos = playlist["videos"]
    records_by_id = {record["video_id"]: record for record in manifest["records"]}
    records = [records_by_id.get(video["video_id"], {"status": "not_checked", "word_count": 0}) for video in videos]

    SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)
    STUDY_DIR.mkdir(parents=True, exist_ok=True)
    write_coverage(videos, records)

    note_infos = []
    for video, record in zip(videos, records):
        note_infos.append(write_video_note(video, record))

    write_learning_path(note_infos)
    write_topic_map(note_infos)
    write_flashcards(note_infos)
    write_exercises(note_infos)
    print(f"Wrote {len(note_infos)} video notes")
    print(f"Transcript coverage: {sum(1 for record in records if record.get('status') == 'ok')}/{len(records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

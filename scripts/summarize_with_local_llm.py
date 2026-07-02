#!/usr/bin/env python3
"""Generate richer study notes with a local open-source LLM.

Supported backends:

- ollama: talks to a local Ollama server at http://127.0.0.1:11434
- llama-cpp: calls a local llama.cpp-compatible CLI with a GGUF model

No OpenAI API key is used.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import textwrap
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from urllib.error import URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
PLAYLIST_PATH = ROOT / "data" / "playlist.json"
MANIFEST_PATH = ROOT / "transcripts" / "transcript_manifest.json"
OUTPUT_DIR = ROOT / "summaries" / "model_based"
SUMMARY_MANIFEST_PATH = ROOT / "data" / "local_summary_manifest.json"


@dataclass
class SummaryRecord:
    index: int
    video_id: str
    title: str
    status: str
    backend: str
    model: str
    output_path: str = ""
    transcript_words: int = 0
    chunks: int = 0
    elapsed_seconds: float = 0.0
    error: str = ""


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value[:90] or "summary"


def title_topic(title: str) -> str:
    return re.split(r"\s+-\s+", title, maxsplit=1)[0].strip()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_transcript(record: dict) -> str:
    clean_path = record.get("clean_path")
    if not clean_path:
        return ""
    path = ROOT / clean_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def chunk_text(text: str, max_chars: int) -> list[str]:
    paragraphs = [part.strip() for part in re.split(r"\n{2,}", text) if part.strip()]
    if not paragraphs:
        paragraphs = [line.strip() for line in text.splitlines() if line.strip()]

    chunks: list[str] = []
    current: list[str] = []
    current_len = 0
    for paragraph in paragraphs:
        if current and current_len + len(paragraph) + 2 > max_chars:
            chunks.append("\n\n".join(current))
            current = []
            current_len = 0
        if len(paragraph) > max_chars:
            sentences = re.split(r"(?<=[.!?])\s+", paragraph)
            for sentence in sentences:
                if current and current_len + len(sentence) + 1 > max_chars:
                    chunks.append("\n\n".join(current))
                    current = []
                    current_len = 0
                current.append(sentence)
                current_len += len(sentence) + 1
        else:
            current.append(paragraph)
            current_len += len(paragraph) + 2
    if current:
        chunks.append("\n\n".join(current))
    return chunks


def system_instruction() -> str:
    return (
        "You are creating high-quality study notes for an AI engineering learner. "
        "Be concrete, technical, and pedagogical. Do not quote the transcript at length. "
        "Prefer concise synthesis over generic advice."
    )


def chunk_prompt(video: dict, chunk: str, chunk_number: int, chunk_count: int) -> str:
    return f"""\
{system_instruction()}

Summarize transcript chunk {chunk_number}/{chunk_count} for this talk.

Title: {video['title']}
Duration: {video['duration']}

Return Markdown with exactly these sections:

## Chunk Thesis
One paragraph.

## Technical Ideas
- 5-10 concrete bullets.

## Learning Signals
- Concepts, tools, frameworks, or patterns the learner should recognize.

## Risks And Failure Modes
- Practical risks mentioned or implied.

Transcript chunk:
{chunk}
"""


def final_prompt(video: dict, chunk_summaries: list[str]) -> str:
    joined = "\n\n---\n\n".join(chunk_summaries)
    return f"""\
{system_instruction()}

Combine the chunk summaries into one final study note.

Title: {video['title']}
Duration: {video['duration']}
Video: {video['url']}

Return Markdown with exactly these sections:

# {video['title']}

## Executive Summary
2-4 paragraphs. Explain the talk's central idea and why it matters.

## What To Learn
- 5-8 bullets focused on durable concepts.

## Key Concepts
- Term: explanation

## Practical Takeaways
- 5-10 bullets that can change how an engineer builds AI systems.

## Implementation Sketch
Describe a small prototype, eval, or workflow inspired by the talk.

## Failure Modes
- What can go wrong in production?

## Watch Recommendation
Choose one: Watch, Skim, Skip for now, or Deep dive. Explain why.

## Review Questions
- 5 questions that test actual understanding.

Chunk summaries:
{joined}
"""


def ollama_generate(prompt: str, model: str, endpoint: str, temperature: float, timeout: int) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
        },
    }
    request = Request(
        endpoint.rstrip("/") + "/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=timeout) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data.get("response", "").strip()


def llama_cpp_generate(
    prompt: str,
    llama_cli: str,
    gguf_model: str,
    temperature: float,
    timeout: int,
) -> str:
    command = [
        llama_cli,
        "-m",
        gguf_model,
        "-p",
        prompt,
        "--temp",
        str(temperature),
        "-n",
        "2048",
    ]
    result = subprocess.run(command, check=True, capture_output=True, text=True, timeout=timeout)
    return result.stdout.strip()


def generate(prompt: str, args: argparse.Namespace) -> str:
    if args.backend == "ollama":
        return ollama_generate(prompt, args.model, args.ollama_endpoint, args.temperature, args.timeout)
    if args.backend == "llama-cpp":
        if not args.llama_cli or not args.gguf_model:
            raise ValueError("--llama-cli and --gguf-model are required for llama-cpp backend")
        return llama_cpp_generate(prompt, args.llama_cli, args.gguf_model, args.temperature, args.timeout)
    raise ValueError(f"Unsupported backend: {args.backend}")


def select_videos(playlist: dict, records_by_id: dict[str, dict], args: argparse.Namespace) -> list[tuple[dict, dict]]:
    selected: list[tuple[dict, dict]] = []
    for video in playlist["videos"]:
        if video["index"] < args.start_index:
            continue
        if args.only_index and video["index"] not in args.only_index:
            continue
        record = records_by_id.get(video["video_id"], {})
        if record.get("status") != "ok":
            continue
        if args.skip_existing:
            output_path = OUTPUT_DIR / f"{video['index']:03d}-{slugify(title_topic(video['title']))}.md"
            if output_path.exists():
                continue
        selected.append((video, record))
        if args.limit and len(selected) >= args.limit:
            break
    return selected


def summarize_video(video: dict, record: dict, args: argparse.Namespace) -> SummaryRecord:
    start = time.time()
    output_path = OUTPUT_DIR / f"{video['index']:03d}-{slugify(title_topic(video['title']))}.md"
    transcript = load_transcript(record)
    transcript_words = word_count(transcript)
    summary_record = SummaryRecord(
        index=video["index"],
        video_id=video["video_id"],
        title=video["title"],
        status="started",
        backend=args.backend,
        model=args.model if args.backend == "ollama" else args.gguf_model,
        output_path=str(output_path.relative_to(ROOT)),
        transcript_words=transcript_words,
    )

    if not transcript.strip():
        summary_record.status = "missing_transcript"
        return summary_record

    chunks = chunk_text(transcript, args.chunk_chars)
    summary_record.chunks = len(chunks)

    if args.dry_run:
        print(f"DRY RUN {video['index']:03d}: {video['title']}")
        print(f"  words={transcript_words} chunks={len(chunks)} output={output_path.relative_to(ROOT)}")
        print("  first_prompt_preview:")
        print(textwrap.indent(chunk_prompt(video, chunks[0], 1, len(chunks))[:1000], "    "))
        summary_record.status = "dry_run"
        summary_record.elapsed_seconds = time.time() - start
        return summary_record

    chunk_summaries: list[str] = []
    for idx, chunk in enumerate(chunks, start=1):
        prompt = chunk_prompt(video, chunk, idx, len(chunks))
        chunk_summaries.append(generate(prompt, args))

    final_markdown = generate(final_prompt(video, chunk_summaries), args)
    if not final_markdown.startswith("# "):
        final_markdown = f"# {video['title']}\n\n{final_markdown}"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(final_markdown.strip() + "\n", encoding="utf-8")
    summary_record.status = "ok"
    summary_record.elapsed_seconds = time.time() - start
    return summary_record


def merge_manifest(new_records: Iterable[SummaryRecord]) -> dict:
    existing_by_id: dict[str, dict] = {}
    if SUMMARY_MANIFEST_PATH.exists():
        existing = load_json(SUMMARY_MANIFEST_PATH)
        existing_by_id = {record["video_id"]: record for record in existing.get("records", [])}
    for record in new_records:
        existing_by_id[record.video_id] = asdict(record)
    records = sorted(existing_by_id.values(), key=lambda item: item["index"])
    return {
        "records": records,
        "ok_count": sum(1 for record in records if record.get("status") == "ok"),
        "dry_run_count": sum(1 for record in records if record.get("status") == "dry_run"),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=["ollama", "llama-cpp"], default="ollama")
    parser.add_argument("--model", default=os.environ.get("OLLAMA_MODEL", "qwen2.5:7b-instruct"))
    parser.add_argument("--ollama-endpoint", default=os.environ.get("OLLAMA_ENDPOINT", "http://127.0.0.1:11434"))
    parser.add_argument("--llama-cli", default=os.environ.get("LLAMA_CLI", ""))
    parser.add_argument("--gguf-model", default=os.environ.get("GGUF_MODEL", ""))
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--start-index", type=int, default=1)
    parser.add_argument("--only-index", type=int, action="append", default=[])
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--chunk-chars", type=int, default=12000)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    playlist = load_json(PLAYLIST_PATH)
    transcript_manifest = load_json(MANIFEST_PATH)
    records_by_id = {record["video_id"]: record for record in transcript_manifest.get("records", [])}
    selected = select_videos(playlist, records_by_id, args)
    if not selected:
        print("No transcript-backed videos selected.")
        return 0

    records: list[SummaryRecord] = []
    for video, record in selected:
        try:
            summary_record = summarize_video(video, record, args)
        except (URLError, TimeoutError, subprocess.SubprocessError, OSError, ValueError) as exc:
            summary_record = SummaryRecord(
                index=video["index"],
                video_id=video["video_id"],
                title=video["title"],
                status="error",
                backend=args.backend,
                model=args.model if args.backend == "ollama" else args.gguf_model,
                transcript_words=int(record.get("word_count", 0) or 0),
                error=str(exc),
            )
        records.append(summary_record)
        print(f"{summary_record.index:03d} {summary_record.status} chunks={summary_record.chunks} {summary_record.title}")

    if not args.dry_run:
        SUMMARY_MANIFEST_PATH.write_text(json.dumps(merge_manifest(records), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 1 if any(record.status == "error" for record in records) else 0


if __name__ == "__main__":
    raise SystemExit(main())

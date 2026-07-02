#!/usr/bin/env python3
"""Check whether local open-source LLM summarization backends are available."""

from __future__ import annotations

import argparse
import json
import shutil
from urllib.error import URLError
from urllib.request import Request, urlopen


def check_ollama(endpoint: str) -> int:
    try:
        request = Request(endpoint.rstrip("/") + "/api/tags")
        with urlopen(request, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
    except URLError as exc:
        print(f"ollama: not reachable at {endpoint} ({exc})")
        return 1

    models = [model.get("name", "") for model in data.get("models", [])]
    print(f"ollama: reachable at {endpoint}")
    if models:
        print("models:")
        for model in models:
            print(f"- {model}")
    else:
        print("models: none pulled yet")
    return 0


def check_llama_cpp(cli: str) -> int:
    resolved = shutil.which(cli) if cli else None
    if not resolved:
        print(f"llama.cpp: CLI not found ({cli or 'no command provided'})")
        return 1
    print(f"llama.cpp: CLI found at {resolved}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ollama-endpoint", default="http://127.0.0.1:11434")
    parser.add_argument("--llama-cli", default="llama-cli")
    args = parser.parse_args()

    ollama_status = check_ollama(args.ollama_endpoint)
    llama_status = check_llama_cpp(args.llama_cli)
    return 0 if ollama_status == 0 or llama_status == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

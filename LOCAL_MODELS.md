# Local Open-Source Model Pipeline

This project can generate richer summaries without the OpenAI API by using a local LLM runtime.

## Recommended Path: Ollama

Ollama is the simplest local runtime to wire into this project.

Example setup:

```bash
brew install ollama
ollama serve
ollama pull qwen2.5:7b-instruct
```

Then run:

```bash
python3 scripts/check_local_model_backend.py
python3 scripts/summarize_with_local_llm.py \
  --backend ollama \
  --model qwen2.5:7b-instruct \
  --limit 3
```

For the full captured transcript set:

```bash
python3 scripts/summarize_with_local_llm.py \
  --backend ollama \
  --model qwen2.5:7b-instruct
```

Generated model-based notes are written to:

- `summaries/model_based/`
- `data/local_summary_manifest.json`

## Alternative: llama.cpp

If you prefer llama.cpp, use a local GGUF instruct model and pass the CLI/model path:

```bash
python3 scripts/summarize_with_local_llm.py \
  --backend llama-cpp \
  --llama-cli /path/to/llama-cli \
  --gguf-model /path/to/model.gguf \
  --limit 3
```

## Model Choice

Good first-pass local models:

- `qwen2.5:7b-instruct`
- `llama3.1:8b`
- `mistral:7b-instruct`

Use a larger model if you want better synthesis and have enough RAM/VRAM. Use a smaller model if you want speed.

## Cost Model

Local models do not charge per API call. The cost is local compute time, disk space, and electricity. They are also easier to rerun without worrying about token budgets.

## Current Limitation

Only videos with local transcripts in `transcripts/clean/` can be summarized semantically. For videos where YouTube returned `HTTP 429` or no captions, the project still needs either:

- a later transcript retry, or
- local audio download + local Whisper transcription.

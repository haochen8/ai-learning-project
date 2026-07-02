# AI Engineer Learning Project

This project organizes the YouTube playlist "AI Engineer World's Fair Online Track 2026" into a learning path.

Playlist:
https://www.youtube.com/playlist?list=PLcfpQ4tk2k0V1LNigteMgExP1rb4Hy8wn

## Goal

Create a practical study system from the playlist:

- playlist inventory with titles, durations, and video IDs
- transcripts where available
- summaries per talk
- theme grouping across the playlist
- prioritized learning path
- flashcards, quiz questions, and small implementation exercises

## Current Pipeline

1. Fetch playlist metadata:

   ```bash
   python3 scripts/fetch_playlist_metadata.py
   ```

2. Review generated files:

   - `data/playlist.json`
   - `data/playlist_inventory.md`

3. Next steps:

   - fetch YouTube caption tracks where available
   - transcribe missing captions from audio only when needed
   - summarize each video into `summaries/`
   - assemble the final learning path in `study-plan/`

## Local Model Summaries

The project can generate richer summaries with local open-source models and no OpenAI API calls. See `LOCAL_MODELS.md`.

Example with Ollama:

```bash
python3 scripts/summarize_with_local_llm.py --backend ollama --model qwen2.5:7b-instruct --limit 3
```

Outputs:

- `summaries/model_based/`
- `data/local_summary_manifest.json`

## Transcription Strategy

Preferred order:

1. Use YouTube caption/transcript tracks when available.
2. Use local open-source Whisper tooling for missing captions when avoiding API costs.
3. Use API transcription only when speed or quality requirements justify the cost.

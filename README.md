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

## Transcription Strategy

Preferred order:

1. Use YouTube caption/transcript tracks when available.
2. Fall back to `gpt-4o-transcribe` for videos without usable captions.
3. Use `gpt-4o-transcribe-diarize` for panels or multi-speaker sessions.
4. Use `whisper-1` only when word-level timestamps are required.

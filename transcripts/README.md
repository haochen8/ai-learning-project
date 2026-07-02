# Transcripts

Full transcript files are generated locally and ignored by git by default:

- `transcripts/raw/`
- `transcripts/clean/`

The tracked file `transcripts/transcript_manifest.json` records which videos have usable caption text, word counts, source language, and local filenames.

This keeps the repository lightweight and avoids publishing large verbatim transcript files.

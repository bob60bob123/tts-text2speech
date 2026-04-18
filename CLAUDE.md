# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start

```bash
# Option 1: Double-click start.bat (Windows)
start.bat

# Option 2: Manual start
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Access at: **http://127.0.0.1:8000/** (not file://)

## Common Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run server (development with auto-reload)
uvicorn app.main:app --reload

# Syntax check (all core files)
python -m py_compile app/main.py app/api/routes.py app/services/tts_service.py app/services/file_parser.py app/engines/edge_tts_engine.py app/engines/google_tts.py app/engines/pyttsx3_engine.py

# Check single file syntax
python -m py_compile app/engines/edge_tts_engine.py
```

## Architecture

### Backend Structure

```
app/
├── main.py              # FastAPI app entry, serves static + mounts routes
├── api/
│   ├── routes.py        # REST endpoints (tts, upload, audio, voices)
│   └── schemas.py       # Pydantic request/response models
├── services/
│   ├── tts_service.py   # Orchestrates engine selection and conversion
│   ├── file_parser.py   # Extracts text from TXT/PDF/DOCX/MD
│   └── audio_storage.py # Manages temp audio files in temp_audio/
└── engines/
    ├── base.py          # Abstract BaseTTSEngine interface
    ├── edge_tts_engine.py # Primary engine (Microsoft, free, high quality)
    ├── google_tts.py     # Secondary engine (Google)
    └── pyttsx3_engine.py # Offline fallback (Windows SAPI only)
```

### Engine Fallback Pattern

`TTSService` uses a Strategy pattern with fallback. Engines are tried in priority order:
1. **Edge TTS** - Best quality, free, Microsoft servers
2. **Google TTS** - Secondary option
3. **pyttsx3** - Offline fallback (Windows only, uses SAPI)

`BaseTTSEngine` interface requires: `speak()`, `is_available()`, `name`

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/tts` | POST | Convert text → audio, returns audio_id |
| `/api/upload` | POST | Parse file → extract text |
| `/api/audio/{id}` | GET | Stream audio MP3 file |
| `/api/voices` | GET | List Edge TTS voices |
| `/api/health` | GET | Health check |
| `/api/shutdown` | POST | Graceful server shutdown |

### Frontend Structure

```
static/
├── index.html           # Single-page app
├── css/styles.css
└── js/
    ├── api-client.js    # Fetch wrapper for backend API
    ├── audio-player.js  # Audio playback + draggable progress bar
    ├── file-handler.js  # File upload + drag-drop
    └── app.js           # Main orchestration + progress animation
```

### Audio File Lifecycle

- Files stored in `temp_audio/{uuid}.mp3`
- Generated on `/api/tts` call
- Served via `/api/audio/{id}`
- No automatic cleanup (manual deletion only)

## TTS Engine Network Requirements

| Engine | Location | Network Required |
|--------|----------|------------------|
| Edge TTS | Microsoft servers | Yes |
| Google TTS | Google servers | Yes |
| pyttsx3 | Local Windows SAPI | No |

## Voice System

Edge TTS provides 11 Neural voices (Chinese + English). Voice IDs use `*Neural` suffix (e.g., `zh-CN-XiaoxiaoNeural`). The voice dropdown in the UI hardcodes these voice IDs - if adding new voices, update both `index.html` and `app/engines/edge_tts_engine.py`.

## Important Notes

- **CORS**: Frontend must be accessed via `http://127.0.0.1:8000/` not `file://` - relative API URLs only work through the server
- **pyttsx3**: Windows-only, uses Windows SAPI - won't work on Linux/macOS
- **Speed parameter**: Converted from `0.5-2.0` to Edge TTS rate format `+/-%` in `routes.py:43`
- **Audio Range Requests**: The `/api/audio/{id}` endpoint implements HTTP Range requests for seeking. This is required for the draggable progress bar to work. Uses `accept-ranges: bytes` header and returns 206 Partial Content for range requests.

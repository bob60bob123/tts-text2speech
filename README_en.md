# Text-to-Speech (TTS)

A text-to-speech application based on FastAPI + Microsoft Edge TTS, supporting text input, file upload, multiple voice selection, and MP3 download.

## Quick Start

```bash
# Clone the project
git clone https://github.com/bob60bob123/tts-text2speech.git
cd tts-text2speech

# Install dependencies
pip install -r requirements.txt

# Start server
Double-click start.bat or run:
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Open in browser
# http://127.0.0.1:8000
```

## Features

- **Text Input**: Paste text directly for conversion
- **File Upload**: Support TXT, PDF, DOCX, MD formats
- **Multiple Voices**: 11 neural network voices (Chinese + English)
- **Playback Control**: Play/pause, progress drag, speed control (0.5x - 2.0x)
- **MP3 Download**: Save audio after conversion

## Voice List

| Voice ID               | Description        |
| ---------------------- | ------------------ |
| zh-CN-XiaoxiaoNeural  | Xiaoxiao (Female-Young) |
| zh-CN-XiaoyiNeural    | Xiaoyi (Female-Child)   |
| zh-CN-YunxiaNeural    | Yunxia (Female-Young)    |
| zh-CN-YunxiNeural     | Yunxi (Male-Young)       |
| zh-CN-YunyangNeural   | Yunyang (Male-Middle)    |
| zh-CN-YunjianNeural   | Yunjian (Male-Young)     |
| en-US-AriaNeural      | Aria (Female-American)   |
| en-US-GuyNeural       | Guy (Male-American)      |
| en-US-JennyNeural     | Jenny (Female-American)  |
| en-GB-SoniaNeural     | Sonia (Female-British)   |
| en-GB-RyanNeural      | Ryan (Male-British)      |

## Project Structure

```
app/
├── main.py              # FastAPI entry point
├── api/
│   ├── routes.py        # API routes (tts, upload, audio, voices)
│   └── schemas.py       # Pydantic models
├── services/
│   ├── tts_service.py   # TTS engine orchestration
│   ├── file_parser.py   # File parsing (TXT/PDF/DOCX/MD)
│   └── audio_storage.py # Audio storage
└── engines/
    ├── base.py          # Engine abstract base class
    ├── edge_tts_engine.py   # Edge TTS (default)
    ├── google_tts.py         # Google TTS
    └── pyttsx3_engine.py     # pyttsx3 (offline)

static/                  # Frontend resources
├── index.html
├── css/styles.css
└── js/
    ├── api-client.js
    ├── app.js
    ├── audio-player.js  # Audio playback + progress drag
    └── file-handler.js
```

## Tech Stack

- **Frontend**: Vanilla JS/CSS (no framework)
- **Backend**: FastAPI + Python 3.11+
- **TTS Engines**: edge-tts, gtts, pyttsx3
- **File Parsing**: PyPDF2, python-docx, mistune

## Engine Priority

1. **Edge TTS** - Free, high quality, Microsoft servers
2. **Google TTS** - Backup option
3. **pyttsx3** - Fully offline (Windows only)

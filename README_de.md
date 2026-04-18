# Text-to-Speech (TTS)

Eine Text-zu-Sprache-Anwendung basierend auf FastAPI + Microsoft Edge TTS, mit Unterstützung für Texteingabe, Datei-Upload, mehrfache Sprachauswahl und MP3-Download.

## Schnellstart

```bash
# Projekt klonen
git clone https://github.com/bob60bob123/tts-text2speech.git
cd tts-text2speech

# Abhängigkeiten installieren
pip install -r requirements.txt

# Server starten
start.bat doppelklicken oder:
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Im Browser öffnen
# http://127.0.0.1:8000
```

## Funktionen

- **Texteingabe**: Text direkt einfügen und konvertieren
- **Datei-Upload**: Unterstützung für TXT, PDF, DOCX, MD Formate
- **Mehrere Stimmen**: 11 neuronale Netzwerkstimmen (Chinesisch + Englisch)
- **Wiedergabesteuerung**: Abspielen/Pause, Fortschrittsziehbar, Geschwindigkeitsregelung (0.5x - 2.0x)
- **MP3-Speicherung**: Audio nach der Konvertierung speichern

## Stimmliste

| Stimme ID              | Beschreibung          |
| --------------------- | ------------------- |
| zh-CN-XiaoxiaoNeural  | Xiaoxiao (Weiblich-Jung) |
| zh-CN-XiaoyiNeural    | Xiaoyi (Weiblich-Kind)   |
| zh-CN-YunxiaNeural    | Yunxia (Weiblich-Jung)    |
| zh-CN-YunxiNeural     | Yunxi (Männlich-Jung)     |
| zh-CN-YunyangNeural   | Yunyang (Männlich-Mittel) |
| zh-CN-YunjianNeural   | Yunjian (Männlich-Jung)   |
| en-US-AriaNeural      | Aria (Weiblich-Amerikanisch) |
| en-US-GuyNeural       | Guy (Männlich-Amerikanisch)  |
| en-US-JennyNeural     | Jenny (Weiblich-Amerikanisch)|
| en-GB-SoniaNeural     | Sonia (Weiblich-Britisch)    |
| en-GB-RyanNeural      | Ryan (Männlich-Britisch)     |

## Projektstruktur

```
app/
├── main.py              # FastAPI Einstiegspunkt
├── api/
│   ├── routes.py        # API-Routen
│   └── schemas.py       # Pydantic Modelle
├── services/
│   ├── tts_service.py   # TTS-Engine Orchestrierung
│   ├── file_parser.py   # Dateiparsing
│   └── audio_storage.py # Audio-Speicher
└── engines/
    ├── base.py          # Abstrakte Engine-Basisklasse
    ├── edge_tts_engine.py   # Edge TTS (Standard)
    ├── google_tts.py         # Google TTS
    └── pyttsx3_engine.py     # pyttsx3 (Offline)

static/                  # Frontend-Ressourcen
├── index.html
├── css/styles.css
└── js/
    ├── api-client.js
    ├── app.js
    ├── audio-player.js  # Audio-Wiedergabe + Fortschrittsziehbar
    └── file-handler.js
```

## Technologie-Stack

- **Frontend**: Vanilla JS/CSS (kein Framework)
- **Backend**: FastAPI + Python 3.11+
- **TTS-Engines**: edge-tts, gtts, pyttsx3
- **Dateiparsing**: PyPDF2, python-docx, mistune

## Engine-Priorität

1. **Edge TTS** - Kostenlos, hohe Qualität, Microsoft-Server
2. **Google TTS** - Backup-Option
3. **pyttsx3** - Vollständig offline (nur Windows)

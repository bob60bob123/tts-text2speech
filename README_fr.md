# Text-to-Speech (TTS) Synthèse vocale

Une application de synthèse vocale basée sur FastAPI + Microsoft Edge TTS, prenant en charge la saisie de texte, le téléchargement de fichiers, la sélection de plusieurs voix et le téléchargement MP3.

## Démarrage rapide

```bash
# Cloner le projet
git clone https://github.com/bob60bob123/tts-text2speech.git
cd tts-text2speech

# Installer les dépendances
pip install -r requirements.txt

# Démarrer le serveur
Double-cliquez sur start.bat ou:
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Ouvrir dans le navigateur
# http://127.0.0.1:8000
```

## Fonctionnalités

- **Saisie de texte**: Collez du texte directement pour la conversion
- **Téléchargement de fichiers**: Prend en charge les formats TXT, PDF, DOCX, MD
- **Plusieurs voix**: 11 voix de réseau neuronal (chinois + anglais)
- **Contrôle de lecture**: Lecture/pause, barre de progression glissante, contrôle de vitesse (0.5x - 2.0x)
- **Enregistrement MP3**: Enregistrer l'audio après conversion

## Liste des voix

| ID de voix              | Description              |
| ---------------------- | ---------------------- |
| zh-CN-XiaoxiaoNeural  | Xiaoxiao (Femme-Jeune)     |
| zh-CN-XiaoyiNeural    | Xiaoyi (Femme-Enfant)      |
| zh-CN-YunxiaNeural    | Yunxia (Femme-Jeune)       |
| zh-CN-YunxiNeural     | Yunxi (Homme-Jeune)        |
| zh-CN-YunyangNeural   | Yunyang (Homme-Moyen)      |
| zh-CN-YunjianNeural   | Yunjian (Homme-Jeune)      |
| en-US-AriaNeural      | Aria (Femme-Américaine)    |
| en-US-GuyNeural       | Guy (Homme-Américain)      |
| en-US-JennyNeural     | Jenny (Femme-Américaine)   |
| en-GB-SoniaNeural     | Sonia (Femme-Britannique)  |
| en-GB-RyanNeural      | Ryan (Homme-Britannique)   |

## Structure du projet

```
app/
├── main.py              # Point d'entrée FastAPI
├── api/
│   ├── routes.py        # Routes API
│   └── schemas.py       # Modèles Pydantic
├── services/
│   ├── tts_service.py   # Orchestration du moteur TTS
│   ├── file_parser.py   # Analyse de fichiers
│   └── audio_storage.py # Stockage audio
└── engines/
    ├── base.py          # Classe de base abstraite du moteur
    ├── edge_tts_engine.py   # Edge TTS (par défaut)
    ├── google_tts.py         # Google TTS
    └── pyttsx3_engine.py     # pyttsx3 (hors ligne)

static/                  # Ressources frontend
├── index.html
├── css/styles.css
└── js/
    ├── api-client.js
    ├── app.js
    ├── audio-player.js  # Lecture audio + barre de progression glissante
    └── file-handler.js
```

## Stack technologique

- **Frontend**: Vanilla JS/CSS (sans framework)
- **Backend**: FastAPI + Python 3.11+
- **Moteurs TTS**: edge-tts, gtts, pyttsx3
- **Analyse de fichiers**: PyPDF2, python-docx, mistune

## Priorité des moteurs

1. **Edge TTS** - Gratuit, haute qualité, serveurs Microsoft
2. **Google TTS** - Option de secours
3. **pyttsx3** - Entièrement hors ligne (Windows uniquement)

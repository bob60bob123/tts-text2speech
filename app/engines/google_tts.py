"""Google TTS engine using gTTS."""
from pathlib import Path
from gtts import gTTS
import httpx


class GoogleTTSEngine:
    """Online TTS engine using Google gTTS."""

    @property
    def name(self) -> str:
        return "Google TTS (online)"

    def is_available(self) -> bool:
        """Check if Google TTS is available (network connectivity)."""
        try:
            with httpx.Client() as client:
                response = client.get("https://translate.google.com/", timeout=5.0)
                return response.status_code == 200
        except Exception:
            return False

    def speak(self, text: str, output_path: Path, **kwargs) -> Path:
        """Convert text to speech and save to MP3 file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        lang = kwargs.get('lang', 'en')
        tts = gTTS(text=text, lang=lang, slow=kwargs.get('slow', False))
        tts.save(str(output_path))

        return output_path

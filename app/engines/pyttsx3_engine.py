"""Offline TTS engine using pyttsx3."""
from pathlib import Path
import pyttsx3


class Pyttsx3Engine:
    """Offline TTS engine using pyttsx3."""

    def __init__(self):
        self._engine: Optional[pyttsx3.Engine] = None

    @property
    def name(self) -> str:
        return "pyttsx3 (offline)"

    def is_available(self) -> bool:
        """Check if pyttsx3 is available."""
        try:
            engine = pyttsx3.init()
            engine.stop()
            return True
        except Exception:
            return False

    def speak(self, text: str, output_path: Path, **kwargs) -> Path:
        """Convert text to speech and save to MP3 file."""
        engine = pyttsx3.init()

        # Set voice properties if available
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)

        # Set rate (words per minute)
        rate = kwargs.get('speed', 150)
        engine.setProperty('rate', rate)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        engine.save_to_file(text, str(output_path))
        engine.runAndWait()
        engine.stop()

        return output_path

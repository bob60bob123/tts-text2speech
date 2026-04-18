"""TTS Service with engine fallback and voice selection."""
from pathlib import Path
from typing import Optional

from app.engines.base import BaseTTSEngine
from app.engines.edge_tts_engine import EdgeTTSEngine
from app.engines.google_tts import GoogleTTSEngine
from app.engines.pyttsx3_engine import Pyttsx3Engine


class TTSService:
    """TTS Service with engine fallback and voice selection.

    Priority: Edge TTS (free, high quality) -> Google TTS -> pyttsx3 (offline)
    """

    def __init__(self):
        self._engines: list[BaseTTSEngine] = [
            EdgeTTSEngine(),  # Best: free, many voices, Microsoft
            GoogleTTSEngine(),
            Pyttsx3Engine(),
        ]

    @property
    def available_voices(self) -> dict:
        """Return available voices from Edge TTS."""
        for engine in self._engines:
            if isinstance(engine, EdgeTTSEngine):
                return engine.voices
        return {}

    def get_available_engine(self) -> Optional[BaseTTSEngine]:
        """Return first available engine."""
        for engine in self._engines:
            if engine.is_available():
                return engine
        return None

    def convert(self, text: str, output_path: Path,
                engine_name: Optional[str] = None,
                voice: Optional[str] = None,
                **kwargs) -> tuple[Path, str]:
        """Convert text to speech.

        Returns: (output_path, engine_name)
        """
        if engine_name:
            engine = self._find_engine(engine_name)
        else:
            engine = self.get_available_engine()

        if not engine:
            raise RuntimeError("No TTS engine available")

        # Pass voice to Edge TTS
        if voice and isinstance(engine, EdgeTTSEngine):
            kwargs['voice'] = voice

        result_path = engine.speak(text, output_path, **kwargs)
        return result_path, engine.name

    def _find_engine(self, name: str) -> Optional[BaseTTSEngine]:
        """Find engine by name."""
        name_lower = name.lower()
        if 'edge' in name_lower:
            return EdgeTTSEngine()
        elif 'google' in name_lower or 'gtts' in name_lower:
            return GoogleTTSEngine()
        elif 'pyttsx3' in name_lower or 'offline' in name_lower:
            return Pyttsx3Engine()
        return next(
            (e for e in self._engines if name_lower in e.name.lower()),
            None
        )

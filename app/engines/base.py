"""Abstract TTS engine interface."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class BaseTTSEngine(ABC):
    """Abstract TTS engine interface."""

    @abstractmethod
    def speak(self, text: str, output_path: Path, **kwargs) -> Path:
        """Convert text to speech and save to file."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if engine is available (installed/network)."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable engine name."""
        pass

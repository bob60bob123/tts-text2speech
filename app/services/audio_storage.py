"""Audio storage service."""
from pathlib import Path
from typing import Optional
import uuid


class AudioStorage:
    """Audio file storage management."""

    def __init__(self, storage_dir: Path = None):
        self._storage_dir = storage_dir or Path(__file__).parent.parent.parent / "temp_audio"
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        self._registry: dict[str, Path] = {}

    def get_path(self, audio_id: str) -> Path:
        """Get path for audio ID."""
        return self._storage_dir / f"{audio_id}.mp3"

    def register(self, audio_id: str, path: Path) -> None:
        """Register an audio file."""
        self._registry[audio_id] = path

    def get(self, audio_id: str) -> Optional[Path]:
        """Get path for registered audio ID."""
        return self._registry.get(audio_id)

    def generate_id(self) -> str:
        """Generate a new unique audio ID."""
        return str(uuid.uuid4())

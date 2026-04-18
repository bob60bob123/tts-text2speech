"""Pydantic request/response models."""
from pydantic import BaseModel, Field
from typing import Optional


class TTSRequest(BaseModel):
    """Request to convert text to speech."""
    text: str = Field(..., min_length=1, max_length=50000)
    engine: Optional[str] = Field(default="edge", description="TTS engine: edge, google, pyttsx3")
    voice: Optional[str] = Field(default=None, description="Voice ID for Edge TTS")
    speed: float = Field(default=1.0, ge=0.5, le=2.0, description="Playback speed")


class TTSResponse(BaseModel):
    """Response with audio file info."""
    audio_id: str = Field(..., description="Unique ID to retrieve audio")
    engine_used: str = Field(..., description="TTS engine that processed")
    voice_used: Optional[str] = Field(default=None, description="Voice used")
    text_length: int = Field(..., description="Character count")


class FileUploadResponse(BaseModel):
    """Response after file upload."""
    text: str = Field(..., description="Extracted text from file")
    filename: str = Field(..., description="Original filename")
    text_length: int = Field(..., description="Extracted character count")
    supported: bool = Field(..., description="File type supported")


class VoiceInfo(BaseModel):
    """Voice information."""
    id: str
    name: str
    gender: str
    locale: str
    age: str


class VoicesResponse(BaseModel):
    """Response with available voices."""
    voices: dict[str, VoiceInfo]
    default: str = "zh-CN-Xiaoxiao"

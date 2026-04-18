"""API endpoint definitions."""
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import FileResponse

from app.api.schemas import TTSRequest, TTSResponse, FileUploadResponse, VoicesResponse, VoiceInfo
from app.services.tts_service import TTSService
from app.services.file_parser import FileParser
from app.services.audio_storage import AudioStorage

router = APIRouter()
tts_service = TTSService()
audio_storage = AudioStorage()


@router.get("/voices", response_model=VoicesResponse)
async def get_voices():
    """Get available voices for Edge TTS."""
    voices = tts_service.available_voices
    voice_infos = {
        voice_id: VoiceInfo(
            id=voice_id,
            name=info["name"],
            gender=info["gender"],
            locale=info["locale"],
            age=info["age"]
        )
        for voice_id, info in voices.items()
    }
    return VoicesResponse(voices=voice_infos, default="zh-CN-Xiaoxiao")


@router.post("/tts", response_model=TTSResponse)
async def text_to_speech(request: TTSRequest):
    """Convert text to speech.

    Returns audio ID for playback/download.
    """
    audio_id = audio_storage.generate_id()
    output_path = audio_storage.get_path(audio_id)

    try:
        # Convert speed to Edge TTS rate format (+/-%)
        rate_str = f"+{int((request.speed - 1) * 100)}%"
        if request.speed == 1.0:
            rate_str = "+0%"

        result_path, engine_name = tts_service.convert(
            text=request.text,
            output_path=output_path,
            engine_name=request.engine,
            voice=request.voice,
            rate=rate_str
        )

        audio_storage.register(audio_id, result_path)

        return TTSResponse(
            audio_id=audio_id,
            engine_used=engine_name,
            voice_used=request.voice,
            text_length=len(request.text)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Upload and parse a file (TXT, PDF, DOCX).

    Returns extracted text for TTS conversion.
    """
    suffix = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    filename = f".{suffix}" if suffix else ""

    if filename not in FileParser.SUPPORTED:
        return FileUploadResponse(
            text="",
            filename=file.filename,
            text_length=0,
            supported=False
        )

    content = await file.read()

    try:
        text = FileParser.parse_bytes(content, file.filename)
        return FileUploadResponse(
            text=text,
            filename=file.filename,
            text_length=len(text),
            supported=True
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Parse error: {str(e)}")


@router.get("/audio/{audio_id}")
async def get_audio(request: Request, audio_id: str):
    """Stream audio file by ID with proper Range request support."""
    path = audio_storage.get_path(audio_id)
    if not path or not path.exists():
        raise HTTPException(status_code=404, detail="Audio not found")

    file_size = path.stat().st_size
    headers = {
        "accept-ranges": "bytes",
        "content-length": str(file_size),
    }

    # Get Range header from request
    range_header = request.headers.get("range")

    if range_header:
        # Parse Range header (e.g., "bytes=0-999")
        try:
            range_match = range_header.replace("bytes=", "").split("-")
            start = int(range_match[0]) if range_match[0] else 0
            end = int(range_match[1]) if range_match[1] else file_size - 1
        except (ValueError, IndexError):
            start, end = 0, file_size - 1

        # Ensure valid range
        start = max(0, min(start, file_size - 1))
        end = max(start, min(end, file_size - 1))
        content_length = end - start + 1

        headers["content-length"] = str(content_length)
        headers["content-range"] = f"bytes {start}-{end}/{file_size}"
        headers["status_code"] = "206"

        # Read only the requested range
        async def range_iterator():
            with path.open("rb") as f:
                f.seek(start)
                remaining = content_length
                chunk_size = 64 * 1024  # 64KB chunks
                while remaining > 0:
                    chunk = f.read(min(chunk_size, remaining))
                    if not chunk:
                        break
                    remaining -= len(chunk)
                    yield chunk

        from fastapi.responses import StreamingResponse
        return StreamingResponse(
            range_iterator(),
            media_type="audio/mpeg",
            headers=headers,
            status_code=206
        )

    # No Range header - return full file
    async def file_iterator():
        with path.open("rb") as f:
            while chunk := f.read(64 * 1024):
                yield chunk

    from fastapi.responses import StreamingResponse
    return StreamingResponse(
        file_iterator(),
        media_type="audio/mpeg",
        headers=headers
    )

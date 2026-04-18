"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import asyncio

from app.api.routes import router

app = FastAPI(
    title="Text-to-Speech API",
    description="Convert text to speech with file upload support",
    version="1.0.0"
)

# Include API routes
app.include_router(router, prefix="/api")

# Mount static files
static_dir = Path(__file__).parent.parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/")
async def root():
    """Serve main HTML page."""
    return FileResponse(str(static_dir / "index.html"))


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/api/shutdown")
async def shutdown_server():
    """Shutdown the server gracefully."""
    import os
    import signal
    import asyncio

    # Schedule shutdown after response is sent
    asyncio.get_event_loop().call_later(1, lambda: os.kill(os.getpid(), signal.SIGTERM))

    return {"message": "Server shutting down..."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

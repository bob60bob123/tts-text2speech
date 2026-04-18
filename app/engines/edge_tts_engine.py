"""Microsoft Edge TTS engine using edge-tts library."""
from pathlib import Path
import concurrent.futures


class EdgeTTSEngine:
    """Microsoft Edge TTS engine - free, high quality, many voices."""

    # Available voices with metadata (using Neural voices from edge-tts)
    VOICES = {
        # Chinese voices (Neural)
        "zh-CN-XiaoxiaoNeural": {"name": "晓晓 (女声-年轻)", "gender": "Female", "locale": "zh-CN", "age": "Young"},
        "zh-CN-XiaoyiNeural": {"name": "小艺 (女声-童年)", "gender": "Female", "locale": "zh-CN", "age": "Child"},
        "zh-CN-YunxiNeural": {"name": "云希 (男声-年轻)", "gender": "Male", "locale": "zh-CN", "age": "Young"},
        "zh-CN-YunyangNeural": {"name": "云扬 (男声-中年)", "gender": "Male", "locale": "zh-CN", "age": "MiddleAge"},
        "zh-CN-YunjianNeural": {"name": "云健 (男声-年轻)", "gender": "Male", "locale": "zh-CN", "age": "Young"},
        "zh-CN-YunxiaNeural": {"name": "云夏 (女声-年轻)", "gender": "Female", "locale": "zh-CN", "age": "Young"},
        # English voices (Neural)
        "en-US-AriaNeural": {"name": "Aria (女声-美式)", "gender": "Female", "locale": "en-US", "age": "Young"},
        "en-US-GuyNeural": {"name": "Guy (男声-美式)", "gender": "Male", "locale": "en-US", "age": "Young"},
        "en-US-JennyNeural": {"name": "Jenny (女声-美式)", "gender": "Female", "locale": "en-US", "age": "Young"},
        "en-GB-SoniaNeural": {"name": "Sonia (女声-英式)", "gender": "Female", "locale": "en-GB", "age": "Young"},
        "en-GB-RyanNeural": {"name": "Ryan (男声-英式)", "gender": "Male", "locale": "en-GB", "age": "Young"},
    }

    @property
    def name(self) -> str:
        return "Microsoft Edge TTS"

    @property
    def voices(self) -> dict:
        return self.VOICES

    def is_available(self) -> bool:
        """Check if edge-tts is available."""
        try:
            import edge_tts
            return True
        except ImportError:
            return False

    def speak(self, text: str, output_path: Path, **kwargs) -> Path:
        """Convert text to speech and save to MP3 file."""
        voice = kwargs.get('voice', 'zh-CN-XiaoxiaoNeural')
        rate = kwargs.get('rate', '+0%')
        volume = kwargs.get('volume', '+0%')
        pitch = kwargs.get('pitch', '+0Hz')

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Run sync version in thread pool to avoid blocking
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                self._sync_tts, text, str(output_path), voice, rate, volume, pitch
            )
            result_path = future.result()

        return Path(result_path)

    @staticmethod
    def _sync_tts(text: str, output_path: str, voice: str, rate: str, volume: str, pitch: str) -> str:
        """Synchronous TTS using edge-tts."""
        import asyncio
        from edge_tts import Communicate

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            communicate = Communicate(text, voice, rate=rate, volume=volume, pitch=pitch)
            loop.run_until_complete(communicate.save(output_path))
        finally:
            loop.close()
        return output_path

from __future__ import annotations
class InworldConfig:
    """Configuration holder for a Twilio/Media-Streams + Inworld realtime stack.

    Inworld exposes STT/TTS/LLM APIs; the actual realtime websocket plumbing is deployment-specific.
    This class intentionally keeps provider credentials out of business logic.
    """
    def __init__(self, api_key: str, tts_model: str="TTS-2-Flash", stt_model: str="STT-1"):
        self.api_key=api_key; self.tts_model=tts_model; self.stt_model=stt_model
    def configured(self) -> bool: return bool(self.api_key)

from faster_whisper import WhisperModel


class TranscriptionService:
    def __init__(self):
        self.model = WhisperModel(
            "small",
            device="cpu",
            compute_type="int8",
        )

    def transcribe(self, audio_path: str):
        segments, info = self.model.transcribe(
            audio_path,
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()

        return {
            "text": text,
            "language": info.language,
        }

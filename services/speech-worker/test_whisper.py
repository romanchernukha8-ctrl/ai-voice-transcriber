from app.services.transcription_service import TranscriptionService


audio_path = "/tmp/44632b94-490e-4e58-8acb-79e650408361-audio_2026-08-27_12-50-29.ogg"

service = TranscriptionService()

result = service.transcribe(audio_path)

print("Language:", result["language"])
print("Text:", result["text"])

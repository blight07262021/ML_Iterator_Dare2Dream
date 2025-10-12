import torch
from transformers import pipeline

# Initialize the Speech-to-Text pipeline using OpenAI's Whisper model
# This will download the model on the first run.
stt_pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-base", # Using the efficient 'base' version
    torch_dtype=torch.float16,
    device_map="auto",
)

def transcribe_audio(audio_bytes: bytes) -> str:
    """
    Transcribes audio bytes into text using the Whisper model.
    Returns the transcribed text as a string.
    """
    try:
        # The pipeline can directly process the raw bytes of the audio file
        result = stt_pipe(audio_bytes)
        return result["text"].strip()
    except Exception as e:
        print(f"Error during transcription: {e}")
        return ""
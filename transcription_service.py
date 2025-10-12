import whisper
import os
import uuid
from fastapi import UploadFile

# Load the base model once when the application starts
# This is more efficient than loading it for every request.
model = whisper.load_model("base") 
print("✅ Whisper transcription model loaded.")

def transcribe_audio(file: UploadFile) -> str:
    """
    Transcribes an uploaded audio file to text using Whisper.
    """
    # Create a temporary directory if it doesn't exist
    temp_dir = "temp_audio"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Save the uploaded file temporarily
    file_extension = os.path.splitext(file.filename)[1]
    temp_filename = f"{uuid.uuid4()}{file_extension}"
    temp_filepath = os.path.join(temp_dir, temp_filename)

    with open(temp_filepath, "wb") as buffer:
        buffer.write(file.file.read())

    # Transcribe the audio file
    try:
        result = model.transcribe(temp_filepath, fp16=False)
        transcribed_text = result["text"]
    finally:
        # Clean up the temporary file
        os.remove(temp_filepath)

    return transcribed_text
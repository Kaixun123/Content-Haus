from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from app.middlewares.logging import LoggingMiddleware
# from app.middlewares.cors import CorsMiddleware
# from backend.services.process.app.api.v1.process import VectoriseRestController

# export TESSDATA_PREFIX=/usr/local/Cellar/tesseract/5.4.1/share/

from services.extract import extract_text_from_frames, extract_frames
from services.transcribe import extract_audio, transcribe_audio

app = FastAPI()

# Maybe TODO: Move registration of middlewares to separate module
# LoggingMiddleware(app)
# CorsMiddleware(app)

# Maybe TODO: Move registration of routers to separate module
# app.include_router(VectoriseRestController().get_router())

# TODO: Create app router that takes in video UUID. 
# This UUID to be stored as key in cloud bucket.
# Download video from bucket, run it through extract, and transcribe, then use LLM to classify
if __name__ == "__main__":
    video_path = "../data/sample_video.MP4"
    
    # OCR Extraction
    extracted_frames = extract_frames(video_path)
    extracted_text = extract_text_from_frames(extracted_frames)

    # Audio Transcribe Extraction
    extract_audio(video_path, "../data/input/extracted_audio.wav")
    transcribed_text = transcribe_audio("../data/input/extracted_audio.wav")

    with open("../data/output/extracted_text.txt", "w") as text_file:
        text_file.write(f"{extracted_text}\n{transcribed_text}")
    
    print("text extraction complete")

    
    


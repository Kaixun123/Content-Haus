import logging
import os

import moviepy.editor as mp
import speech_recognition as sr
from app.services.extract import clean_text
from pydub import AudioSegment


def extract_audio(video_path, audio_path):
    # Ensure that audio_path exists
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    try:
        video = mp.VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
    except Exception as e:
        logging.warning("ERROR: ", e)
    # os.remove(video_path)


def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_path)
    try:
        # Convert audio to WAV format if it's not already
        wav_audio_path = audio_path.replace(audio_path.split('.')[-1], 'wav')
        audio.export(wav_audio_path, format='wav')

        with sr.AudioFile(wav_audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            # os.remove(wav_audio_path)
            logging.debug("Transcribed text: ", text)
            return clean_text(text)

        # Clean up the temporary wav file
    except sr.UnknownValueError:
        logging.warning("Google Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        logging.warning(f"Could not request results from Google Speech Recognition service; {e}")
        return None
    except Exception as e:
        logging.warning(f"An error occurred: {e}")
        return None
    finally:
        # Clean up the temporary wav file
        # if os.path.exists(wav_audio_path):
        #     os.remove(wav_audio_path)
        pass

# pip install opencv-python pytesseract pillow
# brew install tesseract
import logging
import re

import cv2
import pytesseract
from PIL import Image


def extract_frames(video_path, frame_rate=1):
    """
    Extracts frames from a video file at a specified frame rate.

    Parameters:
    video_path (str): The path to the video file.
    frame_rate (int, optional): The frame rate to extract frames at. Default is 1.

    Returns:
    list: A list of frames extracted from the video file.

    """
    # Open the video file.
    video_capture = cv2.VideoCapture(video_path)

    # Get the total number of frames in the video.
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    # Get the frames per second of the video.
    fps = video_capture.get(cv2.CAP_PROP_FPS)

    # Initialize a list to hold the extracted frames.
    frames = []

    # Loop over each frame in the video.
    for i in range(frame_count):
        # Read the next frame from the video.
        success, frame = video_capture.read()

        # If the frame was not read successfully, then we have reached the end of the video.
        if not success:
            break

        # If the current frame number is a multiple of the frame rate, then add the frame to our list.
        if i % int(fps // frame_rate) == 0:
            frames.append(frame)

    # Release the video file.
    video_capture.release()

    # Return the list of frames.
    return frames


def clean_text(text):
    words = text.split()

    seen = set()
    result = []

    for word in words:
        trimmed_word = word.strip()
        if trimmed_word not in seen:
            seen.add(trimmed_word)
            result.append(trimmed_word)

    cleaned_text = ' '.join(result)
    return cleaned_text


def extract_text_from_frames(frames):
    """
    Extracts text from a list of frames using PyTesseract.

    Parameters:
    frames (List[Frame]): A list of frames to extract text from. Each frame is a numpy array representing the image data of the frame.

    Returns:
    str: A string containing the extracted text from all frames. Text from different frames is separated by a newline character.
    """
    text = ""
    for i, frame in enumerate(frames):
        # Convert frame to greyscale
        grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Pytesseract to extract text
        frame_text = pytesseract.image_to_string(Image.fromarray(grey_frame))

        # Removes all symbols and only takes in alphabetical characters
        text += re.sub(r'[^a-zA-Z\s]', ' ', frame_text)
        text += "\n"

        # TODO: Use appropriate logging library
        logging.debug(f"Processed frame {i + 1}/{len(frames)}")

    return clean_text(text)

from fastapi import FastAPI, APIRouter, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os
import requests  # Add this import for downloading the video from the URL
from moviepy.config import change_settings

from api.v1.base import RestController

# Update the path below to the location of the magick executable
change_settings(
    {"IMAGEMAGICK_BINARY": "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = FastAPI()
router = APIRouter()

class EditorRestController(RestController):
    def register_routes(self):
        @self.router.post("/upload")
        async def upload_video(file: UploadFile = File(...)):
            if file.filename == '':
                raise HTTPException(status_code=400, detail="No selected file")
            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            with open(filepath, "wb") as f:
                f.write(await file.read())
            print(f"File uploaded to {filepath}")
            return {"filename": filename, "file_url": f"/uploads/{filename}"}

        @self.router.post("/edit")
        async def edit_video(request: Request):
            try:
                data = await request.json()
                print("Received edit request with data:", data)

                filename = data.get('filename')
                start_time = data.get('start_time')
                end_time = data.get('end_time')
                texts = data.get('texts', [])

                if not filename or start_time is None or end_time is None:
                    print("Missing data:", {
                        'filename': filename,
                        'start_time': start_time,
                        'end_time': end_time,
                        'texts': texts
                    })
                    raise HTTPException(status_code=400, detail="Missing data")

                # Download the file from the public URL
                local_file_path = os.path.join(UPLOAD_FOLDER, os.path.basename(filename))
                response = requests.get(filename)
                if response.status_code == 200:
                    with open(local_file_path, "wb") as f:
                        f.write(response.content)
                    print(f"File downloaded from URL to {local_file_path}")
                else:
                    raise HTTPException(status_code=404, detail="File could not be downloaded")

                edited_clip_path = os.path.join(UPLOAD_FOLDER, f"edited_{os.path.basename(filename)}")

                video = VideoFileClip(local_file_path).subclip(start_time, end_time)

                text_clips = []
                for text_item in texts:
                    txt_clip = (TextClip(text_item['text'], fontsize=70, color='white', font='Amiri-Bold')
                                .set_position('center')
                                .set_start(text_item['position'])
                                .set_duration(5))  # Display text for 5 seconds
                    text_clips.append(txt_clip)

                final_video = CompositeVideoClip([video] + text_clips)
                final_video.write_videofile(edited_clip_path, codec='libx264')
                print(f"Edited video saved to {edited_clip_path}")
                return FileResponse(edited_clip_path, filename=f"edited_{os.path.basename(filename)}")
            except Exception as e:
                print("Error processing video:", str(e))
                raise HTTPException(status_code=500, detail=str(e))
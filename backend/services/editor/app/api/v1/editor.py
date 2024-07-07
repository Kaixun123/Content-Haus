from flask import Blueprint, request, jsonify, send_file
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os
from io import BytesIO
from moviepy.config import change_settings

# Update the path below to the location of the magick executable
change_settings(
    {"IMAGEMAGICK_BINARY": "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

editor_bp = Blueprint('editor', __name__)


@editor_bp.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        print(f"File uploaded to {filepath}")
        return jsonify({'filename': filename, 'file_url': f'/uploads/{filename}'}), 200


@editor_bp.route('/edit', methods=['POST'])
def edit_video():
    try:
        data = request.get_json()
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
            return jsonify({'error': 'Missing data'}), 400

        filepath = os.path.join(UPLOAD_FOLDER, filename)
        edited_clip_path = os.path.join(UPLOAD_FOLDER, f"edited_{filename}")

        if not os.path.exists(filepath):
            print("File not found:", filepath)
            return jsonify({'error': 'File not found'}), 404

        video = VideoFileClip(filepath).subclip(start_time, end_time)

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
        return send_file(edited_clip_path, as_attachment=True)
    except Exception as e:
        print("Error processing video:", str(e))
        return jsonify({'error': str(e)}), 500

from flask import Flask, send_from_directory
import os
from flask_cors import CORS
from app.api.v1.editor import editor_bp
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = Flask(__name__)
CORS(app)

app.register_blueprint(editor_bp, url_prefix='/api/v1/editor')


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True)

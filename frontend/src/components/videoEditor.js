import React, { useState, useRef } from 'react';
import { Player, ControlBar, PlayToggle, VolumeMenuButton } from 'video-react';
import { FFmpeg } from '@ffmpeg/ffmpeg';
import 'video-react/dist/video-react.css';

const ffmpeg = new FFmpeg({ log: true });

const VideoEditor = () => {
  const [video, setVideo] = useState(null);
  const [videoSrc, setVideoSrc] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [outputVideo, setOutputVideo] = useState(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const loadFFmpeg = async () => {
    await ffmpeg.load();
  };

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      setVideoSrc(url);
      setVideo(file);
    }
  };

  const handleTrimVideo = async () => {
    setIsProcessing(true);
    await loadFFmpeg();
    ffmpeg.writeFile('input.mp4', await fetch(video));
    await ffmpeg.exec('-i', 'input.mp4', '-ss', '00:00:02', '-to', '00:00:10', '-c', 'copy', 'output.mp4');
    const data = await ffmpeg.readFile('output.mp4');
    const url = URL.createObjectURL(new Blob([data.buffer], { type: 'video/mp4' }));
    setVideoSrc(url);
    setIsProcessing(false);
  };

  return (
    <div className="video-editor">
        <div
            className={`mb-4 p-6 border-2 ${isDragOver ? 'border-blue-500' : 'border-gray-300'} border-dashed rounded-lg`}
            onDragOver={(e) => {
                e.preventDefault();
                setIsDragOver(true);
            }}
            onDragLeave={(e) => {
                e.preventDefault();
                setIsDragOver(false);
            }}
            onDrop={async (e) => {
                e.preventDefault();
                setIsDragOver(false);
                const file = e.dataTransfer.files[0];
                if (file) {
                const url = URL.createObjectURL(file);
                setVideoSrc(url);
                setVideo(file);
                }
            }}
            >
            Drag and drop a video file here, or click to select a file
            <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                style={{ display: 'none' }}
                onClick={(e) => e.stopPropagation()} // Prevents the click from bubbling to the div
            />
        </div>
        {videoSrc && (
        <div>
            <Player src={videoSrc}>
            <ControlBar autoHide={false}>
                <PlayToggle />
                <VolumeMenuButton />
            </ControlBar>
            </Player>
            <button
            onClick={handleTrimVideo}
            className="bg-blue-500 text-white px-4 py-2 rounded-lg mt-4"
            disabled={isProcessing}
            >
            {isProcessing ? 'Processing...' : 'Trim Video'}
            </button>
        </div>
        )}
        {outputVideo && (
        <div>
            <h2 className="text-xl font-bold mt-6">Edited Video:</h2>
            <Player src={outputVideo}>
            <ControlBar autoHide={false}>
                <PlayToggle />
                <VolumeMenuButton />
            </ControlBar>
            </Player>
            <a
            href={outputVideo}
            download="output.mp4"
            className="bg-green-500 text-white px-4 py-2 rounded-lg mt-4 inline-block"
            >
            Download Video
            </a>
        </div>
        )}
    </div>
  );
};

export default VideoEditor;

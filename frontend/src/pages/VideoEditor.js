import React, { useState, useRef } from 'react';
import { Player, ControlBar, PlayToggle, VolumeMenuButton } from 'video-react';
import { FFmpeg } from '@ffmpeg/ffmpeg';
import { Modal } from '@mui/base/Modal';
import { styled } from '@mui/system';
import 'video-react/dist/video-react.css';
import '../'

// const ffmpeg = new FFmpeg({ log: true });

const Backdrop = styled('div')(({ theme }) => ({
  zIndex: -1,
  position: 'fixed',
  right: 0,
  bottom: 0,
  top: 0,
  left: 0,
  backgroundColor: 'rgba(0, 0, 0, 0.5)',
  '-webkit-tap-highlight-color': 'transparent',
}));

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  backgroundColor: 'white',
  border: '2px solid #000',
  boxShadow: 24,
  padding: '16px 32px 24px',
};

const VideoEditor = () => {
  const [video, setVideo] = useState(null);
  const [videoSrc, setVideoSrc] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [outputVideo, setOutputVideo] = useState(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');
  const fileInputRef = useRef(null);

  // const loadFFmpeg = async () => {
  //   await ffmpeg.load();
  // };

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      setVideoSrc(url);
      setVideo(file);
      setModalIsOpen(true);
    }
  };

  const handleVideo = async () => {
    setIsProcessing(true);
    // await loadFFmpeg();
    // ffmpeg.writeFile('input.mp4', await fetch(video));
    // await ffmpeg.exec('-i', 'input.mp4', '-ss', '00:00:02', '-to', '00:00:10', '-c', 'copy', 'output.mp4');
    // const data = await ffmpeg.readFile('output.mp4');
    // const url = URL.createObjectURL(new Blob([data.buffer], { type: 'video/mp4' }));
    // setVideoSrc(url);
    // TODO: add proper functions for the uploading process
    // recommend using moviePY for movie editing 
    setIsProcessing(false);
  };

  return (
    <div className="video-editor parent-container flex flex-col items-center justify-center h-screen">
      <h1 className="text-4xl subpixel-antialiased mb-4">Improve your videos</h1>
      <p className="text-xl subpixel-antialiased mb-4">Use our Generative AI service to help improve your video&apos;s viewership count</p>
      {!videoSrc && (
        <div
          className={`mb-4 mt-4 p-10 flex justify-center items-center w-4/5 h-4/6 mx-auto border-2 ${isDragOver ? 'border-blue-500' : 'border-gray-300'} border-dashed rounded-lg`}
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
              setModalIsOpen(true);  // Open the modal upon file drop
            }
          }}
          onClick={() => fileInputRef.current.click()}
        >
          Drag and drop a video file here, or click to select a file
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
        </div>
      )}
      {videoSrc && (
        <div>
          <Player src={videoSrc}>
            <ControlBar autoHide={false}>
              <PlayToggle />
              <VolumeMenuButton />
            </ControlBar>
          </Player>
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

      <Modal
        open={modalIsOpen}
        onClose={() => setModalIsOpen(false)}
        BackdropComponent={Backdrop}
      >
        <div css={style}>
          <h2>Enter Video Editing Details</h2>
          <div>
            <label>
              Start Time:
              <input
                type="text"
                value={startTime}
                onChange={(e) => setStartTime(e.target.value)}
                placeholder="00:00:00"
              />
            </label>
          </div>
          <div>
            <label>
              End Time:
              <input
                type="text"
                value={endTime}
                onChange={(e) => setEndTime(e.target.value)}
                placeholder="00:00:10"
              />
            </label>
          </div>
          <button
            onClick={handleVideo}
            className="bg-blue-500 text-white px-4 py-2 rounded-lg mt-4"
            disabled={isProcessing}
          >
            {isProcessing ? 'Processing...' : 'Trim Video'}
          </button>
        </div>
      </Modal>
    </div>
  );
};

export default VideoEditor;

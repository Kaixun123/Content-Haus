import React, { useState, useRef } from 'react';
import { Player, ControlBar, PlayToggle, VolumeMenuButton } from 'video-react';
import { useNavigate } from 'react-router-dom';
import 'video-react/dist/video-react.css';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const VideoUpload = () => {
  const [videoSrc, setVideoSrc] = useState(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      setVideoSrc(url);
      toast.success('Video uploaded successfully!');
    }
  };

  const handleVideo = async () => {
    // TODO: add proper functions for the uploading process
    // recommend using moviePY for movie editing 
    navigate('/preference', { state: { videoSrc } });
  };

  return (
    <div className="parent-container flex flex-col items-center justify-center min-h-screen">
      <ToastContainer />
      <h1 className="text-4xl subpixel-antialiased mb-4 header-text">Improve your videos</h1>
      <p className="text-xl subpixel-antialiased mb-4 header-text">Use our Generative AI service to help improve your video&apos;s viewership count</p>
      {!videoSrc && (
        <div
          className={`mb-20 mt-4 p-10 flex justify-center items-center w-4/5 h-4/6 mx-auto border-2 ${isDragOver ? 'border-blue-500' : 'border-gray-300'} border-dashed rounded-lg`}
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
        <div className="mb-4 mt-4" style={{ width: '85%', height: '60%' }}>
          <Player src={videoSrc} fluid={false} width="100%" height="100%">
            <ControlBar autoHide={false}>
              <PlayToggle />
              <VolumeMenuButton />
            </ControlBar>
          </Player>
        </div>
      )}

      {videoSrc && (
        <button
          onClick={handleVideo}
          className="bg-blue-500 text-white px-4 py-2 rounded-lg mt-7 mb-20"
        >
          Proceed
        </button>
      )}
    </div>
  );
};

export default VideoUpload;

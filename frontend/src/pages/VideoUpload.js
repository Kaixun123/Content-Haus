import React, { useState, useRef } from 'react';
import axios from 'axios';
import { Player, ControlBar, PlayToggle, VolumeMenuButton } from 'video-react';
import { useNavigate } from 'react-router-dom';
import 'video-react/dist/video-react.css';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import CircularProgress from '@mui/material/CircularProgress';

const VideoUpload = () => {
  const [videoSrc, setVideoSrc] = useState(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      setVideoSrc(url);
      await uploadFile(file);
    }
  };

  const uploadFile = async (file) => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post('http://localhost:8000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.key_id) {
        localStorage.setItem('user_uploaded_url', response.data.key_id);
        toast.success('Video uploaded successfully!');
      } else {
        throw new Error('Upload failed');
      }
    } catch (error) {
      console.error('Error uploading video:', error);
      toast.error('Failed to upload video');
    } finally {
      setLoading(false);
    }
  };

  const handleVideo = () => {
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
              await uploadFile(file);
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
      {loading && (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-500 bg-opacity-75">
          <CircularProgress className='mr-2' />
          <div className="text-white text-xl mt-4">Uploading Video...</div>
        </div>
      )}
    </div>
  );
};

export default VideoUpload;

import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import { Player, ControlBar, PlayToggle, VolumeMenuButton } from 'video-react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const RecommendationEditor = () => {
  const location = useLocation();
  const { videoSrc } = location.state || {};

  return (
    <div className="video-sequence parent-container flex flex-col items-center justify-center min-h-screen p-4">
        <ToastContainer />
        <h1 className="text-4xl subpixel-antialiased mb-4 header-text">Here are our recommendation for you!</h1>
    </div>
  );
};

export default RecommendationEditor;
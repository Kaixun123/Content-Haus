import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import { Player, ControlBar, PlayToggle, VolumeMenuButton } from 'video-react';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const RecommendationEditor = () => {
  const location = useLocation();
  const { videoSrc } = location.state || {};

  const [searchType, setSearchType] = useState('trending');
  const [inputValue, setInputValue] = useState('');
  const [videos, setVideos] = useState(null);

  const handleSearchTypeChange = (type) => {
    setSearchType(type);
    setInputValue('');
  };

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    let endpoint = '';
    switch (searchType) {
      case 'username':
        endpoint = `http://127.0.0.1:8000/username?username=${inputValue}`;
        break;
      case 'hashtag':
        endpoint = `http://127.0.0.1:8000/hashtag?hashtag=${inputValue}`;
        break;
      case 'trending':
        endpoint = 'http://127.0.0.1:8000/trending';
        break;
      default:
        return;
    }

    try {
      const response = await axios.get(endpoint);
      setVideos(response.data);
      console.log(response.data);
    } catch (error) {
      console.error('Error fetching videos:', error);
    }
  };

  return (
    <div className="video-sequence parent-container flex flex-col items-center justify-center min-h-screen p-4">
        <ToastContainer />
        <h1 className="text-4xl subpixel-antialiased mb-4 header-text">Here are our recommendation for you!</h1>


    </div>
  );
};

export default RecommendationEditor;
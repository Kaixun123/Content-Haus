import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Player, ControlBar, PlayToggle, VolumeMenuButton } from 'video-react';
import { FaUser, FaHashtag, FaFire } from 'react-icons/fa';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const TikTokVidRetrieval = () => {
  const location = useLocation();
  const { videoSrc } = location.state || {};
  const navigate = useNavigate();

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
      navigate('/recommendation', { state: { videoSrc } });
    } catch (error) {
      console.error('Error fetching videos:', error);
    }
  };

  return (
    <div className="video-sequence parent-container flex flex-col items-center justify-center min-h-screen p-4">
        <ToastContainer />
        <h1 className="text-4xl subpixel-antialiased mb-4 header-text">What videos would you like for us to search for?</h1>


        <form onSubmit={handleSubmit} className="form-container">
        <div className="flex justify-center mb-4">
          <div
            className={`option-box ${searchType === 'username' ? 'selected' : ''}`}
            onClick={() => handleSearchTypeChange('username')}
          >
            <FaUser className="option-box-icon" />
            <span className="option-box-text">Username</span>
          </div>
          <div
            className={`option-box ${searchType === 'hashtag' ? 'selected' : ''}`}
            onClick={() => handleSearchTypeChange('hashtag')}
          >
            <FaHashtag className="option-box-icon" />
            <span className="option-box-text">Hashtag</span>
          </div>
          <div
            className={`option-box ${searchType === 'trending' ? 'selected' : ''}`}
            onClick={() => handleSearchTypeChange('trending')}
          >
            <FaFire className="option-box-icon" />
            <span className="option-box-text">Trending</span>
          </div>
        </div>

        {(searchType === 'username' || searchType === 'hashtag') && (
          <div className="mb-4 w-11/12">
            <input
              type="text"
              value={inputValue}
              onChange={handleInputChange}
              placeholder={`Enter ${searchType}`}
              className="p-2 border border-gray-300 rounded-lg w-full"
            />
          </div>
        )}

        <button
          type="submit"
          className="search-button"
        >
          Search
        </button>
      </form>

      {videos && (
        <div className="videos-container">
          {/* Render the videos here */}
          {videos.map((video, index) => (
            <div key={index} className="video-item">
              {/* Customize video rendering based on your response structure */}
              <p>{video.title}</p>
              <video src={video.url} controls width="300"></video>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TikTokVidRetrieval;
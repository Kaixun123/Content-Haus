import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { FaUser, FaHashtag, FaFire } from 'react-icons/fa';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import CircularProgress from '@mui/material/CircularProgress';

const TikTokVidRetrieval = () => {
  const location = useLocation();
  const { videoSrc } = location.state || {};
  const navigate = useNavigate();
  const [searchType, setSearchType] = useState('trending');
  const [inputValue, setInputValue] = useState('');
  const [videos, setVideos] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showSearchForm, setShowSearchForm] = useState(true);

  const handleSearchTypeChange = (type) => {
    setSearchType(type);
    setInputValue('');
  };

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);

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
      if (!response.data.error && response.data.urls.length > 0) {
        setVideos(response.data.urls);
        toast.success('Videos found! Now let us do our magic 🎉');
        setShowSearchForm(false);
      } else {
        throw new Error('No videos found or API returned an error');
      }
    } catch (error) {
      console.error('Error fetching videos:', error);
      toast.error('Failed to fetch videos');
    } finally {
      setLoading(false);
    }
  };

  const handleRetry = () => {
    setVideos(null);
    setShowSearchForm(true);
  };

  const handleVideoClick = (videoUrl) => {
    navigate('/recommendedvid', { state: { videoUrl } });
  };

  return (
    <div className="video-sequence parent-container flex flex-col items-center justify-center min-h-screen p-4">
      <ToastContainer />
      <h1 className="text-4xl subpixel-antialiased mb-4 header-text">
        {showSearchForm ? 'What videos would you like for us to search for?' : 'Here are some videos recommended'}
      </h1>

      {showSearchForm ? (
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
          <button type="submit" className="search-button">
            Search
          </button>
        </form>
      ) : (
        <div className="flex flex-col items-center">
          {videos && (
            <div className="videos-container flex flex-row overflow-x-auto space-x-4 mt-4">
              {videos.map((url, index) => (
                <div key={index} className="video-item cursor-pointer" onClick={() => handleVideoClick(url)}>
                  <video
                    src={`https://storage.googleapis.com/tiktok-techjam-storage/${url}`}
                    controls
                    className="h-96"
                    onClick={(e) => e.preventDefault()}
                  />
                </div>
              ))}
            </div>
          )}
          <button
            onClick={handleRetry}
            className="mt-4 bg-red-500 text-white px-4 py-2 rounded hover:bg-red-700"
          >
            Retry
          </button>
        </div>
      )}

      {loading && (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-500 bg-opacity-75">
          <CircularProgress className='mr-2' />
          <div className="text-white text-xl">Retrieving Videos...</div>
        </div>
      )}
    </div>
  );
};

export default TikTokVidRetrieval;

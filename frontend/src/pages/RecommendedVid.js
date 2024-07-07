import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const RecommendedVid = () => {
  const location = useLocation();
  const { videoUrl } = location.state || {};
  const navigate = useNavigate();

  const handleRetry = () => {
    navigate('/preference');
  };

  const handleSubmitRecommendation = async () => {
    try {
      await axios.post('http://127.0.0.1:8000/recommendation', { videoUrl });
      toast.success('Recommendation sent successfully!');
      navigate('/storyboard');
    } catch (error) {
      console.error('Error sending recommendation:', error);
      toast.error('Failed to send recommendation');
    }
  };

  return (
    <div className="flex flex-col items-center p-4 min-h-screen">
      <ToastContainer />
      <h1 className="text-4xl mb-4">Here's Your Recommendation!</h1>
      {videoUrl && (
        <video
          src={`https://storage.googleapis.com/tiktok-techjam-storage/${videoUrl}`}
          controls
          width="300"
          height="400"
        ></video>
      )}
      <div className="flex space-x-4 mt-3">
        <button
          onClick={handleRetry}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Retry
        </button>
        <button
          onClick={handleSubmitRecommendation}
          className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Submit Recommendation
        </button>
      </div>
    </div>
  );

};

export default RecommendedVid;

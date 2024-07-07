import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import ReactPlayer from 'react-player';
import Slider from 'rc-slider';
import 'rc-slider/assets/index.css';
import { TextField, Button, Typography, Box, Container, Backdrop, CircularProgress } from '@mui/material';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import '../App.css';

const RecommendationEditor = () => {
  const [fileUrl, setFileUrl] = useState('');
  const [uploadFilename, setUploadFilename] = useState('');
  const [startTime, setStartTime] = useState(0);
  const [endTime, setEndTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [text, setText] = useState('');
  const [textPosition, setTextPosition] = useState(0);
  const [texts, setTexts] = useState([]);
  const [previewVideoUrl, setPreviewVideoUrl] = useState('');
  const [editedVideoBlob, setEditedVideoBlob] = useState(null);
  const [loading, setLoading] = useState(false); // Add state to manage loading
  const playerRef = useRef(null);

  useEffect(() => {
    const userUploadedUrl = "https://storage.googleapis.com/tiktok-techjam-storage/" + localStorage.getItem('user_uploaded_url');
    if (userUploadedUrl) {
      setFileUrl(userUploadedUrl);
      setUploadFilename(userUploadedUrl);
      console.log("URL retrieved from localStorage: ", userUploadedUrl);
    }
  }, []);

  const handleUrlChange = (e) => {
    const url = e.target.value;
    setFileUrl(url);
    setPreviewVideoUrl(''); // Clear previous preview
    setUploadFilename(url.split('/').pop()); // Extract filename from URL
    console.log("URL entered: ", url);
  };

  const handleEdit = async () => {
    const editData = {
      filename: uploadFilename,
      start_time: startTime,
      end_time: endTime,
      texts,
    };

    console.log("Sending edit request with data:", editData);
    setLoading(true); // Set loading to true when the edit process starts

    try {
      const response = await axios.post('http://127.0.0.1:5000/edit', editData, {
        headers: {
          'Content-Type': 'application/json',
        },
        responseType: 'blob',
      });

      const url = URL.createObjectURL(new Blob([response.data], { type: 'video/mp4' }));
      setPreviewVideoUrl(url);
      setEditedVideoBlob(new Blob([response.data], { type: 'video/mp4' })); // Store the edited video blob
      console.log("Edited video URL: ", url);
      toast.success("Video edited successfully.");
    } catch (error) {
      console.error('Error editing video:', error);
      toast.error("Error editing video.");
    } finally {
      setLoading(false); // Set loading to false when the edit process finishes
    }
  };

  const addText = () => {
    setTexts([...texts, { text, position: textPosition }]);
    setText('');
    setTextPosition(0);
    toast.success("Text added to video.");
  };

  const handleDuration = (duration) => {
    setDuration(duration);
    setEndTime(duration);
    console.log("Video duration set to: ", duration);
  };

  const handleProgress = (state) => {
    if (playerRef.current) {
      const currentTime = playerRef.current.getCurrentTime();
      console.log("Current video time: ", currentTime);
      // Logic to update preview can be added here
    }
  };

  const downloadVideo = () => {
    if (editedVideoBlob) {
      const url = URL.createObjectURL(editedVideoBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = uploadFilename;
      link.click();
    }
  };

  return (
    <Container className="App">
      <Typography variant="h3" gutterBottom>Video Editor</Typography>
      <TextField
        label="Video URL"
        fullWidth
        variant="outlined"
        onChange={handleUrlChange}
        value={fileUrl}
        sx={{ mb: 2 }}
      />
      <ToastContainer />
      {fileUrl && (
        <Box className="editor-container" display="flex">
          <Box className="video-preview" flex={1}>
            <ReactPlayer
              ref={playerRef}
              url={fileUrl}
              controls
              onDuration={handleDuration}
              onProgress={handleProgress}
              className="react-player"
            />
            {previewVideoUrl && (
              <Box mt={4}>
                <Typography variant="h6">Edited Video Preview:</Typography>
                <ReactPlayer
                  url={previewVideoUrl}
                  controls
                  className="react-player"
                />
                <Button
                  className="mt-4 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-700"
                  onClick={downloadVideo}
                >
                  Download Edited Video
                </Button>
              </Box>
            )}
          </Box>
          <Box className="editor-options" flex={1}>
            <Typography variant="h6">Select Start and End Time:</Typography>
            <Slider
              range
              min={0}
              max={duration}
              defaultValue={[0, duration]}
              onChange={(values) => {
                setStartTime(values[0]);
                setEndTime(values[1]);
                console.log("Start time set to: ", values[0]);
                console.log("End time set to: ", values[1]);
              }}
              step={0.1}
              tipFormatter={(value) => `${value.toFixed(1)}s`}
            />
            <Typography variant="body1">Start Time: {startTime.toFixed(1)}s</Typography>
            <Typography variant="body1">End Time: {endTime.toFixed(1)}s</Typography>
            <Typography variant="h6" mt={4}>Add Text to Video:</Typography>
            <TextField
              label="Text"
              value={text}
              onChange={(e) => setText(e.target.value)}
              sx={{ mr: 2, mt: 2 }}
            />
            <TextField
              label="Position (seconds)"
              type="number"
              value={textPosition}
              onChange={(e) => setTextPosition(Number(e.target.value))}
              sx={{ mr: 2, mt: 2 }}
            />
            <Button variant="contained" onClick={addText} sx={{ mt: 2 }}>Add Text</Button>
            <Box mt={2}>
              {texts.map((textItem, index) => (
                <Typography key={index} variant="body2">
                  {textItem.text} at {textItem.position.toFixed(1)}s
                </Typography>
              ))}
            </Box>
            <Button variant="contained" onClick={handleEdit} sx={{ mt: 4 }}>Confirm Edits</Button>
          </Box>
        </Box>
      )}
      <Backdrop sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }} open={loading}>
        <CircularProgress color="inherit" />
        <div className="text-white text-xl">Editing Video...</div>
      </Backdrop>
    </Container>
  );
};

export default RecommendationEditor;

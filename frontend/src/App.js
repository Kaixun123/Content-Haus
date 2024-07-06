import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AppRouter } from "./routes/AppRouter";

import './App.css';
import 'video-react/dist/video-react.css';
import VideoEditor from './components/videoEditor';
import HomePage from './components/homepage';

function App() {
  return (
    <BrowserRouter>
      <AppRouter />
    </BrowserRouter>
  );
}

export default App;

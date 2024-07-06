import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AppRouter } from "./routes/AppRouter";

import './App.css';
import 'video-react/dist/video-react.css';
import 'react-toastify/dist/ReactToastify.css';

// toastify notification - make sure to import this in to the respectative pages when needed.
// import { ToastContainer, toast } from 'react-toastify';
// import 'react-toastify/dist/ReactToastify.css';

function App() {
  return (
    <BrowserRouter>
      <AppRouter />
    </BrowserRouter>
  );
}

export default App;

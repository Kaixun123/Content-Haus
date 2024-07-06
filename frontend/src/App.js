import './App.css';
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import 'video-react/dist/video-react.css';
import VideoEditor from './components/videoEditor';
import HomePage from './components/homepage';

function App() {
  return ( 
    <BrowserRouter>
      <div className="App">
        <main className="container mx-auto">
          <Routes>
            <Route path="/" element={<HomePage/>}/>
            <Route path="/editor" element={<VideoEditor/>}/>
            {/* Add more routes as needed */}
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;

import React, { useState, useRef } from 'react';
import { Link } from 'react-router-dom';
import homepagePic from '../assets/homepage-pic.png'

function HomePage() {
    return(
        <div className="flex items-center justify-center h-screen">
            <div className="flex justify-between items-center w-full mx-auto">
                <div className="ml-32 space-x-2">
                    <h1 className="subpixel-antialiased text-8xl">Content-Haus</h1>
                    <p className="subpixel-antialiased text-2xl mt-9">Don't just make your videos popular, make them famous.</p>
                    <Link 
                        to="/editor" 
                        className="py-4 px-6 bg-blue-500 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 mt-9 inline-block"
                    >
                        Upload Video
                    </Link>
                </div>
                <img src={homepagePic} alt="Homepage" className="w-2/6 mr-28" />
            </div>
        </div>
    )
}

export default HomePage;
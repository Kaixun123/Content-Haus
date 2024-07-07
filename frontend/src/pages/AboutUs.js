import React, { useState, useRef } from 'react';
import { Link } from 'react-router-dom';

function AboutUs() {
    return(
        <div className="flex items-center justify-center h-screen">
            <div className="flex justify-between items-center w-full mx-auto">
                <div className="ml-32 space-x-2">
                    <h1 className="subpixel-antialiased text-8xl">About Us</h1>
                    <p className="subpixel-antialiased text-2xl mt-9">Nothing much to see here. It&apos;s time to go back</p>
                </div>
            </div>
        </div>
    )
}

export default AboutUs;
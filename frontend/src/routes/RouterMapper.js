import { useEffect } from 'react';
import { useNavigate } from "react-router-dom";

// Import Pages
import HomePage from "../pages/HomePage";
import VideoUpload from '../pages/VideoUpload';
import AboutUs from '../pages/AboutUs';
import TikTokVidRetrieval from '../pages/TiktokRetrieval';
import RecommendationEditor from '../pages/RecommendationEditor';
import StoryBoardPage from '../pages/StoryBoard';
import RecommendedVid from '../pages/RecommendedVid';

// Redirect to home
const RedirectToHome = () => {
    const navigate = useNavigate();

    useEffect(() => {
        navigate('/home');
    }, [navigate]);

    return null;
}

// Route Mapping
export const PUBLIC_ROUTE_MAPS = [
    { path: "/", element: <RedirectToHome />},
    { path: "/home", element: <HomePage />},
    { path: "/editor", element: <VideoUpload />},
    { path: "/preference", element: <TikTokVidRetrieval/>},
    { path: "/about-us", element: <AboutUs />},
    { path: "/recommendedvid", element: <RecommendedVid/>},
    { path: "/recommendation", element: <RecommendationEditor/>},
    { path: "/storyboard", element: <StoryBoardPage/>}
];


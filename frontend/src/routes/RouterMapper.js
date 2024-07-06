import { useEffect } from 'react';
import { useNavigate } from "react-router-dom";

// Import Pages
import HomePage from "../pages/HomePage";


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
];


import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Button, Spin, notification } from 'antd';
import { useNavigate, useLocation } from 'react-router-dom';
import Storyboard from '../components/storyboard/StoryboardComponent';

const getStoryboard = async (storyboardKey) => {
    // Key - the bucket key for video stored in cloud
    const baseURL = "http://localhost:5003";
    const storyboardURL = new URL("/process-video", baseURL);
    const response = await axios.post(storyboardURL, {
        key: storyboardKey // Set to louis.mp4 for testing purposes
    });
    return response.data;
}

const StoryBoardPage = () => {
    const [loading, setLoading] = useState(true);
    const [storyboard, setStoryboard] = useState(null);
    const navigate = useNavigate();
    const location = useLocation();

    const storyboardKey = null; // navigate('/storyboard', {state: {storyboardKey: 'louis.mp4;}});
    if (location.state && location.state.storyboardKey) {
        storyboardKey = location.state.storyboardKey;
    }

    useEffect(() => {
        const fetchStoryboard = async () => {
            try {
                const data = await getStoryboard(storyboardKey);
                setStoryboard(data);
                setLoading(false);
            } catch (error) {
                notification.error({
                    message: 'Error',
                    description: 'Failed to fetch storyboard data.',
                });
                setLoading(false);
            }
        };
        fetchStoryboard();
    }, []);

    if (loading) {
        return <Spin size="large" />;
    }

    return (
        <div>
            <h1>Story Board Page</h1>
            {storyboard && storyboard.data && <Storyboard data={storyboard.data} />}
            <Button type="primary" onClick={() => navigate('/home')}>
                Back to Home
            </Button>
        </div>
    );
}

export default StoryBoardPage;

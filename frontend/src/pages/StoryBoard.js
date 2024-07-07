import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Button, Spin, notification, Layout, Typography, Space } from 'antd';
import { useNavigate, useLocation } from 'react-router-dom';
import StoryboardComponent from '../components/storyboard/StoryboardComponent';

const { Header, Content } = Layout;
const { Title } = Typography;

const getStoryboard = async (storyboardKey) => {
    // Key - the bucket key for video stored in cloud
    const baseURL = "http://localhost:5003";
    const storyboardURL = new URL("/process-video", baseURL);
    const response = await axios.post(storyboardURL, {
        key: "louis.mp4" // Set to louis.mp4 for testing purposes
    });
    return response.data;
};

const StoryBoardPage = () => {
    const [loading, setLoading] = useState(true);
    const [storyboard, setStoryboard] = useState(null);
    const navigate = useNavigate();
    const location = useLocation();

    let storyboardKey = null;
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
    }, [storyboardKey]);

    if (loading) {
        return (
            <Layout style={{ minHeight: '100vh' }}>
                <Content style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                    <Spin size="large" />
                </Content>
            </Layout>
        );
    }

    return (
        <Layout style={{ minHeight: '100vh' }}>
            <Header style={{ background: '#fff', padding: '0 16px' }}>
                <Title level={2} style={{ margin: '16px 0' }}>
                    Storyboard Editor
                </Title>
            </Header>
            <Content style={{ padding: '0 50px', overflowY: 'auto', height: 'calc(100vh - 64px)' }}>
                <Space direction="vertical" size="large" style={{ width: '100%' }}>
                    {storyboard && storyboard.data && <StoryboardComponent data={storyboard.data} />}
                    <Button type="primary" onClick={() => navigate('/home')}>
                        Back to Home
                    </Button>
                </Space>
            </Content>
        </Layout>
    );
};

export default StoryBoardPage;
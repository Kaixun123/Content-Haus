import React from 'react';
import { Card, Button, Typography, Space } from 'antd';

const { Text, Paragraph } = Typography;

function SceneCard({ scene, onEdit }) {
    return (
        <Card
            title={`Scene ${scene.id}`}
            extra={<Button type="primary" onClick={onEdit}>Edit</Button>}
            style={{ marginBottom: '20px', borderRadius: '8px', boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)' }}
        >
            <Space direction="vertical" size="middle" style={{ width: '100%' }}>
                <Paragraph>
                    <Text strong>Visual:</Text> {scene.visual}
                </Paragraph>
                <Paragraph>
                    <Text strong>Audio:</Text> {scene.audio}
                </Paragraph>
            </Space>
        </Card>
    );
}

export default SceneCard;

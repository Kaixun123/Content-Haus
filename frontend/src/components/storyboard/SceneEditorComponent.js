import React, { useState } from 'react';
import { Form, Input, Button } from 'antd';

const { TextArea } = Input;

function SceneEditor({ scene, onSave }) {
    const [visual, setVisual] = useState(scene.visual);
    const [audio, setAudio] = useState(scene.audio);

    const handleSubmit = () => {
        onSave({ ...scene, visual, audio });
    };

    return (
        <Form layout="vertical" onFinish={handleSubmit} style={{ marginBottom: '20px' }}>
            <Form.Item label="Visual">
                <TextArea
                    value={visual}
                    onChange={(e) => setVisual(e.target.value)}
                    rows={4}
                />
            </Form.Item>
            <Form.Item label="Audio">
                <TextArea
                    value={audio}
                    onChange={(e) => setAudio(e.target.value)}
                    rows={4}
                />
            </Form.Item>
            <Form.Item>
                <Button type="primary" htmlType="submit">Save</Button>
            </Form.Item>
        </Form>
    );
}

export default SceneEditor;

import React, { useState } from 'react';
import { Form, Input, Button } from 'antd';

const { TextArea } = Input;

function SceneEditor({ scene, onSave }) {
    const [visual, setVisual] = useState(scene.visual);
    const [audio, setAudio] = useState(scene.audio);
    const [voiceover, setVoiceover] = useState(scene.voiceover);
    const [textOverlay, setTextOverlay] = useState(scene.textOverlay);

    const handleSubmit = () => {
        onSave({ ...scene, visual, audio, voiceover, textOverlay });
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
            <Form.Item label="Voiceover">
                <TextArea
                    value={voiceover}
                    onChange={(e) => setVoiceover(e.target.value)}
                    rows={4}
                />
            </Form.Item>
            <Form.Item label="Text Overlay">
                <TextArea
                    value={textOverlay}
                    onChange={(e) => setTextOverlay(e.target.value)}
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

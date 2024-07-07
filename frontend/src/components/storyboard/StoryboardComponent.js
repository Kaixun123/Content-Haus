import React, { useState } from 'react';
import SceneEditor from './SceneEditorComponent';
import SceneCard from './StoryboardCardComponent';

// Helper function to parse markdown data
const parseData = (data) => {
    const scenePattern = /\*\*Scene (\d+):\*\*\n\n\* \*\*Visual:\*\* (.*?)\n\* \*\*Audio:\*\* (.*?)(?=\n\n\*\*Scene|\n\n$)/gs;
    const scenes = [];
    let match;

    while ((match = scenePattern.exec(data)) !== null) {
        const [, id, visual, audio] = match;
        scenes.push({
            id: parseInt(id, 10),
            visual: visual.trim(),
            audio: audio.trim()
        });
    }

    return scenes;
};

// Data retrieved is in markdown
const StoryboardComponent = ({ data }) => {
    const [scenes, setScenes] = useState(parseData(data));
    const [editingSceneId, setEditingSceneId] = useState(null);

    const handleEditScene = (id) => {
        setEditingSceneId(id);
    };

    const handleSaveScene = (updatedScene) => {
        setScenes(scenes.map(scene => (scene.id === updatedScene.id ? updatedScene : scene)));
        setEditingSceneId(null);
    };

    return (
        <div className="App">
            {scenes.map(scene => (
                editingSceneId === scene.id ? (
                    <SceneEditor key={scene.id} scene={scene} onSave={handleSaveScene} />
                ) : (
                    <SceneCard key={scene.id} scene={scene} onEdit={() => handleEditScene(scene.id)} />
                )
            ))}
        </div>
    );
};

export default StoryboardComponent;

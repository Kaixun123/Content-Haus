import React from 'react';
import ReactMarkdown from 'react-markdown';


// Helper function to parseMarkdown

// Data retrieved is in markdown
const StoryboardComponent = ({ data }) => {
    return (
        <div>
            {data ? (
                <ReactMarkdown>
                    {data}
                </ReactMarkdown>
            ) : (
                <div>No storyboard data available.</div>
            )}
        </div>
    );
};

export default StoryboardComponent;

import React, { useState, useEffect } from 'react';
import './App.css';

// For now, we'll use REST API as a simple alternative to gRPC-Web
// gRPC-Web requires an Envoy proxy which adds complexity for Render.com
// We'll create a simple HTTP wrapper around the gRPC backend

function App() {
    console.log('Backend URL:', process.env.REACT_APP_BACKEND_URL);
    const [currentJoke, setCurrentJoke] = useState(null);
    const [jokes, setJokes] = useState([]);
    const [currentIndex, setCurrentIndex] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Fetch jokes from backend
    useEffect(() => {
        const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

        fetch(`${backendUrl}/api/jokes`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch jokes');
                }
                return response.json();
            })
            .then(data => {
                setJokes(data.jokes);
                if (data.jokes.length > 0) {
                    setCurrentJoke(data.jokes[0]);
                }
                setLoading(false);
            })
            .catch(err => {
                setError(err.message);
                setLoading(false);
            });
    }, []);

    // Cycle through jokes every second
    useEffect(() => {
        if (jokes.length === 0) return;

        const interval = setInterval(() => {
            setCurrentIndex(prevIndex => {
                const nextIndex = (prevIndex + 1) % jokes.length;
                setCurrentJoke(jokes[nextIndex]);
                return nextIndex;
            });
        }, 1000);

        return () => clearInterval(interval);
    }, [jokes]);

    if (loading) {
        return (
            <div className="App">
                <div className="joke-container">
                    <h1>🎭 Joke Streamer</h1>
                    <p>Loading jokes...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="App">
                <div className="joke-container error">
                    <h1>🎭 Joke Streamer</h1>
                    <p>Error: {error}</p>
                </div>
            </div>
        );
    }

    return (
        <div className="App">
            <div className="joke-container">
                <h1>🎭 Joke Streamer</h1>
                {currentJoke && (
                    <div className="joke">
                        <div className="joke-number">
                            Joke {currentIndex + 1} of {jokes.length}
                        </div>
                        <div className="setup">{currentJoke.setup}</div>
                        <div className="punchline">{currentJoke.punchline}</div>
                    </div>
                )}
                <div className="progress-dots">
                    {jokes.map((_, index) => (
                        <span
                            key={index}
                            className={`dot ${index === currentIndex ? 'active' : ''}`}
                        />
                    ))}
                </div>
            </div>
        </div>
    );
}

export default App;

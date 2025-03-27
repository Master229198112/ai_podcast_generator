const API_BASE = import.meta.env.VITE_API_URL;
import React, { useState } from "react";
import aircLogo from "./AIRC.jpg";
import woxsenLogo from "./woxsen.png";

const App = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [topic, setTopic] = useState("");
    const [inputType, setInputType] = useState("pdf");
    const [backgroundMusic, setBackgroundMusic] = useState("none");
    const [voiceSample, setVoiceSample] = useState(null);
    const [useClonedVoice, setUseClonedVoice] = useState(false);
    const [customHostName, setCustomHostName] = useState("Rahul");
    const [loading, setLoading] = useState(false);
    const [progress, setProgress] = useState(0);
    const [audioUrl, setAudioUrl] = useState(null);
    const [errorMessage, setErrorMessage] = useState(null);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
        setTopic("");
        setAudioUrl(null);
        setErrorMessage(null);
    };

    const handleTopicChange = (event) => {
        setTopic(event.target.value);
        setSelectedFile(null);
        setAudioUrl(null);
        setErrorMessage(null);
    };

    const handleMusicChange = (event) => {
        setBackgroundMusic(event.target.value);
    };

    const handleVoiceSampleChange = (event) => {
        setVoiceSample(event.target.files[0]);
    };

    const toggleVoiceCloning = () => {
        setUseClonedVoice(!useClonedVoice);
    };

    const handleSubmit = async () => {
        setLoading(true);
        setErrorMessage(null);
        setAudioUrl(null);
        setProgress(10);
    
        const formData = new FormData();
        if (inputType === "pdf" && selectedFile) {
            formData.append("file", selectedFile);
        } else if (inputType === "topic" && topic.trim()) {
            formData.append("topic", topic);
        } else {
            setErrorMessage("Please provide a valid input.");
            setLoading(false);
            return;
        }
    
        formData.append("background_music", backgroundMusic);
        formData.append("host_name", useClonedVoice ? customHostName : "Rahul");
    
        if (useClonedVoice && voiceSample) {
            formData.append("voice_sample", voiceSample);
        }
    
        let simulatedProgress = 1;
        const interval = setInterval(() => {
            simulatedProgress += Math.random() * 0.5; // Increase 5–8% per tick
            if (simulatedProgress < 90) {
                setProgress(simulatedProgress);
            }
        }, 500);
    
        try {
            const endpoint = inputType === "pdf" ? `${API_BASE}/upload` : `${API_BASE}/generate`;
            const response = await fetch(endpoint, {
                method: "POST",
                body: formData,
            });
    
            const data = await response.json();
    
            if (response.ok) {
                clearInterval(interval);
                setProgress(100);
                const audioResponse = await fetch(`${API_BASE}${data.audio}`, {
                    headers: {
                        'ngrok-skip-browser-warning': 'true'
                    }
                });
                const audioBlob = await audioResponse.blob();
                const audioBlobUrl = URL.createObjectURL(audioBlob);
                setAudioUrl(audioBlobUrl);                
            } else {
                throw new Error(data.error || "Failed to process request.");
            }
        } catch (error) {
            console.error("Error:", error);
            setErrorMessage(error.message);
        } finally {
            clearInterval(interval);
            setLoading(false);
        }
    };    

    return (
        <>
        <div className="app-container">
            <header className="header">
            <a href="https://airc.example.com" target="_blank" rel="noopener noreferrer">
                <img src={aircLogo} alt="AIRC Logo" className="logo-left" />
            </a>
            <a href="https://woxsen.edu.in" target="_blank" rel="noopener noreferrer">
                <img src={woxsenLogo} alt="Woxsen Logo" className="logo-right" />
            </a>
            </header>

            <div className="tile">
                <h1 className="title">AI Podcast Generator 🎙️</h1>

                <div className="radio-group">
                    <label>
                        <input type="radio" value="pdf" checked={inputType === "pdf"} onChange={() => setInputType("pdf")} /> Upload PDF
                    </label>
                    <label>
                        <input type="radio" value="topic" checked={inputType === "topic"} onChange={() => setInputType("topic")} /> Enter Topic
                    </label>
                </div>

                {inputType === "pdf" ? (
                    <input type="file" onChange={handleFileChange} className="input-field" />
                ) : (
                    <input type="text" placeholder="Enter a topic..." value={topic} onChange={handleTopicChange} className="input-field" />
                )}

                <div className="music-selection">
                    <label>Select Background Music:</label>
                    <select onChange={handleMusicChange} className="input-field">
                        <option value="none">None</option>
                        <option value="jazz">Jazz</option>
                        <option value="ambient">Ambient</option>
                        <option value="lofi">Lo-Fi</option>
                    </select>
                </div>

                <div className="music-selection">
                    <label>
                        <input type="checkbox" checked={useClonedVoice} onChange={toggleVoiceCloning} /> Enable Voice Cloning
                    </label>
                    {useClonedVoice && (
                        <>
                            <input type="text" placeholder="Enter Host Name (e.g. Vishal)" onChange={(e) => setCustomHostName(e.target.value)} className="input-field" />
                            <input type="file" accept="audio/*" onChange={handleVoiceSampleChange} className="input-field" />
                        </>
                    )}
                </div>

                <button onClick={handleSubmit} className="btn" disabled={loading}>
                    {loading ? "Processing..." : "Generate Podcast"}
                </button>

                {loading && (
                    <div className="progress-bar">
                        <div className="progress" style={{ width: `${progress}%` }}></div>
                    </div>
                )}

                {audioUrl && (
                    <div className="audio-container">
                        <h2 className="audio-title">Generated Audio:</h2>
                        <audio controls className="audio-player">
                            <source src={audioUrl} type="audio/mpeg" />
                            Your browser does not support the audio element.
                        </audio>
                    </div>
                )}

                {errorMessage && (
                    <div className="error-message">
                        Error: {errorMessage}
                    </div>
                )}
            </div>
        </div>  
    
            <footer className="footer">
            Developed by <a href="https://www.linkedin.com/in/mastervishal/" target="_blank" rel="noopener noreferrer">
                Vishal Kumar Sharma
            </a>
            </footer>
        </>
    );
};



export default App;

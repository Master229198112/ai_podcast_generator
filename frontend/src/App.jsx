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
    const [showInfo, setShowInfo] = useState(false);
    const [projectName, setProjectName] = useState("");
    const [videoUrl, setVideoUrl] = useState(null);
    const [videoGenerating, setVideoGenerating] = useState(false);
    const [useClonedVoice2, setUseClonedVoice2] = useState(false);
    const [voice_sample_2, setvoice_sample_2] = useState(null);
    const [customHostName2, setCustomHostName2] = useState("Emy");




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

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setErrorMessage(null);
        setAudioUrl(null);
        setVideoUrl(null);
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
        formData.append("host_name_2", useClonedVoice2 ? customHostName2 : "Emy");

        if (useClonedVoice && voiceSample) {
        formData.append("voice_sample", voiceSample);
        }
        if (useClonedVoice2 && voice_sample_2) {
        formData.append("voice_sample_2", voice_sample_2);
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
            
            setProjectName(data.audio.split("/")[2]?.replace("_final.mp3", "")); // extracts filename prefix

                // Add this block to correctly fetch audio through ngrok
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
    
    const handleGenerateVideo = async () => {
        setVideoGenerating(true);
        setVideoUrl(null);
    
        const formData = new FormData();
        formData.append("project_name", projectName);
    
        try {
            const response = await fetch(`${API_BASE}/generate_video`, {
                method: "POST",
                body: formData,
            });
    
            const data = await response.json();
    
            if (response.ok && data.video) {
                // Load via ngrok-safe fetch
                const videoResponse = await fetch(`${API_BASE}${data.video}`, {
                    headers: { 'ngrok-skip-browser-warning': 'true' }
                });
                const blob = await videoResponse.blob();
                setVideoUrl(URL.createObjectURL(blob));
            } else {
                throw new Error(data.error || "Video generation failed.");
            }
        } catch (err) {
            alert("❌ " + err.message);
        } finally {
            setVideoGenerating(false);
        }
    };    

    return (
        <div className="main-wrapper">
          <div className="app-container content">
            <header className="header">
              <a href="https://airc.woxsen.edu.in/" target="_blank" rel="noopener noreferrer">
                <img src={aircLogo} alt="AIRC Logo" className="logo-left" />
              </a>
              <a href="https://woxsen.edu.in" target="_blank" rel="noopener noreferrer">
                <img src={woxsenLogo} alt="Woxsen Logo" className="logo-right" />
              </a>
            </header>
      
            <div className="tile">
              <h1 className="title">AI Podcast Generator 🎙️</h1>
      
              <button className="info-button" onClick={() => setShowInfo(true)} title="How to use">
                <label>Info:</label> ℹ️
              </button>
      
              <div className="radio-group">
                <label>
                  <input type="radio" value="pdf" checked={inputType === "pdf"} onChange={() => setInputType("pdf")} /> Upload PDF
                </label>
                <label>
                  <input type="radio" value="topic" checked={inputType === "topic"} onChange={() => setInputType("topic")} /> Enter Topic
                </label>
              </div>
      
              {inputType === "pdf" ? (
                <input type="file" accept=".pdf" onChange={handleFileChange} className="input-field" />
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
                  <input type="checkbox" checked={useClonedVoice} onChange={toggleVoiceCloning} /> Enable Host 1 Voice Cloning
                </label>
                {useClonedVoice && (
                  <>
                    <input
                      type="text"
                      placeholder="Enter Host 1 Name (e.g. Vishal)"
                      onChange={(e) => setCustomHostName(e.target.value)}
                      className="input-field"
                    />
                    <input type="file" accept=".mp3" onChange={handleVoiceSampleChange} className="input-field" />
                  </>
                )}
              </div>

              <div className="music-selection">
                <label>
                    <input type="checkbox" checked={useClonedVoice2} onChange={() => setUseClonedVoice2(!useClonedVoice2)} />
                    Enable Host 2 Voice Cloning
                </label>
                {useClonedVoice2 && (
                    <>
                    <input
                        type="text"
                        placeholder="Enter Host 2 Name (e.g. Emy)"
                        onChange={(e) => setCustomHostName2(e.target.value)}
                        className="input-field"
                    />
                    <input type="file" accept=".mp3" onChange={(e) => setvoice_sample_2(e.target.files[0])} className="input-field" />
                    </>
                )}
                </div>

              <button onClick={handleSubmit} className="btn" disabled={loading}>
                {loading ? "Processing..." : "Generate Podcast 🎧"}
              </button>
      
              {loading && (
                <div className="progress-bar">
                  <div className="progress" style={{ width: `${progress}%` }}></div>
                </div>
              )}
      
              {audioUrl && (
                <>
                  <div className="audio-container">
                    <h2 className="audio-title">Generated Audio 🎧:</h2>
                    <audio controls className="audio-player">
                      <source src={audioUrl} type="audio/mpeg" />
                      Your browser does not support the audio element.
                    </audio>
                  </div>
      
                  <button className="btn" onClick={handleGenerateVideo} disabled={videoGenerating}>
                    {videoGenerating ? "Generating Video..." : "Generate Video 🎬"}
                  </button>
                </>
              )}
      
              {videoUrl && (
                <div className="audio-container">
                  <h2 className="audio-title">Generated Video 🎬:</h2>
                  <video controls width="100%" style={{ marginTop: "10px", borderRadius: "8px" }}>
                    <source src={videoUrl} type="video/mp4" />
                    Your browser does not support the video element.
                  </video>
                </div>
              )}
      
              {errorMessage && <div className="error-message">Error: {errorMessage}</div>}
            </div>
          </div>
      
          <footer className="footer">
            Developed by:{" "}
            <a href="https://www.linkedin.com/in/mastervishal/" target="_blank" rel="noopener noreferrer">
              Vishal Kumar Sharma
            </a>
            , {" "}
            <a href="https://www.linkedin.com/in/madhav-janumula-841b25253/" target="_blank" rel="noopener noreferrer">
                Madhav Janumula
            </a>
            &nbsp; - &nbsp;
            <a href="https://airc.woxsen.edu.in/" target="_blank" rel="noopener noreferrer">
              AI Research Centre
            </a>
          </footer>
      
          {showInfo && (
            <div className="modal-overlay" onClick={() => setShowInfo(false)}>
              <div className="modal-box" onClick={(e) => e.stopPropagation()}>
                <button className="close-button" onClick={() => setShowInfo(false)}>
                  ✖
                </button>
                <h2>
                  <u>How to Use AI Podcast Generator</u>
                </h2>
                <ul>
                  <li>📄 Upload a PDF file (only `.pdf`) or enter a topic manually</li>
                  <li>🎵 Select optional background music</li>
                  <li>🧬 Enable Voice Cloning (optional) by uploading your voice sample `.mp3` and your name</li>
                  <li>🎙 Click <strong>Generate Podcast</strong> and wait while your AI podcast is created</li>
                  <li>🎧 Listen to your final podcast below on popup music player</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      );      
};



export default App;

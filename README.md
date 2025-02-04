# AI Podcast Generator

The **AI Podcast Generator** is a web application that allows users to generate podcasts from uploaded PDF files or by providing a topic input. The generated content is processed using AI models for summarization, discussion generation, and text-to-speech conversion. Users can enhance their podcasts by integrating background music and (in-progress) voice cloning features.

---

## Features

### 🎛 Podcast Generation
- **PDF Upload**: Generate podcasts from uploaded PDF files by extracting and summarizing the content.
- **Topic Input**: Manually enter a topic, and the system will generate AI-driven podcast content.

### 🎵 Background Music Integration
- **Genre Selection**: Choose from various background music genres like **Jazz**, **Ambient**, and **Lo-Fi**.
- **Automatic Mixing**: The system overlays the selected music onto the podcast while balancing volume levels.

### 🎤 Voice Cloning (In Progress)
- **Custom Voice Generation**: Upload a voice sample to clone your voice and generate personalized podcasts.
- **Default AI Voices**: If no voice sample is provided, the podcast will use predefined AI voices (**Rahul** and **Kusum**).

---

## Technologies Used
- **Frontend**: React.js (App.jsx, index.css)
- **Backend**: FastAPI (main.py, tts.py, extract_text.py, summarize.py, discussion.py, db.py)
- **AI Models**:
  - **Text-to-Speech**: [TTS - xtts_v2](https://github.com/coqui-ai/TTS)
  - **Summarization**: `facebook/bart-large-cnn`
  - **Discussion Generation**: `llama3.1:8b`
- **Audio Processing**: gTTS, PyDub

---

## Installation & Setup

### 1. Clone the Repository
```
git clone https://github.com/Master229198112/ai_podcast_generator.git
cd ai_podcast_generator
```

### 2. Backend Setup
1. **Navigate to the backend folder**:
   ```
   cd backend
   ```

2. **Create a virtual environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   
   I have used conda to create env
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Start the FastAPI server**:
   ```
   uvicorn main:app --reload
   ```

---

### 3. Frontend Setup
1. **Navigate to the frontend folder**:
   ```
   cd frontend
   ```

2. **Install frontend dependencies**:
   ```
   npm install
   ```

3. **Start the React app**:
   ```
   npm run dev
   ```

---

## Project Structure
```
ai-podcast-generator/
├── backend/
│   ├── audio/                    # Generated podcast audio files
│   ├── background_music/         # Background music files (jazz.mp3, ambient.mp3, lofi.mp3)
│   ├── voice_clones/             # User voice samples for cloning (In Progress)
│   ├── extract_text.py           # Extract text from PDF or DOCX
│   ├── summarize.py              # Summarize extracted text
│   ├── discussion.py             # Generate AI discussions
│   ├── tts.py                    # Text-to-Speech with background music & voice cloning
│   ├── db.py                     # Save podcast metadata to database
│   ├── main.py                   # FastAPI server routes
│   └── requirements.txt          # Backend dependencies
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx               # React frontend with file upload, topic input, and music selection
│   │   └── index.css             # Styling for frontend UI
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── README.md                     # Project documentation
└── .gitignore
```

---

## Usage Instructions

1. **Open the application in your browser**:
   - The React frontend runs by default on `http://localhost:3000`.

2. **Generate a Podcast**:
   - **Option 1: Upload PDF**
     1. Click on "Upload PDF".
     2. Choose a `.pdf` file from your system.
     3. Select background music (optional).
     4. Click "Generate Podcast".
   
   - **Option 2: Enter Topic**
     1. Click on "Enter Topic".
     2. Type in your desired topic (e.g., "Future of Artificial Intelligence").
     3. Select background music (optional).
     4. Click "Generate Podcast".

3. **Enable Voice Cloning (Optional)**:
   - Check the "Enable Voice Cloning" box.
   - Upload a **voice sample** (1-3 minutes, `.wav` or `.mp3`).

4. **Listen to Your Podcast**:
   - After processing, the generated podcast will appear with an **audio player**.
   - You can **download** the podcast or listen to it directly from the app.

---

## Contributing

1. **Fork** this repository.
2. **Create a branch** (`git checkout -b feature-branch`).
3. **Commit your changes** (`git commit -m 'Add new feature'`).
4. **Push to the branch** (`git push origin feature-branch`).
5. **Open a Pull Request**.

---

## Future Features (Planned)
- **Multi-Language Support**: Automatic detection and manual selection of podcast language.
- **Custom Intros/Outros**: Let users personalize the beginning and end of their podcasts.
- **Transcript Generation**: Display and download full podcast transcripts in PDF format.
- **Sentiment-Based Generation**: Allow users to select the tone of the podcast (informative, humorous, formal).

---

## License
This project is licensed under the **AIRC**.

---

## Contact
For any questions or contributions, feel free to reach out:
- **Email**: vishalkumar.sharma37@gmail.com
- **GitHub**: [Master229198112](https://github.com/Master229198112)

Happy Podcasting! 🎤🌟


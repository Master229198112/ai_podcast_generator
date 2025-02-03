from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from extract_text import extract_text
from summarize import summarize_text
from discussion import generate_discussion
from tts import generate_combined_audio
from db import save_podcast
import os

app = FastAPI()

# ✅ Add CORS support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change as needed)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Ensure the 'audio' directory exists to store generated audio files
STATIC_DIR = "audio"
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/audio", StaticFiles(directory=STATIC_DIR), name="audio")


# ✅ Upload & Process PDF File
@app.post("/upload")
async def upload_document(file: UploadFile = File(...), background_music: str = Form("none")):
    try:
        # Read file content
        content = await file.read()
        text = extract_text(content, file.filename)
        print(f"\n✅ Extracted Text: {text[:500]}...")  # Debug print (first 500 chars)

        # Check if text extraction was successful
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text extracted from the file.")

        summary = summarize_text(text)
        print(f"\n✅ Generated Summary: {summary}")  # Debug print

        discussion = generate_discussion(summary)
        print(f"\n✅ Generated Discussion: {discussion}")  # Debug print

        # Generate audio in alternating host voices with selected background music
        audio_file = generate_combined_audio(discussion, file.filename, background_music)

        # Ensure audio file is created
        if not os.path.exists(audio_file):
            raise HTTPException(status_code=500, detail="Failed to generate audio.")

        print(f"\n✅ Generated Audio File: {audio_file}")  # Debug print

        # Save to database (optional)
        podcast_id = save_podcast(file.filename, summary, audio_file)

        # Response JSON
        response_data = {
            "message": "Podcast Created from PDF!",
            "podcast_id": podcast_id,
            "audio": f"/audio/{os.path.basename(audio_file)}"
        }

        print(f"\n✅ Response Data: {response_data}")  # Debug print
        return JSONResponse(content=response_data, status_code=200)

    except HTTPException as e:
        print(f"\n❌ HTTP Error: {str(e)}")  # Debug print
        return JSONResponse(content={"error": str(e.detail)}, status_code=e.status_code)

    except Exception as e:
        print(f"\n❌ Unexpected Error: {str(e)}")  # Debug print
        return JSONResponse(content={"error": "An internal error occurred."}, status_code=500)


# ✅ Generate Podcast from Topic Input
@app.post("/generate")
async def generate_podcast(topic: str = Form(...), background_music: str = Form("none")):
    try:
        print(f"\n✅ Received Topic: {topic}")  # Debug print

        summary = summarize_text(topic)
        print(f"\n✅ Generated Summary: {summary}")  # Debug print

        discussion = generate_discussion(summary)
        print(f"\n✅ Generated Discussion: {discussion}")  # Debug print

        # Generate an audio file based on topic with selected background music
        filename = f"podcast_{topic.replace(' ', '_')}.mp3"
        audio_file = generate_combined_audio(discussion, filename, background_music)

        # Ensure audio file is created
        if not os.path.exists(audio_file):
            raise HTTPException(status_code=500, detail="Failed to generate audio.")

        print(f"\n✅ Generated Audio File: {audio_file}")  # Debug print

        # Save to database (optional)
        podcast_id = save_podcast(topic, summary, audio_file)

        # Response JSON
        response_data = {
            "message": "Podcast Created from Topic!",
            "podcast_id": podcast_id,
            "audio": f"/audio/{os.path.basename(audio_file)}"
        }

        print(f"\n✅ Response Data: {response_data}")  # Debug print
        return JSONResponse(content=response_data, status_code=200)

    except HTTPException as e:
        print(f"\n❌ HTTP Error: {str(e)}")  # Debug print
        return JSONResponse(content={"error": str(e.detail)}, status_code=e.status_code)

    except Exception as e:
        print(f"\n❌ Unexpected Error: {str(e)}")  # Debug print
        return JSONResponse(content={"error": "An internal error occurred."}, status_code=500)

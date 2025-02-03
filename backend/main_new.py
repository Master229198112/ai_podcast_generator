from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from extract_text import extract_text
from summarize import summarize_text
from discussion import generate_discussion
from tts import generate_combined_audio
from db import save_podcast
import os


app = FastAPI()

# Ensure the 'audio' directory exists to store generated audio files
STATIC_DIR = "audio"
os.makedirs(STATIC_DIR, exist_ok=True)

app.mount("/audio", StaticFiles(directory=STATIC_DIR), name="audio")

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        # Read file content
        content = await file.read()
        text = extract_text(content, file.filename)
        print(f"\n✅ Extracted Text: {text[:500]}...")  # Debug print (first 500 chars)

        summary = summarize_text(text)
        print(f"\n✅ Generated Summary: {summary}")  # Debug print

        discussion = generate_discussion(summary)
        print(f"\n✅ Generated Discussion: {discussion}")  # Debug print

        # Generate single-file alternating conversation audio
        audio_file = generate_combined_audio(discussion, file.filename)
        
        if not os.path.exists(audio_file):
            raise HTTPException(status_code=500, detail="Failed to generate audio.")

        print(f"\n✅ Generated Audio File: {audio_file}")  # Debug print

        podcast_id = save_podcast(file.filename, summary, audio_file)
        
        response_data = {
            "message": "Podcast Created!",
            "podcast_id": podcast_id,
            "audio": f"/audio/{os.path.basename(audio_file)}"
        }
        
        print(f"\n✅ Response Data: {response_data}")  # Debug print
        return JSONResponse(content=response_data, status_code=200)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")  # Debug print
        raise HTTPException(status_code=500, detail=str(e))

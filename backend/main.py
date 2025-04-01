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

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://ai-podcast-generator-zeta.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve audio files
STATIC_DIR = "audio"
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/audio", StaticFiles(directory=STATIC_DIR), name="audio")


@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    background_music: str = Form("none"),
    voice_sample: UploadFile = File(None),
    host_name: str = Form("Rahul")
):
    try:
        cloned_voice_path = None
        if voice_sample:
            cloned_voice_path = os.path.join(STATIC_DIR, voice_sample.filename)
            with open(cloned_voice_path, "wb") as f:
                f.write(await voice_sample.read())
            print(f"✅ Voice sample saved at: {cloned_voice_path}")

        content = await file.read()
        text = extract_text(content, file.filename)
        print(f"\n✅ Extracted Text: {text[:500]}...")  # shows first 500 characters
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text extracted from the file.")

        summary = summarize_text(text)
        print(f"\n✅ Generated Summary: {summary}")
        discussion = generate_discussion(summary, host_name)
        print(f"\n✅ Generated Discussion:\n{discussion}")

        audio_file = generate_combined_audio(
            discussion,
            file.filename,
            background_music_genre=background_music,
            cloned_voice_path=cloned_voice_path,
            host_name=host_name
        )
        print(f"\n✅ Generated Audio File: {audio_file}")


        if not os.path.exists(audio_file):
            raise HTTPException(status_code=500, detail="Failed to generate audio.")

        podcast_id = save_podcast(file.filename, summary, audio_file)

        return JSONResponse(
            content={
                "message": "Podcast Created from PDF!",
                "podcast_id": podcast_id,
                "audio": f"/audio/{os.path.basename(audio_file)}"
            },
            status_code=200
        )

    except HTTPException as e:
        return JSONResponse(content={"error": str(e.detail)}, status_code=e.status_code)
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        return JSONResponse(content={"error": "An internal error occurred."}, status_code=500)


@app.post("/generate")
async def generate_podcast(
    topic: str = Form(...),
    background_music: str = Form("none"),
    voice_sample: UploadFile = File(None),
    host_name: str = Form("Rahul")
):
    try:
        print(f"✅ Received Topic: {topic}")

        cloned_voice_path = None
        if voice_sample:
            cloned_voice_path = os.path.join(STATIC_DIR, voice_sample.filename)
            with open(cloned_voice_path, "wb") as f:
                f.write(await voice_sample.read())
            print(f"✅ Voice sample saved at: {cloned_voice_path}")

        summary = summarize_text(topic)
        print(f"\n✅ Generated Summary: {summary}")
        discussion = generate_discussion(summary, host_name)
        print(f"\n✅ Generated Discussion:\n{discussion}")

        filename = f"podcast_{topic.replace(' ', '_')}.mp3"
        audio_file = generate_combined_audio(
            discussion,
            filename,
            background_music_genre=background_music,
            cloned_voice_path=cloned_voice_path,
            host_name=host_name
        )
        print(f"\n✅ Generated Audio File: {audio_file}")

        if not os.path.exists(audio_file):
            raise HTTPException(status_code=500, detail="Failed to generate audio.")

        podcast_id = save_podcast(topic, summary, audio_file)

        return JSONResponse(
            content={
                "message": "Podcast Created from Topic!",
                "podcast_id": podcast_id,
                "audio": f"/audio/{os.path.basename(audio_file)}"
            },
            status_code=200
        )

    except HTTPException as e:
        return JSONResponse(content={"error": str(e.detail)}, status_code=e.status_code)
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        return JSONResponse(content={"error": "An internal error occurred."}, status_code=500)

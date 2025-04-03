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
from video_generator.video_generator import generate_video

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://ai-podcast-generator-zeta.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = "audio"
os.makedirs(STATIC_DIR, exist_ok=True)
app.mount("/audio", StaticFiles(directory=STATIC_DIR), name="audio")
app.mount("/podcast", StaticFiles(directory="Podcast"), name="podcast")

# ✅ Common helper for saving voice samples
def save_voice_sample(uploaded_file: UploadFile) -> str:
    if not uploaded_file:
        return None
    path = os.path.join(STATIC_DIR, uploaded_file.filename)
    with open(path, "wb") as f:
        f.write(uploaded_file.file.read())
    print(f"✅ Voice sample saved at: {path}")
    return path

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    background_music: str = Form("none"),
    voice_sample: UploadFile = File(None),
    host_name: str = Form("Rahul"),
    voice_sample_2: UploadFile = File(None),
    host_name_2: str = Form("Emy")
):
    try:
        # cloned_voice_path_1 = save_voice_sample(voice_sample)
        # cloned_voice_path_2 = save_voice_sample(voice_sample_2)

        # content = await file.read()
        # text = extract_text(content, file.filename)
        # print(f"\n✅ Extracted Text: {text[:500]}...")  # shows first 500 characters
        # if not text.strip():
        #     raise HTTPException(status_code=400, detail="No text extracted from the file.")
        # summary = summarize_text(text)
        # print(f"\n✅ Generated Summary: {summary}")
        # discussion = generate_discussion(summary, host_name, host_name_2)
        # print(f"\n✅ Generated Discussion:\n{discussion}")
        cloned_voice_path = None
        cloned_voice_path_2 = None

        if voice_sample:
            cloned_voice_path = os.path.join(STATIC_DIR, voice_sample.filename)
            with open(cloned_voice_path, "wb") as f:
                f.write(await voice_sample.read())
            print(f"✅ Voice sample saved at: {cloned_voice_path}")

        if voice_sample_2:
            cloned_voice_path_2 = os.path.join(STATIC_DIR, voice_sample_2.filename)
            with open(cloned_voice_path_2, "wb") as f:
                f.write(await voice_sample_2.read())
            print(f"✅ Voice sample 2 saved at: {cloned_voice_path_2}")

        content = await file.read()
        text = extract_text(content, file.filename)
        print(f"\n✅ Extracted Text: {text[:500]}...")  # shows first 500 characters
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text extracted from the file.")
        summary = summarize_text(text)
        print(f"\n✅ Generated Summary: {summary}")
        discussion = generate_discussion(summary, host_name, host_name_2)
        print(f"\n✅ Generated Discussion:\n{discussion}")

        audio_file = generate_combined_audio(
            discussion,
            file.filename,
            background_music_genre=background_music,
            cloned_voice_path=cloned_voice_path,
            cloned_voice_path_2=cloned_voice_path_2,
            host_name=host_name,
            host_name_2=host_name_2
        )

        print(f"\n✅ Generated Audio File: {audio_file}")

        if not os.path.exists(audio_file):
            raise HTTPException(status_code=500, detail="Failed to generate audio.")

        podcast_id = save_podcast(file.filename, summary, audio_file)
        project_name = os.path.basename(audio_file).replace("_final.mp3", "")
        return JSONResponse(
            content={
                "message": "Podcast Created from PDF!",
                "podcast_id": podcast_id,
                "project_name": project_name,
                "audio": f"/podcast/{project_name}/{project_name}_final.mp3"
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
    host_name: str = Form("Rahul"),
    voice_sample_2: UploadFile = File(None),
    host_name_2: str = Form("Emy")
):
    try:
        print(f"✅ Received Topic: {topic}")
        cloned_voice_path_1 = save_voice_sample(voice_sample)
        cloned_voice_path_2 = save_voice_sample(voice_sample_2)


        summary = summarize_text(topic)
        discussion = generate_discussion(summary, host_name, host_name_2)

        filename = f"podcast_{topic.replace(' ', '_')}.mp3"
        audio_file = generate_combined_audio(
            discussion,
            filename,
            background_music_genre=background_music,
            cloned_voice_path=cloned_voice_path_1,
            host_name=host_name,
            cloned_voice_path_2=cloned_voice_path_2,
            host_name_2=host_name_2
        )

        if not os.path.exists(audio_file):
            raise HTTPException(status_code=500, detail="Failed to generate audio.")

        podcast_id = save_podcast(topic, summary, audio_file)
        project_name = os.path.basename(audio_file).replace("_final.mp3", "")
        return JSONResponse(
            content={
                "message": "Podcast Created from Topic!",
                "podcast_id": podcast_id,
                "project_name": project_name,
                "audio": f"/podcast/{project_name}/{project_name}_final.mp3"
            },
            status_code=200
        )

    except HTTPException as e:
        return JSONResponse(content={"error": str(e.detail)}, status_code=e.status_code)
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        return JSONResponse(content={"error": "An internal error occurred."}, status_code=500)

@app.post("/generate_video")
async def generate_video_api(project_name: str = Form(...)):
    try:
        output_path = generate_video(project_name)
        return JSONResponse(
            content={
                "message": "Video generated successfully.",
                "video": f"/podcast/{project_name}/{os.path.basename(output_path)}"
            },
            status_code=200
        )
    except Exception as e:
        print(f"❌ Error during video generation: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

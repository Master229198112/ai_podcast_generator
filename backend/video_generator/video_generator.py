import os
import json
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def generate_video(project_name: str, base_dir="Podcast"):
    folder_path = os.path.join(base_dir, project_name)
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"No such project folder: {folder_path}")

    # Load JSON
    json_path = next((f for f in os.listdir(folder_path) if f.endswith("_segments.json")), None)
    if not json_path:
        raise FileNotFoundError("No *_segments.json found.")
    with open(os.path.join(folder_path, json_path)) as f:
        segments = json.load(f)

    # Load final audio
    audio_path = next((f for f in os.listdir(folder_path) if f.endswith("_final.mp3")), None)
    if not audio_path:
        raise FileNotFoundError("No *_final.mp3 found.")
    audio_clip = AudioFileClip(os.path.join(folder_path, audio_path))

    # Load speaker loop clips
    base = os.path.dirname(__file__)
    rahul_clip = VideoFileClip(os.path.join(base, "Rahul.mp4"))
    emy_clip = VideoFileClip(os.path.join(base, "Emy.mp4"))

    def loop_video(clip, duration):
        looped = concatenate_videoclips([clip] * (int(duration // clip.duration) + 1))
        return looped.subclip(0, duration)

    final_clips = []
    for seg in segments:
        speaker = seg["speaker"]
        duration = seg["end"] - seg["start"]
        base_clip = rahul_clip if speaker == "Rahul" else emy_clip
        final_clips.append(loop_video(base_clip, duration))

    video = concatenate_videoclips(final_clips).set_audio(audio_clip)
    output_path = os.path.join(folder_path, f"{project_name}_final_video.mp4")
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    return output_path

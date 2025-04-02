import os
import json
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

# Setup paths
BASE_DIR = os.path.dirname(__file__)
AUDIO_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "audio"))
OUTPUT_VIDEO = os.path.join(BASE_DIR, "stitched_podcast_video.mp4")

# Load timestamped segment metadata
segment_json = next((f for f in os.listdir(AUDIO_DIR) if f.endswith("_segments.json")), None)
if not segment_json:
    raise FileNotFoundError("No *_segments.json file found in audio folder.")

with open(os.path.join(AUDIO_DIR, segment_json), "r") as f:
    segments = json.load(f)

# Load final podcast audio
final_audio_file = next((f for f in os.listdir(AUDIO_DIR) if f.endswith("_final.mp3")), None)
if not final_audio_file:
    raise FileNotFoundError("No *_final.mp3 file found in audio folder.")

final_audio_path = os.path.join(AUDIO_DIR, final_audio_file)
audio_clip = AudioFileClip(final_audio_path)
total_audio_duration = audio_clip.duration

# Load Rahul and Emy video loops
rahul_clip = VideoFileClip(os.path.join(BASE_DIR, "Rahul.mp4"))
emy_clip = VideoFileClip(os.path.join(BASE_DIR, "Emy.mp4"))

def loop_video_to_duration(base_clip, duration):
    loop_count = int(duration // base_clip.duration) + 1
    looped = concatenate_videoclips([base_clip] * loop_count)
    return looped.subclip(0, duration)

# Build video segments based on speaker and timestamp durations
final_clips = []
for seg in segments:
    speaker = seg["speaker"]
    start = seg["start"]
    end = seg["end"]
    duration = end - start

    clip = rahul_clip if speaker == "Rahul" else emy_clip
    video_piece = loop_video_to_duration(clip, duration)
    final_clips.append(video_piece)

# Concatenate all speaker clips
stitched_video = concatenate_videoclips(final_clips)
stitched_video = stitched_video.set_audio(audio_clip)

# Export
stitched_video.write_videofile(OUTPUT_VIDEO, codec="libx264", audio_codec="aac")

print(f"✅ Final video with audio saved at: {OUTPUT_VIDEO}")

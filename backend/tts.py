import os
import re
import time
from pydub import AudioSegment
from TTS.api import TTS
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

AUDIO_DIR = "audio"
BACKGROUND_MUSIC_DIR = "background_music"
os.makedirs(AUDIO_DIR, exist_ok=True)

tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")
tts.to(device)

def clean_text(text, host_name="Rahul"):
    return re.sub(rf"{host_name}:|Emy:", "", text, flags=re.IGNORECASE).strip()

def text_to_speech(text, filename, voice_index, cloned_voice_path=None, host_name="Rahul"):
    text = clean_text(text, host_name)
    if not text.strip():
        print(f"⚠️ Skipping empty text for {filename}")
        return None

    audio_path = os.path.join(AUDIO_DIR, filename)
    print(f"🔄 Generating speech for: {filename}")

    try:
        if voice_index == "Host1" and cloned_voice_path:
            print(f"🎙️ Using cloned voice from: {cloned_voice_path}")
            tts.tts_to_file(
                text=text,
                speaker_wav=cloned_voice_path,
                language="en",
                file_path=audio_path
            )
        else:
            valid_voice = "Damien Black" if voice_index == "Host1" else voice_index
            tts.tts_to_file(
                text=text,
                speaker=valid_voice,
                language="en",
                file_path=audio_path
            )

        wait_time = 0
        while not os.path.exists(audio_path):
            if wait_time > 10:
                print(f"❌ Error: File {audio_path} not created after 10s")
                return None
            time.sleep(1)
            wait_time += 1

        print(f"✅ Speech generated: {audio_path}")
        return audio_path
    except Exception as e:
        print(f"⚠️ Error during TTS processing: {e}")
        return None

def add_background_music(speech_audio, background_music_genre, output_filename):
    try:
        speech = AudioSegment.from_file(speech_audio)

        if background_music_genre != "none":
            bg_music_path = os.path.join(BACKGROUND_MUSIC_DIR, f"{background_music_genre}.mp3")
            if os.path.exists(bg_music_path):
                background = AudioSegment.from_file(bg_music_path) - 20

                if len(background) < len(speech):
                    background *= (len(speech) // len(background)) + 1

                combined = speech.overlay(background[:len(speech)])
            else:
                print(f"❌ Background music not found: {bg_music_path}")
                combined = speech
        else:
            combined = speech

        combined.export(output_filename, format="mp3")
        print(f"✅ Final audio with background music saved: {output_filename}")
        return output_filename
    except Exception as e:
        print(f"❌ Error adding background music: {e}")
        return speech_audio

def combine_audio_files(temp_audio_files, output_filename="audio/combined_audio.mp3", background_music_genre="none"):
    if not temp_audio_files:
        print("❌ No audio files to combine.")
        return None

    try:
        combined = AudioSegment.from_file(temp_audio_files[0])
        for audio_file in temp_audio_files[1:]:
            combined += AudioSegment.from_file(audio_file)

        combined.export(output_filename, format="mp3")
        print(f"✅ Combined audio saved as: {output_filename}")

        return add_background_music(output_filename, background_music_genre, output_filename)
    except Exception as e:
        print(f"❌ Error during audio combination: {e}")
        return None

def generate_combined_audio(conversation_text, filename_prefix, background_music_genre="none", cloned_voice_path=None, host_name="Rahul"):
    safe_prefix = re.sub(r'[\\/*?:"<>|]', '', filename_prefix)
    final_audio_path = os.path.join(AUDIO_DIR, f"{safe_prefix}_final.mp3")
    temp_audio_files = []

    if not host_name.strip():
        host_name = "Rahul"

    # conversation_text = re.sub(r'Rahul:', f'{host_name}:', conversation_text)
    # Normalize speaker names to remove formatting like "**Rahul:**"
    conversation_text = re.sub(r"\*\*(\w+):\*\*", r"\1:", conversation_text)  # Remove markdown bold
    conversation_text = re.sub(r'Rahul:', f'{host_name}:', conversation_text)  # Replace default host name

    # dialogue_lines = re.findall(rf'({host_name}|Emy):\s*(.*?)(?=\n({host_name}|Emy):|\Z)', conversation_text, re.DOTALL)
    dialogue_lines = re.findall(rf'({host_name}|Emy):\s*(.*?)(?=\n(?:{host_name}|Emy):|\Z)', conversation_text, re.DOTALL)


    if not dialogue_lines:
        print("❌ Error: No dialogues detected in the conversation.")
        return None

    for i, (speaker, line) in enumerate(dialogue_lines):
        if not line.strip():
            continue

        if speaker == host_name:
            voice_index = "Host1" if cloned_voice_path else "Damien Black"
        else:
            voice_index = "Claribel Dervla"

        audio_filename = f"{filename_prefix}_part_{i}.mp3"
        speech_file = text_to_speech(line, audio_filename, voice_index, cloned_voice_path, host_name)

        if speech_file:
            temp_audio_files.append(speech_file)

    if not temp_audio_files:
        print("❌ Error: No audio files generated.")
        return None

    return combine_audio_files(temp_audio_files, final_audio_path, background_music_genre)

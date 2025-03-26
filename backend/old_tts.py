from gtts import gTTS
import os
import re
import pyttsx3
import time
from pydub import AudioSegment
from TTS.api import TTS
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

# Ensure 'audio/' directory exists for storing generated audio
AUDIO_DIR = "audio"
BACKGROUND_MUSIC_DIR = "background_music"  # Directory for background music tracks
os.makedirs(AUDIO_DIR, exist_ok=True)

tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")
tts.to(device)

def clean_text(text):
    """
    Remove * symbols and host names (Rahul: and Kusum:)
    """
    text = re.sub(r"Rahul:|Kusum:", "", text, flags=re.IGNORECASE)
    return text.strip()

def create_attention_mask(text):
    """
    Use the model's tokenizer to create an attention mask that aligns with tokenized input.
    """
    # Use the TTS model's internal tokenizer
    tokenized = tts.tokenizer(text)
    
    # Create attention mask based on the number of tokens
    attention_mask = [1] * len(tokenized["input_ids"])
    
    return torch.tensor(attention_mask).unsqueeze(0), tokenized["input_ids"]

def text_to_speech(text, filename, voice_index, cloned_voice_path=None):
    """
    Convert text to speech using TTS and save as an audio file.
    """
    text = clean_text(text)

    if not text.strip():
        print(f"⚠️ Skipping empty text for {filename}")
        return None

    audio_path = os.path.join(AUDIO_DIR, filename)
    print(f"🔄 Generating speech for: {filename}")

    try:
        if cloned_voice_path:
            print(f"🎙️ Using cloned voice from: {cloned_voice_path}")
            tts.tts_to_file(
                text=text,
                speaker_wav=cloned_voice_path,
                language="en",
                file_path=audio_path
            )
        else:
            tts.tts_to_file(
                text=text,
                speaker=voice_index,
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
    """
    Overlay selected background music onto the generated podcast audio.
    """
    try:
        speech = AudioSegment.from_file(speech_audio)

        if background_music_genre != "none":
            bg_music_path = os.path.join(BACKGROUND_MUSIC_DIR, f"{background_music_genre}.mp3")
            if os.path.exists(bg_music_path):
                background = AudioSegment.from_file(bg_music_path)
                background = background - 20  # Reduce background music volume

                if len(background) < len(speech):
                    repeat_count = (len(speech) // len(background)) + 1
                    background = background * repeat_count

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
    """
    Combine multiple audio files into one final audio file with optional background music.
    """
    if not temp_audio_files:
        print("❌ No audio files to combine.")
        return None

    temp_audio_files = [os.path.normpath(file) for file in temp_audio_files]

    try:
        combined = AudioSegment.from_file(temp_audio_files[0])
        for audio_file in temp_audio_files[1:]:
            sound = AudioSegment.from_file(audio_file)
            combined += sound

        combined_audio_path = os.path.join(AUDIO_DIR, os.path.basename(output_filename))  

        combined.export(combined_audio_path, format="mp3")
        print(f"✅ Combined audio saved as: {combined_audio_path}")

        # Add background music if selected
        final_audio_with_music = add_background_music(combined_audio_path, background_music_genre, combined_audio_path)

        return final_audio_with_music
    except Exception as e:
        print(f"❌ Error during audio combination: {e}")
        return None

def generate_combined_audio(conversation_text, filename_prefix, background_music_genre="none", cloned_voice_path=None):
    """
    Generate individual speech files for each dialogue turn and combine them into one file.
    If cloned_voice_path is provided, use it for voice cloning.
    """
    final_audio_path = os.path.join(AUDIO_DIR, f"{filename_prefix}_final.mp3")
    temp_audio_files = []

    # dialogue_lines = re.findall(r'(Rahul|Kusum):\\s*(.*?)(?=\\n(Rahul|Kusum):|\\Z)', conversation_text, re.DOTALL)
    dialogue_lines = re.findall(r'\*\*(Rahul|Kusum):\*\*(.*?)(?=\n\*\*(Rahul|Kusum):|\Z)', conversation_text, re.DOTALL)
    
    if not dialogue_lines:
        print("❌ Error: No dialogues detected in the conversation.")
        return None

    for i, (speaker, line, _) in enumerate(dialogue_lines):
        if not line.strip():
            continue

        voice_index = "Damien Black" if speaker == "Rahul" else "Claribel Dervla"
        audio_filename = f"{filename_prefix}_part_{i}.mp3"

        # Use cloned voice if provided, otherwise use default voice
        speech_file = text_to_speech(line, audio_filename, voice_index, cloned_voice_path=cloned_voice_path)

        if speech_file:
            temp_audio_files.append(speech_file)

    if not temp_audio_files:
        print("❌ Error: No audio files generated.")
        return None

    final_audio_path = combine_audio_files(temp_audio_files, final_audio_path, background_music_genre)

    return final_audio_path

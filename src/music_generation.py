import sys
import json
import requests
from pydub import AudioSegment
import io
import os
from dotenv import load_dotenv
import random

load_dotenv()

ELEVEN_LABS_API_KEY = os.getenv('ELEVEN_LABS_API_KEY')


def generate_lyrics(theme, mood):
    # Use OpenAI to generate lyrics based on the theme and mood
    # This is a placeholder. In a real implementation, you'd make an API call to OpenAI here.
    return f'''This is a {mood} song about {theme}\nThe colors swirl and dance\nIn a rhythm of chance\nEchoes of 
emotion in every glance'''


def generate_melody(mood):
    # This is a simplified melody generation.
    # In a real implementation, you'd use a more sophisticated music generation algorithm.
    base_notes = {
        "happy": ["C4", "E4", "G4", "A4"],
        "sad": ["A3", "C4", "E4", "G4"],
        "energetic": ["D4", "F#4", "A4", "C5"],
        "calm": ["G3", "B3", "D4", "F4"]
    }
    notes = base_notes.get(mood, ["C4", "D4", "E4", "F4", "G4", "A4", "B4"])
    return " ".join(random.choices(notes, k=16))  # Generate a 16-note melody


def text_to_speech(text, voice_id="21m00Tcm4TlvDq8ikWAM"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_LABS_API_KEY
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return AudioSegment.from_mp3(io.BytesIO(response.content))
    else:
        print(f"Error: {response.status_code}")
        return None


def generate_music(lyrics, melody):
    url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_LABS_API_KEY
    }

    data = {
        "text": lyrics,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        return AudioSegment.from_mp3(io.BytesIO(response.content))
    else:
        print(f"Error: {response.status_code}")
        return None


def create_song(theme, mood):
    lyrics = generate_lyrics(theme, mood)
    melody = generate_melody(mood)

    # Generate vocal track
    vocal_track = text_to_speech(lyrics)

    # Generate a simple backing track (this is a placeholder)
    backing_track = AudioSegment.silent(duration=30000)  # 30 seconds of silence

    # Combine vocal track and backing track
    if vocal_track:
        combined = backing_track.overlay(vocal_track)

        # Trim to 30 seconds
        combined = combined[:30000]

        output_path = "generated_song.mp3"
        combined.export(output_path, format="mp3")
        return output_path, lyrics
    else:
        return None, lyrics


if __name__ == "__main__":
    # input_data = json.loads(sys.argv[1])
    # theme = input_data['theme']
    # mood = input_data['mood']
    # output_path, lyrics = create_song(theme, mood)
    # if output_path:
    #     print(json.dumps({"output": output_path, "lyrics": lyrics}))
    # else:
    #     print(json.dumps({"error": "Failed to generate music"}))
    print(generate_lyrics("nature", "peace"))

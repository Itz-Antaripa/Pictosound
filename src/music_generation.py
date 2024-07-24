import sys
import json
import requests
from pydub import AudioSegment
import io
import os
from dotenv import load_dotenv
import random
from openai import OpenAI

client = OpenAI()

load_dotenv()

ELEVEN_LABS_API_KEY = os.getenv('ELEVEN_LABS_API_KEY')


def generate_lyrics(theme, mood, instrument, description):
    
    conversation = [
        {
            "role": "system",
            "content": '''You are a world famous musician and art enthusiast. You will be given with theme, mood, instrument, and description.
Based on that you need to generate lyrics for 30 sec music along with base notes. Utilize the theme, mood and instrument provided.
Return the output in json format:
{
    "lyrics": "theme that explains the visual art",
    "base_notes": [base notes of the 30 sec music in list],
}
'''
        },
        {
            "role": "user", 
            "content": "Understand the theme, mood, instrument, description and generate the lyrics and base_notes accordingly. Return in json format."
        },
    ]
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            temperature=0.5,
            top_p=1
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


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
    payload = {
        "theme": "Abstract Geometric Expression",
        "mood": "Vibrant and Dynamic",
        "instrument": "Electric Guitar",
        "description": "This artwork features a striking array of geometric shapes and vivid colors, forming an abstract composition. It appears to incorporate stylized human and possibly natural forms, interwoven with patterns and lines that suggest movement and energy. The use of bright colors such as orange, blue, and pink adds to the vibrant and dynamic feel of the piece. The complexity and the boldness of the work convey a sense of intensity and liveliness."
    }
    print(generate_lyrics(payload['theme'], 
                          payload['mood'], 
                          payload['instrument'], 
                          payload['description']))

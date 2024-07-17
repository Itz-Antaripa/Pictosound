import base64
import requests
import sys
import json
import os
from dotenv import load_dotenv
import random

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')



def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def get_image_analyze(image_path):
    base64_image = encode_image(image_path)

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    conversation = [
        {
            "role": "system",
            "content": '''You are a world famous artist and art enthusiast. Given an image of a visual art, you need analyze and understand the image.
    Get the deeper understanding of the art and think about what theme, mood and instrument will be perfectly able to describe the picture if we had to convert that to music.
    Return the output in json format:
    {
        "theme": "theme that explains the visual art",
        "mood": "mood that depicts the visual art",
        "instrument": "the instrument that can describe the visual art in music",
        "description": "Explain the image in brief"
    }
    '''
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "Undertstand the visual art image and return the output in json format."
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ]

    payload = {
    "model": "gpt-4o",
    "messages": conversation,
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    response_data = response.json()
    return response_data['choices'][0]['message']['content']

print(get_image_analyze('visual_image.jpeg'))

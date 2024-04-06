import requests
from PIL import Image
import base64
import os
import pandas as pd

api_key = os.getenv('OPENAI_API_KEY')
org = os.getenv("OPENAI_ORG")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
        
def main():

    airport_data = []

    image_path = 'images/or/S39.png'

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "OpenAI-Organization": org
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": 'Extract information from the pages. I need the 3 letter airport identifier (usually near the top left), the airport name, whether there is mention of a Courtesy Car, mention of Bikes or Bicycles, mention of Camping or Campgrounds, and mention of Food (but only yes to food if options are within 1 mile or on the field). Output should be in this csv format: Airport Identifier,Airport Name,Courtesy Car,Bicycles,Camping,Meals. For example: S33,MADRAS MUNICIPAL,Yes,No,No,Yes'
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    #import pdb
    #pdb.set_trace()

    resp = response.json()
    data = resp.get('choices')[0].get('message').get('content')
    airport_data.append(data)

    df = pd.DataFrame(airport_data)
    print(df)

    out = 'chatgpt.csv'
    df.to_csv(out, index=False)
    print(f"Data saved to {out}")



if __name__ == '__main__':
    main()

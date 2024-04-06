import pdfplumber
import pandas as pd
import requests
import os
import json
import base64
from pdf2image import convert_from_path
from PIL import Image

'''
About 1579 tokens or ~$0.018 per image

python -m venv env
source env/bin/activate
pip install -r requirements.txt
pip3 install --upgrade openai

export OPENAI_API_KEY='your-api-key-here'
export OPENAI_ORG='your org'

'''

or_url = '' 

airports_url = 'https://davidmegginson.github.io/ourairports-data/airports.csv'
airports_path = 'data/airports.csv'

api_key = os.getenv('OPENAI_API_KEY')
org = os.getenv("OPENAI_ORG")

def extract_page_info(page, text, state):
    os.system('magick mogrify -colorspace gray images/or/tmp.png')

    image_path = f"images/{state}/tmp.png"
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
            "text": 'I need information from this public airport directory page with public information. I need the 3 letter airport identifier (usually near the top left), the airport name, whether there is mention of a Courtesy Car, mention of Bikes or Bicycles, mention of Camping or Campgrounds, and mention of Food (but only yes to food if options are within 1 mile or on the field). Output should only be in this csv format and nothing else: {"Airport Identifier": "","Airport Name": "","Courtesy Car": "","Bicycles": "","Camping": "","Meals": ""}'
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

    print("Uploading image...")
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    #import pdb
    #pdb.set_trace()

    resp = response.json()
    print(resp)
    data = resp.get('choices')[0].get('message').get('content')
    if "Airport Name" not in data:
        print("error")
        return {'Airport Identifier': '', 'Airport Name': '', 'Courtesy Car': '', 'Bicycles': '', 'Camping': '', 'Meals': ''}
    
    data = json.loads(data)
    print(data)
    return data

def parse_state(airport_data, state, directory_url, method, start_page, end_page):
    pdf = f'directories/{state}.pdf'
    out = f'data/airport_info_{state}.csv'
    imgDir = f'images/{state}/'

    # dl if we need 
    if not os.path.exists(pdf):
        download_pdf(directory_url, pdf)

    with pdfplumber.open(pdf) as pdff:
        total_pages = len(pdff.pages)
        print(f"Total pages: {total_pages}")
        if method == "pairs":
            for i in range(start_page - 1, total_pages - (total_pages - end_page) - 1): # pairs of pages
                if (i - start_page + 1) % 2 == 0:  # every other
                    current_page_text = pdff.pages[i].extract_text() if pdff.pages[i] else ""
                    next_page_text = pdff.pages[i + 1].extract_text() if i + 1 < len(pdff.pages) else ""  # Handle the last page case
                    text = current_page_text + " " + next_page_text
                    if text:
                        save_combined_image(pdf, i + 1, i + 2, "tmp", imgDir) #we don't know the ID yet but need it for chatgpt
                        airport_info = extract_page_info(i, text, state)
                        if airport_info:
                            airport_data.append(airport_info)
                            id = airport_info.get("Airport Identifier")
                            if id:
                                save_combined_image(pdf, i + 1, i + 2, id, imgDir)  # Adjust indices as necessary
                if i >= (total_pages - (total_pages - end_page) - 1):  # Check if it's time to break after processing pairs
                    break
        else:
            for i, page in enumerate(pdff.pages[start_page-1:], start=start_page):
                text = page.extract_text()
                if text:
                    save_image(pdf, i, "tmp", imgDir) #we don't know the ID yet but need it for chatgpt
                    airport_info = extract_page_info(i, text, state)
                    if airport_info:
                        airport_data.append(airport_info)
                        id = airport_info.get("Airport Identifier")
                        if id: save_image(pdf, i, id, imgDir)
                if i > (total_pages - (total_pages-end_page)):
                    break
            

    # Convert the list of dictionaries into a pandas DataFrame
    df = pd.DataFrame(airport_data)
    
    # Print the DataFrame
    print(df)

    df.to_csv(out, mode='a', index=False)
    print(f"Data saved to {out}")

def save_combined_image(pdf_path, start_page, end_page, name, imgdir):
    if not os.path.exists(imgdir):
        os.makedirs(imgdir)

    # Convert pages to images
    images = convert_from_path(pdf_path, first_page=start_page, last_page=end_page)
    images = [image.rotate(270, expand=True) for image in images] #to rotate

    # Assuming images are not empty and have the same width
    total_height = sum(image.height for image in images)
    max_width = max(image.width for image in images)
    
    # Create a new image with the combined height of the two pages
    combined_image = Image.new('RGB', (max_width, total_height))
    
    # Paste the images into the combined image
    y_offset = 0
    for image in images:
        combined_image.paste(image, (0, y_offset))
        y_offset += image.height
    
    # Save the combined image
    combined_image_filename = f"{imgdir}{name}.png"
    combined_image.save(combined_image_filename, 'PNG')

def save_image(pdf_path, pageNum, name, imgdir):
    if not os.path.exists(f'{imgdir}'):
        os.makedirs(imgdir)

    images = convert_from_path(pdf_path, first_page=pageNum, last_page=pageNum)
    for i, image in enumerate(images):
        image.save(f'{imgdir}{name}.png', 'PNG')

def download_pdf(url, save_path):
    print(f"Downloading pdf from {url}")
    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        
        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Open the file path as a binary file and write the content
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"PDF successfully downloaded and saved as '{save_path}'.")
        else:
            print(f"Failed to download the PDF. HTTP status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred downloading file: {e}")  

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def main():
    airport_data = []
    if not os.path.exists(airports_path):
        download_pdf(airports_url, airports_path)

    #parse_state(airport_data, "or", or_url, "pairs", 66, 109) # eastern
    #parse_state(airport_data, "or", or_url, "pairs", 112, 123) # gorge
    #parse_state(airport_data, "or", or_url, "pairs", 126, 143) # portland
    #parse_state(airport_data, "or", or_url, "pairs", 146, 187) # southern
    #parse_state(airport_data, "or", or_url, "pairs", 190, 221) # WILLAMETTE
    #parse_state(airport_data, "or", or_url, "pairs", 30, 63) # coast
    #parse_state(airport_data, "or", or_url, "pairs", 14, 27) # central

if __name__ == "__main__":
    main()


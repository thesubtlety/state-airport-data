import pdfplumber
import pandas as pd
import requests
import os
import csv
from pdf2image import convert_from_path

pdf_url = 'https://www.mdt.mt.gov/other/webdata/external/aero/airport-directory.pdf'
mt_pdf_path = 'montana-directory.pdf'
outfile = 'airport_info_mt.csv'

def extract_airport_info(text):
    # Initialize dictionary to hold extracted info
    airport_info = {
        "Airport Identifier": "",
        "Airport Name": "",
        "Courtesy Car": "No",
        "Bicycles": "No",
        "Camping": "No",
        "Meals": "No"
    }
    
    # Split text into lines for easier processing
    lines = text.split('\n')
    if lines:
        # Assuming the first line contains the airport name
        airport_info["Airport Name"] = lines[-1].strip().replace("Ø","0")
    
    for line in lines:
        # Extracting the identifier
        if "IDENT:" in line:
            parts = line.split()
            ident_index = parts.index("IDENT:") + 1
            if ident_index < len(parts):
                airport_info["Airport Identifier"] = parts[ident_index]
        # Check for amenities
        if "rental" in line.lower() or "courtesy" in line.lower() or "crew car" in line.lower():
            airport_info["Courtesy Car"] = "Yes"
        if "camping" in line.lower():
            airport_info["Camping"] = "Yes"
        if "meals" in line.lower() or "food" in line.lower():
            airport_info["Meals"] = "Yes"
        if "bicycles" in line.lower() or "bikes" in line.lower():
            airport_info["Bicycles"] = "Yes"

    return airport_info

def save_image(pdf_path, pageNum, name):
    images = convert_from_path(pdf_path, first_page=pageNum+1, last_page=pageNum+1) #0-based
    for i, image in enumerate(images):
        image.save(f'images_mt/{name}.png', 'PNG')

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

def main():
    pdf_path = mt_pdf_path
    airport_data = []

    if not os.path.exists(pdf_path):
        download_pdf(pdf_url, mt_pdf_path)

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"Total pages: {total_pages}")

        for i, page in enumerate(pdf.pages):
            if i<35 or i>total_pages-3 : continue #skip the first 35 pages and last 3 pages
            text = page.extract_text()
            if text:
                airport_info = extract_airport_info(text)
                if airport_info["Airport Name"]:
                    id = airport_info["Airport Identifier"].replace("Ø","0")
                    #save_image(pdf_path, i, id)
                airport_data.append(airport_info)
                    
    # Convert the list of dictionaries into a pandas DataFrame
    df = pd.DataFrame(airport_data)
    
    # Print the DataFrame
    print(df)

    df.to_csv(outfile, index=False)
    print(f"Data saved to {outfile}")

if __name__ == "__main__":
    main()

'''
Modifications
8S1,POLSON,Yes,No,No,Yes
S09,HOT SPRINGS,Yes,No,No,Yes
3U8,BIG SANDY,Yes,No,No,Yes
BZN,BOZEMAN,Yes,No,No,Yes
97M,EKALAKA,Yes,No,No,Yes
S59,LIBBY,Yes,No,No,Yes
7S0,RONAN,Yes,No,No,Yes
7S6,WHITE SULPHUR SPRINGS,Yes,No,No,Yes
8U8,TOWNSEND,Yes,No,No,Yes
KGPI,KALISPELL (1),Yes,No,No,Yes

'''
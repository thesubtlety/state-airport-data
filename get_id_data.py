import pdfplumber
import pandas as pd
import requests
import os
import csv
from pdf2image import convert_from_path

pdf_url = 'https://itd.idaho.gov/wp-content/uploads/2020/08/Airport-Facilities-Directory.pdf'
pdf_path = 'idaho-directory.pdf'

def extract_airport_info(page, text):
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
    print(lines)
    if lines:
        # Assuming the first line contains the airport name
        name = lines[0]
        ident = name.split(' ')[-1]
        nme = " ".join(name.split(' ')[0:-1])
        print(nme)
        print(ident)

        if len(ident) > 4 or len(ident) < 3:
            print(f"Error parsing page {page} ({name})")
            return #ignore for now, manually fix
        else:
            airport_info["Airport Identifier"] = ident.replace("Ø","0")
            airport_info["Airport Name"] = nme
    
    for line in lines:
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
        image.save(f'images_id/{name}.png', 'PNG')

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
    airport_data = []

    if not os.path.exists(pdf_path):
        download_pdf(pdf_url, pdf_path)

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"Total pages: {total_pages}")

        for i, page in enumerate(pdf.pages):
            if i<37 or i>total_pages-20 : continue #skip the first and last pages
            #if i != 83: continue
            text = page.extract_text()
            if text:
                airport_info = extract_airport_info(i, text)
                if airport_info:
                    airport_data.append(airport_info)
                    id = airport_info.get("Airport Identifier")
                    if id: save_image(pdf_path, i, id) #lots of bad data
                    
    # Convert the list of dictionaries into a pandas DataFrame
    df = pd.DataFrame(airport_data)
    
    # Print the DataFrame
    print(df)

    df.to_csv('airport_info_id.csv', index=False)
    print("Data saved to airport_info_id.csv")

    #todo fix up with modifications before writing to file

if __name__ == "__main__":
    main()

'''
Fixes (due to pdf text extraction issues)

BOI,BOISE AIRPORT,Yes,No,No,Yes
U87,SMILEY CREEK,Yes,No,No,Yes
AOC,ARCO-BUTTE CO,No,No,No,Yes
1U0,BEAR TRAP,No,No,No,No
U84,DONNELLY,No,Yes,No,Yes
U89,GLENNS FERRY,No,No,No,Yes
SUN,HAILEY,Yes,No,No,Yes
LWS,LEWISTON,Yes,No,No,Yes
MYL,MCCALL,Yes,Yes,No,Yes
25U,MEMALOOSE USFS,No,No,No,No
0U9,MIDVALE,No,No,No,No
1U1,MOOSE CREEK USFS,No,No,No,No
U76,MOUNTAIN HOME,Yes,No,No,Yes
1U2,MUD LAKE,No,No,No,Yes
MAN,NAMPA,No,No,No,Yes
1U4,NEW MEADOWS ,No,No,No,Yes
1U6,OAKLEY,No,No,No,Yes
1U7,PARIS/BEAR LAKE CO,Yes,No,No,Yes
PIH,POCATELLO,Yes,No,No,Yes
1S1,PORTHILL,No,No,No,Yes
PUW,PULLMAN/MOSCOW,Yes,No,No,Yes
1S7,SLATE CREEK,No,No,No,No
TWF,TWIN FALLS,Yes,No,No,Yes
0U1,WARM SPRINGS,No,No,Yes,No
U02,BLACKFOOT,Yes,No,No,Yes
I08,CABIN CREEK USFS,No,No,No,No
HRF,HAMILTON MT,No,No,No,Yes
OU7,HOLLOW TOP,No,No,No,No
U00,LEADORE,No,No,No,Yes
ID28,MACKAY BAR,No,No,No,No
MLD,MALAD,Yes,No,No,Yes
0U8,MAY,No,No,No,No
ID82,PICABO,No,No,No,Yes
I92,REED RANCH,No,No,Yes,No
ID74,SULPHUR CREEK,No,No,No,Yes
I45,WAPSHILLA,No,No,No,No
0U7,HOLLOW TOP,No,No,No,No
ID28,MACKAY BAR,No,No,No,No
ID8,MARBLE CREEK,No,No,No,No
ID82,PICABO,No,No,No,Yes
ID74,SULPHUR CREEK,No,No,No,Yes

'''
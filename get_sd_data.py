import pdfplumber
import pandas as pd
import requests
import os
import re
from PIL import Image
from pdf2image import convert_from_path

'''
update page nums
update data terms
'''

pdf_url = 'https://drive.google.com/file/d/1s04nV-sgQ0J5bsz9d9yyxE2I1RP3k0ao/view'
pdf_path = 'directories/southdakota-directory.pdf'
outputf = 'airport_info_sd.csv'
imgdir = 'images_sd/'

airports_url = 'https://davidmegginson.github.io/ourairports-data/airports.csv'
airports_path = 'airports.csv'

def save_images_for_pages(pdf_path, start_page, end_page, name, imgdir):
    if not os.path.exists(imgdir):
        os.makedirs(imgdir)

    images = convert_from_path(pdf_path, first_page=start_page, last_page=end_page)
    for i, image in enumerate(images):
        # Adjust the file name to include the page number if multiple images are expected
        image_filename = f"{imgdir}{name}_page_{start_page + i}.png"
        image.save(image_filename, 'PNG')

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
    
    #import pdb
    #pdb.set_trace()
    
    # Split text into lines for easier processing
    lines = text.split('\n')
    print(lines)
    if lines:
        # Assuming one of these lines contains the airport name
        namestr = lines[0]
        ident = namestr.split(" ")[-1]
        nme = " ".join(namestr.split(" ")[1:-1])

        print(nme)
        print(ident)

        if len(ident) > 4 or len(ident) < 3:
            print(f"Error parsing page {page} ({nme})")
            #return #ignore for now, manually fix
        else:
            airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
            airport_info["Airport Name"] = nme.strip()
    
    for line in lines:
        # Check for amenities
        if "rental" in line.lower() or "courtesy" in line.lower() or "crew car" in line.lower():
            airport_info["Courtesy Car"] = "Yes"
        if "camping" in line.lower():
            airport_info["Camping"] = "Yes"
        if "dining: " in line.lower():
            airport_info["Meals"] = "Yes"
        if "bicycles" in line.lower() or "bikes" in line.lower():
            airport_info["Bicycles"] = "Yes"

    return airport_info

def save_combined_image(pdf_path, start_page, end_page, name, imgdir):
    if not os.path.exists(imgdir):
        os.makedirs(imgdir)

    # Convert pages to images
    images = convert_from_path(pdf_path, first_page=start_page, last_page=end_page)
    
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

def process_two_pages(i, current_page_text, next_page_text):
    combined_text = current_page_text + " " + next_page_text
    airport_info = extract_airport_info(i, combined_text)
    return airport_info

def main():
    airport_data = []

    if not os.path.exists(pdf_path):
        download_pdf(pdf_url, pdf_path)
        download_pdf(airports_url, airports_path)

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"Total pages: {total_pages}")

        start_page = 36
        end_page = 175

        for i in range(start_page - 1, total_pages - (total_pages - end_page) - 1): # pairs of pages
            if (i - start_page + 1) % 2 == 0:  # every other
                current_page_text = pdf.pages[i].extract_text() if pdf.pages[i] else ""
                next_page_text = pdf.pages[i + 1].extract_text() if i + 1 < len(pdf.pages) else ""  # Handle the last page case

                if current_page_text or next_page_text:  # Proceed if either of the pages has text
                    airport_info = process_two_pages(i, current_page_text, next_page_text)
                    if airport_info:
                        airport_data.append(airport_info)
                        id = airport_info.get("Airport Identifier")
                        if id:
                            save_combined_image(pdf_path, i + 1, i + 2, id, imgdir)  # Adjust indices as necessary

                if i >= (total_pages - (total_pages - end_page) - 1):  # Check if it's time to break after processing pairs
                    break
                    
    # Convert the list of dictionaries into a pandas DataFrame
    df = pd.DataFrame(airport_data)
    
    # Print the DataFrame
    print(df)

    df.to_csv(outputf, index=False)
    print(f"Data saved to {outputf}")

    #todo fix up with modifications before writing to file

if __name__ == "__main__":
    main()

'''
Fixes (due to pdf text extraction issues)
Copy paste into airport_info_state.csv before converting to json

EVW,Uinta County Airport,Yes,No,No,No
RKS,Southwest Wyoming Regional Airport,Yes,No,No,No

'''
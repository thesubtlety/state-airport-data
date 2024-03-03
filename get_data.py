import pdfplumber
import pandas as pd
import requests
import os
import csv
from pdf2image import convert_from_path

pdf_url = 'https://www.mdt.mt.gov/other/webdata/external/aero/airport-directory.pdf'
mt_pdf_path = 'airport-directory.pdf'

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
        if "courtesy car" in line.lower() or "crew car" in line.lower():
            airport_info["Courtesy Car"] = "Yes"
        if "camping" in line.lower():
            airport_info["Camping"] = "Yes"
        if "meals" in line.lower():
            airport_info["Meals"] = "Yes"
        if "bicycles" in line.lower():
            airport_info["Bicycles"] = "Yes"

    return airport_info

def save_image(pdf_path, pageNum, name):
    images = convert_from_path(pdf_path, first_page=pageNum+1, last_page=pageNum+1) #0-based
    for i, image in enumerate(images):
        image.save(f'images/{name}.png', 'PNG')

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
    make_html()
    exit(0)
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
                    id = airport_info["Airport Identifier"]
                    airport_data.append(airport_info)
                    save_image(pdf_path, i, id)
                    
    # Convert the list of dictionaries into a pandas DataFrame
    df = pd.DataFrame(airport_data)
    
    # Print the DataFrame
    print(df)

    df.to_csv('airport_info.csv', index=False)
    print("Data saved to airport_info.csv")

def make_html():
    # Define the path to the images directory
    images_directory = "images/"

    # Start the HTML output with the table tag and headers
    html_output = '''
        <!DOCTYPE html>
    <html>
    <head>
        <title>MT Airports Table</title>
        <script src="https://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script>
    </head>
    <style>
        .modal {
            display: none; /* Hidden by default */
            position: fixed; /* Stay in place */
            z-index: 1; /* Sit on top */
            left: 30%;
            top: 0;

            overflow: auto; /* Enable scroll if needed */
            background-color: rgb(146, 143, 143); /* Fallback color */
            background-color: rgba(210, 204, 204, 0.9); /* Black w/ opacity */
            padding-top: 30px; /* Added padding to ensure modal content does not touch the edges */
        }

        .modal-content {
            /* Existing styles */
            margin: auto;
            display: block;
            width: 80%; /* Adjust this to control the modal width */
            max-width: 700px; /* Adjust this to control the maximum size of the modal */
            position: relative; 
            top: 50%;
            transform: translateY(-50%);
            max-height: 80vh; /* vh is a percentage of the viewport height */
            object-fit: contain; /* This makes the image keep its aspect ratio */
        }

        .close {
            position: absolute;
            top: -10px; /* Adjust as needed */
            right: 15px; /* Adjust as needed */
            color: #f1f1f1;
            font-size: 40px;
            font-weight: bold;
            transition: 0.3s;
        }

        .close:hover,
        .close:focus {
            color: #bbb;
            text-decoration: none;
            cursor: pointer;
        }

        /* Style the Image Used to Trigger the Modal */
        .myImg {
            border-radius: 5px;
            cursor: pointer;
            transition: 0.3s;
            max-height: 100vh;
        }

        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        table.sortable {
            border-collapse: collapse;
            width: 100%;
            border: 1px solid #ddd;
        }
        table.sortable th, table.sortable td {
            text-align: left;
            padding: 8px;
        }
        table.sortable th {
            background-color: #4CAF50;
            color: white;
        }
        table.sortable tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        table.sortable tr:hover {
            background-color: #ddd;
        }
        .image-cell img {
            height: 50px; /* Adjust based on your preference */
            width: auto;
        }
    </style>
    <body>
    <!-- The Modal -->
    <div id="myModal" class="modal">
        <span class="close">&times;</span>
        <img class="myImg" class="modal-content" id="img01">
    </div>
    <table border="0" class="sortable">
    <tr>
        <th>Image</th>
        <th>Airport Identifier</th>
        <th>Airport Name</th>
        <th>Courtesy Car</th>
        <th>Bicycles</th>
        <th>Camping</th>
        <th>Meals</th>
    </tr>
    '''

    # Read the CSV file
    with open('airport_info.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Construct the row HTML
            row_html = f'''
    <tr>
        <td><img class="myImg" src="images/{row["Airport Identifier"]}.png" width="70" alt="{row["Airport Identifier"]}"></td>
        <td>{row["Airport Identifier"]}</td>
        <td>{row["Airport Name"]}</td>
        <td>{row["Courtesy Car"]}</td>
        <td>{row["Bicycles"]}</td>
        <td>{row["Camping"]}</td>
        <td>{row["Meals"]}</td>
    </tr>
    '''
            # Append the row to the output
            html_output += row_html

    # Close the table tag
    html_output += '''
    </table>
    <script>
        // Get the modal
        var modal = document.getElementById("myModal");
        var modalImg = document.getElementById("img01");

        document.querySelectorAll('.myImg').forEach(item => {
            item.addEventListener('click', event => {
                modal.style.display = "block";
                modalImg.src = item.src;
            })
        })
        var span = document.getElementsByClassName("close")[0];
        span.onclick = function() { 
            modal.style.display = "none";
        }
    </script>
</body>
</html>
    '''

    # Print or save the HTML output
    #print(html_output)
    # If you want to save the output to an HTML file:
    with open('airports_table.html', 'w') as html_file:
        html_file.write(html_output)

if __name__ == "__main__":
    main()

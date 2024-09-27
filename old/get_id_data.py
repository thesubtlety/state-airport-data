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
        if "camping" in line.lower() or "campground" in line.lower():
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
Airport Identifier,Airport Name,Courtesy Car,Bicycles,Camping,Meals
06U,JACKPOT NV,Yes,No,No,Yes
0S5,NEZ PERCE,No,No,No,Yes
0U0,LANDMARK USFS,No,No,Yes,No
0U1,WARM SPRINGS,No,No,Yes,No
0U2,COPPER BASIN,No,No,No,No
0U3,MAHONEY CREEK USFS,No,No,No,No
0U7,HOLLOW TOP,No,No,No,No
0U8,MAY,No,No,No,No
0U9,MIDVALE,No,No,No,No
I08,CABIN CREEK USFS,No,No,No,No
12ID,FLYING BRANCH,No,No,No,Yes
I45,WAPSHILLA,No,No,No,No
I92,REED RANCH,No,No,Yes,No
1S1,PORTHILL,No,No,No,Yes
1S6,PRIEST RIVER,No,No,No,Yes
1S7,SLATE CREEK,No,No,No,No
1U0,BEAR TRAP,No,No,No,No
1U1,MOOSE CREEK USFS,No,No,No,No
1U2,MUD LAKE,No,No,No,Yes
1U3,MURPHY,No,No,No,Yes
1U4,NEW MEADOWS ,No,No,No,Yes
1U6,OAKLEY,No,No,No,Yes
1U7,PARIS/BEAR LAKE CO,Yes,No,No,Yes
1U9,PINE,No,No,No,Yes
24K,KRASSELUSFS,No,No,No,No
25U,MEMALOOSE USFS,No,No,No,No
2U0,PRAIRIE,No,No,Yes,No
2U4,ROCKFORD,No,No,No,Yes
2U5,SHEARER USFS,No,No,No,No
2U7,STANLEY,No,No,No,Yes
2U8,THOMAS CREEK,No,No,No,No
32S,STEVENSVILLE MT,No,No,No,Yes
3U0,MURPHY HOT SPRINGS,No,No,No,No
3U1,WARREN USFS,No,No,No,Yes
3U2,JOHNSON CREEK,Yes,No,Yes,Yes
46U,ALPINE,No,No,No,Yes
50S,PARMA,No,No,No,Yes
52U,WEATHERBY USFS,No,No,No,No
55H,ATLANTA,No,No,No,No
65S,BONNERS FERRY,Yes,No,No,Yes
66S,CAVANAUGH BAY,Yes,No,No,Yes
67S,PRIEST LAKE USFS,No,No,No,Yes
75C,OROGRANDE USFS,No,No,No,No
78U,SNAKE RIVER SPB,No,No,No,Yes
85U,SOLDIER BAR USFS,No,No,No,No
A05,DIXIE USFS,No,No,No,No
AOC,ARCO-BUTTE CO,No,No,No,Yes
BOI,BOISE AIRPORT,Yes,No,No,Yes
BYI,BURLEY,No,No,No,Yes
C48,WILSON BAR-USFS,No,No,No,No
C53,LOWER LOON,No,No,No,No
C64,CAYUSE CREEK USFS,No,No,No,No
MLD,MALAD,Yes,No,No,Yes
COE,COEUR D'ALENE,Yes,No,No,Yes
D28,TANGLEFOOT SPB,No,No,No,Yes
D47,COUGAR RANCH IDF&G,No,No,No,No
DIJ,DRIGGS,Yes,No,No,Yes
EUL,CALDWELL,Yes,No,No,Yes
GIC,GRANGEVILLE,Yes,No,No,Yes
GNG,GOODING,Yes,No,No,Yes
HRF,HAMILTON MT,No,No,No,Yes
I08,CABIN CREEK USFS,No,No,No,No
I45,WAPSHILLA,No,No,No,No
I92,REED RANCH,No,No,Yes,No
ID28,MACKAY BAR,No,No,No,No
ID74,SULPHUR CREEK,No,No,No,Yes
ID8,MARBLE CREEK,No,No,No,No
ID82,PICABO,No,No,No,Yes
IDA,IDAHO FALLS,No,No,No,No
JER,JEROME,Yes,No,No,Yes
U02,BLACKFOOT,Yes,No,No,Yes
LLJ,CHALLIS,Yes,No,No,Yes
LWS,LEWISTON,Yes,No,No,Yes
MAN,NAMPA,No,No,No,Yes
MLD,MALAD,Yes,No,No,Yes
MYL,MCCALL,Yes,Yes,No,Yes
ONO,ONTARIO OR,Yes,No,No,Yes
0U7,HOLLOW TOP,No,No,No,No
0U8,MAY,No,No,No,No
PIH,POCATELLO,Yes,No,No,Yes
PUW,PULLMAN/MOSCOW,Yes,No,No,Yes
RXE,REXBURG,Yes,No,No,Yes
S66,HOMEDALE,No,No,No,Yes
S68,OROFINO,No,No,No,Yes
S72,ST MARIES,No,No,No,Yes
S73,KAMIAH,Yes,No,No,Yes
S75,PAYETTE,No,No,No,Yes
S76,BROOKS SPB,No,No,No,Yes
S77,MAGEE,No,No,Yes,No
S78,EMMETT,Yes,No,No,Yes
S81,INDIAN CREEK USFS,No,No,No,No
S82,KOOSKIA,No,No,No,Yes
S83,KELLOGG,No,No,No,Yes
S84,COTTONWOOD,No,No,No,Yes
S87,WEISER,Yes,No,No,Yes
S89,CRAIGMONT,No,No,No,No
S90,ELK CITY,No,No,No,Yes
S92,FISH LAKE USFS,No,No,No,No
SMN,SALMON,Yes,No,No,Yes
SUN,HAILEY,Yes,No,No,Yes
SZT,SANDPOINT,Yes,No,No,Yes
TWF,TWIN FALLS,No,No,No,No
TWF,TWIN FALLS,Yes,No,No,Yes
U00,LEADORE,No,No,No,Yes
U01,AMERICAN FALLS,Yes,No,No,Yes
U02,BLACKFOOT,Yes,No,No,Yes
U03,BUHL,Yes,No,No,Yes
U10,PRESTON,Yes,No,No,Yes
U12,ST ANTHONY,No,No,No,Yes
U36,ABERDEEN,No,No,No,Yes
U37,MIDWAY,No,No,No,No
U41,DUBOIS,No,No,No,Yes
U45,GRAHAM USFS,No,No,No,No
U46,BIG SOUTHERN BUTTE,No,No,No,No
U48,COX'S WELL,No,No,No,No
U51,BANCROFT,No,No,No,Yes
U53,HENRY'S LAKE,No,No,Yes,No
U54,BERNARD USFS,No,No,No,No
U56,RIGBY,No,No,No,Yes
U58,DOWNEY,No,No,No,Yes
U60,BIG CREEK,No,No,No,No
U61,TWIN BRIDGES,No,No,No,No
U62,MACKAY,No,No,No,Yes
U63,BRUCE MEADOWS,No,No,Yes,No
U65,CAREY,No,No,No,Yes
U70,CASCADE,No,No,No,Yes
U72,UPPER LOON CREEK USFS,No,No,No,No
U76,MOUNTAIN HOME,Yes,No,No,Yes
U78,SODA SPRINGS,Yes,No,No,Yes
U79,CHAMBERLAIN BASIN USFS,No,No,No,No
U81,COLD MEADOWS USFS,No,No,No,No
U82,COUNCIL,No,No,No,Yes
U84,DONNELLY,No,Yes,No,Yes
U86,FAIRFIELD,No,No,No,Yes
U87,SMILEY CREEK,Yes,No,No,Yes
U87,SMILEY CREEK,Yes,No,No,Yes
U88,GARDEN VALLEY,Yes,No,No,Yes
U89,GLENNS FERRY,No,No,No,Yes
U91,GRASMERE,No,No,No,No
U92,ANTELOPE VALLEY,No,No,No,No
U93,MAGIC RESERVOIR,No,No,No,Yes
U94,HAZELT ON,No,No,No,Yes
U97,HOWE,No,No,No,No
U98,IDAHO CITY USFS,No,No,No,Yes
U99,LAIDLAW CORRALS,No,No,No,No
U00,LEADORE,No,No,No,Yes


'''
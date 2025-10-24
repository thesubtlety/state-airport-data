import cv2
import pytesseract
import re
from dataclasses import dataclass
from typing import Dict, List, Optional
import sys
@dataclass

class AirportData:
    name: str
    identifier: str
    location: Dict[str, str]
    elevation: int
    ctaf: str
    runways: List[Dict]
    services: List[str]
    manager: str
    remarks: str

def extract_airport_data(image_path):
    # Read and preprocess the image
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # For these charts, simple thresholding works well
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    
    # Use PSM 6 for uniform block of text
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(thresh, config=custom_config)
    print(text)
    
    # Parse structured data
    data = {}
    
    # Extract coordinates
    coord_pattern = r'LAT\s+(\d+°\d+\.\d+\')\s+LONG\s+(\d+°\d+\.\d+\')'
    coord_match = re.search(coord_pattern, text)
    if coord_match:
        data['lat'] = coord_match.group(1)
        data['long'] = coord_match.group(2)
    
    # Extract elevation
    elev_match = re.search(r'ELEVATION\s+(\d+)', text)
    if elev_match:
        data['elevation'] = int(elev_match.group(1))
    
    # Extract CTAF
    ctaf_match = re.search(r'CTAF\s+([\d.]+)', text)
    if ctaf_match:
        data['ctaf'] = ctaf_match.group(1)
    
    # Extract runway info
    runway_pattern = r'(\d{2}[LRC]?)\s+(\d+)\s+x\s+(\d+)'
    runways = re.findall(runway_pattern, text)
    data['runways'] = [{'id': r[0], 'length': r[1], 'width': r[2]} for r in runways]
    
    return data

# For even better results with these specific charts, 
# you could use region-based extraction:

def extract_by_regions(image_path):
    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    
    # Define regions based on typical chart layout
    regions = {
        'header': (0, 0, width, int(height * 0.1)),
        'location': (0, int(height * 0.08), int(width * 0.5), int(height * 0.15)),
        'layout_map': (0, int(height * 0.15), width, int(height * 0.5)),
        'data_table': (0, int(height * 0.5), width, height)
    }
    
    extracted_data = {}
    
    for region_name, (x1, y1, x2, y2) in regions.items():
        roi = img[y1:y2, x1:x2]
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        # Adjust preprocessing based on region
        if region_name == 'data_table':
            # Tables need different processing
            _, thresh_roi = cv2.threshold(gray_roi, 180, 255, cv2.THRESH_BINARY)
        else:
            _, thresh_roi = cv2.threshold(gray_roi, 200, 255, cv2.THRESH_BINARY)
        
        text = pytesseract.image_to_string(thresh_roi, config='--psm 6')
        extracted_data[region_name] = text
    
    return extracted_data

def main():
    image_path = sys.argv[1]
    data = extract_airport_data(image_path)
    print(data)

if __name__ == "__main__":
    main()
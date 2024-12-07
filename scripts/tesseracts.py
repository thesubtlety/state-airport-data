from PIL import Image
import pytesseract
import sys

'''
brew install tesseract
pip3.11 install pytesseract
'''

# Function to extract text from an image file
def extract_text_from_image(image_path):
    # Open the image file
    img = Image.open(image_path)
    
    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(img)
    
    return text

# Replace 'path_to_image.png' with your image file path
image_path =  sys.argv[1] #'images/mi/BEH.png'
extracted_text = extract_text_from_image(image_path)

# Print the extracted text
print(extracted_text)

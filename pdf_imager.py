import os
import sys
from pdf2image import convert_from_path
from PIL import Image

def save_image(pdf_path, pageNum, ident, imgdir):
    images = convert_from_path(pdf_path, first_page=pageNum, last_page=pageNum)
    for i, image in enumerate(images):
        image.save(f'{imgdir}/{ident}.png', 'PNG')
        print(f"saved {ident}")

def save_combined_image(pdf_path, start_page, end_page, name, imgdir,degrees):
    if not os.path.exists(imgdir):
        os.makedirs(imgdir)

    # Convert pages to images
    images = convert_from_path(pdf_path, first_page=start_page, last_page=end_page)
    images = [image.rotate(degrees, expand=True) for image in images]
    
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
    combined_image_filename = f"{imgdir}/{name}.png"
    combined_image.save(combined_image_filename, 'PNG')
    print(f"saved {combined_image_filename}.png")

def main():
    pdfpath = "directories/or.pdf"
    start_page = 22
    end_page = 23
    ident = "RDM"
    imgdir = "images/or"
    degrees = 270 # typically 0 unless you're special like oregon
    #save_image(pdfpath, pageNum, ident, imgdir)
    save_combined_image(pdfpath, start_page, end_page, ident, imgdir, degrees)

if __name__ == "__main__":
    main()
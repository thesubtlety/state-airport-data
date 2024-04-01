import os
import sys
from pdf2image import convert_from_path

def save_image(pdf_path, pageNum, ident, imgdir):
    images = convert_from_path(pdf_path, first_page=pageNum, last_page=pageNum)
    for i, image in enumerate(images):
        image.save(f'{imgdir}/{ident}.png', 'PNG')
        print(f"saved {ident}")

def main():
    pdfpath = "directories/northdakota-directory.pdf"
    pageNum = 25
    ident = "Y71"
    imgdir = "images_nd"
    save_image(pdfpath, pageNum, ident, imgdir)

if __name__ == "__main__":
    main()
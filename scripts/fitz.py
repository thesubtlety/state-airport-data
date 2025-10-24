import pymupdf
import sys

path = sys.argv[1]

doc = pymupdf.open(path)
page = doc[51]

# Try different extraction flags
text = page.get_text()
print("Basic extraction:", text)

# Force text extraction with OCR if needed
text_ocr = page.get_text(flags=pymupdf.TEXT_PRESERVE_LIGATURES | pymupdf.TEXT_PRESERVE_WHITESPACE)
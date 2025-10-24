import pdfplumber 
import sys
import re
import os

path = sys.argv[1]

with pdfplumber.open(path) as pdff:
    first_page = pdff.pages[50]
    text = first_page.extract_text()
    print("Default extraction:", first_page.extract_text())
    print("\nWith layout:", first_page.extract_text(layout=True))
    print("\nWith x_tolerance=3:", first_page.extract_text(x_tolerance=3))
    print(text)

lines = text.split('\n')
ident, nme = "", ""

for line in lines:    
    m = re.search(r'^(.*?)\s*\((\w{3})\)$', line)
    if m:
        nme = m.group(1)
        ident = m.group(2)

sys.exit()

for pdf in os.listdir(path):
    try:
        with pdfplumber.open(path+pdf) as pdff:
            first_page = pdff.pages[0]
            text = first_page.extract_text()
            #print(text)

        lines = text.split('\n')
        ident, nme = "", ""

        for line in lines:    
            m = re.search(r'^(.*?)\s*\((\w{3})\)$', line)
            if m:
                nme = m.group(1)
                ident = m.group(2)

        print(", ".join([ident, nme, pdf]))
    except:
        continue

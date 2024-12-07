import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import os
import PyPDF2

MAIN_URL = "https://fly.arkansas.gov/airport-info.html"

def get_ar_pdfs():
    response = requests.get(MAIN_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get all links from the main page
    links = set(a.get('href') for a in soup.find_all('a', href=True))

    for link in links:
        link = urljoin(MAIN_URL, link)
        resp = requests.get(link)
        sub_soup = BeautifulSoup(resp.text, 'html.parser')
        pdf_links = set(a.get('href') for a in sub_soup.find_all('a', href=True) if a['href'].lower().endswith('.pdf'))

        for pdf_link in pdf_links:
            pdf_url = urljoin(link, pdf_link)
            print(f"Found PDF: {pdf_url}")
            pdf_response = requests.get(pdf_url, stream=True)
            filename = f'directories/ar/{os.path.basename(pdf_url)}'
            with open(filename, 'wb') as f:
                for chunk in pdf_response.iter_content(chunk_size=8192):
                    f.write(chunk)

def combine_pdfs_in_dir(directory, output_filename):
    pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]

    merger = PyPDF2.PdfMerger()
    for pdf_file in pdf_files:
        full_path = os.path.join(directory, pdf_file)
        merger.append(full_path)

    with open(os.path.join(directory, output_filename), 'wb') as f:
        merger.write(f)

def main():
    get_ar_pdfs()
    combine_pdfs_in_dir('directories/ar/','combined_ar.pdf')

if __name__ == "__main__":
    main()
import requests
from bs4 import BeautifulSoup
import csv
import os
import re
import time

MAIN_URL = "https://oklahoma.gov/aerospace/airports/find-an-airport.html"
BASE_URL = "https://oklahoma.gov/aerospace/airports/find-an-airport/"
OUTPUT_FILE = "data/airport_info_ok.csv"

def get_airport_list():
    """Fetch the list of all airports from the main page."""
    print(f"Fetching airport list from {MAIN_URL}...")
    response = requests.get(MAIN_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    airports = []
    # Find the table containing airport data
    table = soup.find('table')
    if not table:
        raise Exception("Could not find airport table on page")

    # Parse table rows
    for row in table.find_all('tr')[1:]:  # Skip header row
        cols = row.find_all('td')
        if len(cols) >= 3:
            airport_link = cols[0].find('a')
            if airport_link:
                airport_name = airport_link.text.strip()
                airport_url = airport_link.get('href', '')
                airport_id = cols[1].text.strip()
                city = cols[2].text.strip()

                airports.append({
                    'id': airport_id,
                    'name': airport_name,
                    'city': city,
                    'url': airport_url
                })

    print(f"Found {len(airports)} airports")
    return airports

def get_courtesy_car_info(airport_url):
    """Visit an airport page and extract courtesy car information."""
    # Handle relative URLs
    if not airport_url.startswith('http'):
        if airport_url.startswith('/'):
            airport_url = f"https://oklahoma.gov{airport_url}"
        else:
            airport_url = BASE_URL + airport_url

    try:
        response = requests.get(airport_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for "Ground Transportation Available" section
        # This might be in a table, div, or paragraph
        text_content = soup.get_text()

        # Search for ground transportation section
        if 'Ground Transportation Available' in text_content:
            # Try to find the Yes/No value near this text
            # Look for common patterns
            paragraphs = soup.find_all(['p', 'td', 'div', 'li'])
            for p in paragraphs:
                text = p.get_text()
                if 'Ground Transportation Available' in text or 'Courtesy Car' in text:
                    # Check for Yes/No in the same or next element
                    if 'Yes' in text:
                        return 'Yes'
                    elif 'No' in text:
                        return 'No'

            # If we found the section but couldn't determine Yes/No, default to No
            return 'No'

        return 'No'

    except requests.exceptions.RequestException as e:
        print(f"  Error fetching {airport_url}: {e}")
        return 'No'

def fetch_oklahoma_data():
    """Main function to fetch all Oklahoma airport data."""
    airports = get_airport_list()
    airport_data = []

    for i, airport in enumerate(airports, 1):
        print(f"[{i}/{len(airports)}] Processing {airport['id']} - {airport['name']}...")

        courtesy_car = get_courtesy_car_info(airport['url'])

        airport_data.append({
            'identifier': airport['id'],
            'name': airport['name'],
            'courtesy_car': courtesy_car,
            'bicycles': 'No',
            'camping': 'No',
            'meals': 'No'
        })

        # Be polite to the server
        time.sleep(0.5)

    return airport_data

def write_csv(airport_data):
    """Write airport data to CSV file."""
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)

    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'identifier', 'name', 'courtesy_car', 'bicycles', 'camping', 'meals'
        ])

        # Write header
        f.write('Airport Identifier,Airport Name,Courtesy Car,Bicycles,Camping,Meals\n')

        # Write data rows
        for airport in airport_data:
            f.write(f"{airport['identifier']},{airport['name']},{airport['courtesy_car']},{airport['bicycles']},{airport['camping']},{airport['meals']}\n")

    print(f"\nData written to {OUTPUT_FILE}")
    print(f"Total airports: {len(airport_data)}")
    print(f"With courtesy cars: {sum(1 for a in airport_data if a['courtesy_car'] == 'Yes')}")
    print(f"Without courtesy cars: {sum(1 for a in airport_data if a['courtesy_car'] == 'No')}")

def main():
    """Main entry point."""
    try:
        airport_data = fetch_oklahoma_data()
        write_csv(airport_data)
        print("\nOklahoma airport data successfully updated!")
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    main()

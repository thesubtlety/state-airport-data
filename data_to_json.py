import csv
import json
import sys

if len(sys.argv) < 2:
    sys.exit("Usage: data_to_json <statecode>")

state = sys.argv[1]

state_data = 'airport_info_%s.csv' % state
outfile = 'data_%s.json' % state
all_airports = 'airports.csv'

airport_facts = {}
enriched = {}

# Define a mapping of CSV indices to attribute names for clarity and maintainability
index_to_name = {
    3: 'name',
    4: 'latitude',
    5: 'longitude',
    6: 'elevation',
    9: 'state',
    13: 'gps_code',
}

# Read the basic airport data
with open(all_airports, mode='r') as airport_data:
    reader = csv.reader(airport_data)
    next(reader)  # Skip the header row
    for row in reader:
        ident = row[14] #local_code
        state = row[9] # country
        if not "US" in state or "CA" in state: continue
        # Use dictionary comprehension to map indices to their named attributes
        airport_facts[ident] = {index_to_name[i]: row[i] for i in index_to_name}       

# Read the airport attributes data
with open(state_data, mode='r') as attributes_file:
    state_data_reader = csv.DictReader(attributes_file)
    for state_aero_row in state_data_reader:
        ident = state_aero_row['Airport Identifier']
        ident = ident.strip().replace("Ø","0")
        #if ident in airport_facts:
        if not airport_facts.get(ident):
            print(f"key not found: {ident}")
        else:
            if ident not in enriched:
                enriched[ident] = {
                    'info': airport_facts[ident],
                    'attributes': {}
                }
            enriched[ident]['attributes'].update({
                'courtesy_car': state_aero_row['Courtesy Car'].lower() == 'yes',
                'bicycles': state_aero_row['Bicycles'].lower() == 'yes',
                'camping': state_aero_row['Camping'].lower() == 'yes',
                'meals': state_aero_row['Meals'].lower() == 'yes',
            })

# for ident, data in enriched.items():
#     print(f"{ident}: {data}")

# Prepare data for JSON output
output = [
    {
        'id': key,
        'name': value['info']['name'],
        'latitude': float(value['info']['latitude']),
        'longitude': float(value['info']['longitude']),
        'elevation': value['info']['elevation'],
        'courtesy_car': value['attributes']['courtesy_car'],
        'bicycles': value['attributes']['bicycles'],
        'camping': value['attributes']['camping'],
        'meals': value['attributes']['meals'],
    } for key, value in enriched.items()
]

# Output the combined data as JSON
#print('const items =', json.dumps(output, indent=2))

with open(outfile, 'w') as outfile:
    json.dump({'items': output}, outfile, indent=2)


import json
import sys

def read_json_file(file_path):
    """Reads a JSON file and returns the parsed data."""
    with open(file_path, 'r') as file:
        return json.load(file)

def combine_json_files(file_paths):
    combined_items = []

    for path in file_paths:
        data = read_json_file(path)
        combined_items.extend(data['items'])
    
    return combined_items

if __name__ == '__main__':
    # Skip the first argument (script name), take the rest as file paths
    file_paths = sys.argv[1:]
    
    if not file_paths:
        print("Usage: python combine.py file1.json file2.json ...")
        sys.exit(1)

    combined_items = combine_json_files(file_paths)
    
    # Save the combined list to a new JSON file
    combined_file_path = 'data/combined_data.json'
    with open(combined_file_path, 'w') as file:
        json.dump({"items": combined_items}, file, indent=4)
    
    print(f"Combined items from {len(file_paths)} files into {combined_file_path}.")

# --------------------------------------------------------------------------------
# FILE HANDLER MODULE
# This module deals with reading and writing files. 
# We use standard JSON files because they are simple, human-readable text files
# that store data like lists and dictionaries.
# ---------------------------------------------------------------------------------

import json
import os

# Directory where all our data files (JSON) will be stored
DATA_DIR = 'data'

def ensure_data_dir():
    """
    Checks if the 'data' folder exists. If not, it creates it.
    This prevents errors when trying to read or write files inside it.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def read_json_file(filename):
    """
    Reads data from a JSON file in the data directory.
    If the file doesn't exist, it returns an empty list.
    """
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    
    # If file doesn't exist, we return an empty list because there is no data yet
    if not os.path.exists(filepath):
        return []
    
    try:
        with open(filepath, 'r') as file:
            # json.load parses the text file back into Python lists and dicts
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        # If there's an issue with the file (corrupted or empty), return an empty list
        return []

def write_json_file(filename, data):
    """
    Saves data (list or dictionary) into a JSON file in the data directory.
    """
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    
    try:
        with open(filepath, 'w') as file:
            # json.dump converts Python lists/dicts into nice spaced-out text using indent=4
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Error saving data to {filename}: {e}")
        return False

if __name__ == "__main__":
    from main import main
    main()

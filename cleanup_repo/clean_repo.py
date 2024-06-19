import os 
import json
from pathlib import Path
from datetime import datetime

def cleaning_ids():
    repo_path = Path("fetch_data/ids_data/") 

    # Get list of JSON files
    json_files = list(repo_path.glob("**/*.json"))  # Updated pattern

    if not json_files:
        print("No JSON files found in the specified directory.")
        return

    # Parse datetimes from file names
    json_files_with_datetimes = []
    for json_file in json_files:
        try:
            datetime_str = json_file.stem.split("_")[0]  
            datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")
            json_files_with_datetimes.append((json_file, datetime_obj))
        except ValueError:
            print(f"Skipping file with invalid datetime format: {json_file}")
            
    json_files_with_datetimes.sort(key=lambda x: x[1], reverse=True)

    # Remove older JSON files
    for json_file, _ in json_files_with_datetimes[1:]:  
        try:
            with open(json_file, "r") as f:
                json.load(f)  
            os.remove(json_file)
            print(f"Removed JSON file: {json_file}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error processing {json_file}: {e}")
            
            

if __name__ == "__main__":
    cleaning_ids()

import json
import sys
import os

def find_ids(obj, ids):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "id":
                ids.append(value)
            else:
                find_ids(value, ids)
    elif isinstance(obj, list):
        for item in obj:
            find_ids(item, ids)
    return ids

def find_duplicate_ids(filepaths):
    all_ids = []
    for filepath in filepaths:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            ids = find_ids(data, [])
            all_ids.extend(ids)

    duplicate_ids = set([id_ for id_ in all_ids if all_ids.count(id_) > 1])
    return duplicate_ids

def get_all_json_files_in_directory(directory_path):
    return [
        os.path.join(directory_path, filename)
        for filename in os.listdir(directory_path)
        if filename.endswith(".json")
    ]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python find_duplicate_ids.py <path1> [<path2> ... <pathN>]")
        sys.exit(1)

    filepaths = []
    for path in sys.argv[1:]:
        if os.path.isdir(path):
            filepaths.extend(get_all_json_files_in_directory(path))
        elif os.path.isfile(path) and path.endswith(".json"):
            filepaths.append(path)
        else:
            print(f"Warning: {path} is not a recognized JSON file or folder. Skipping...")

    duplicate_ids = find_duplicate_ids(filepaths)

    if duplicate_ids:
        print("Duplicate IDs found:")
        for duplicate_id in duplicate_ids:
            print(f"- {duplicate_id}")
    else:
        print("No duplicate IDs found.")
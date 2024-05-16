import os
import json

def merge_json_files(input_folder, output_file):
    # List to store data from all JSON files
    all_data = []

    # Iterate through each file in the input folder
    for filename in os.listdir(input_folder):
        # Check if the file is a JSON file
        if filename.endswith('.json'):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r') as file:
                # Load data from JSON file
                data = json.load(file)
                # Append data to the list
                all_data.append(data)

    # Write the combined data to the output JSON file
    with open(output_file, 'w') as outfile:
        json.dump(all_data, outfile, indent=4)
    
    print(f"Combined JSON data written to {output_file}")

# Example usage:
input_folder = "./ava/ava_backend/resources/jsons"
output_file = "./ava/ava_backend/resources/all_json/output.json"
merge_json_files(input_folder, output_file)

import os
import json
import pandas as pd

input_dir = "D:/AIproject/bpwp/PJP_results"
output_file = "output_table.csv"


all_data = []


print(f"Searching for JSON files in {input_dir}...")  
for root, dirs, files in os.walk(input_dir):
    print(f"Checking directory: {root}") 
    for filename in files:
        if filename.endswith(".json"): 
            file_path = os.path.join(root, filename)
            folder_name = os.path.basename(root)
            print(f"Processing file: {file_path}, Folder: {folder_name}") 
            with open(file_path, "r", encoding="utf-8") as f:
                try:
            
                    data = json.load(f)
                    
                    data["file_path"] = file_path  
                    data["file_name"] = filename  
                    data["folder_name"] = folder_name  
              
                    all_data.append(data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from file {file_path}: {e}")


if not all_data:
    print("No JSON files were processed or data is empty.")


df = pd.DataFrame(all_data)

df.to_csv(output_file, index=False)

print(f"Data has been written to {output_file}")

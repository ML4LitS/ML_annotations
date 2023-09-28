import csv
from tqdm import tqdm
import re
import pickle
import json

# Input and output filenames
input_filename = "/home/stirunag/work/github/source_data/knowledge_base/taxdump/names.dmp"
output_pickle_filename = "/home/stirunag/work/github/source_data/dictionaries/NCBI_taxonomy.pkl"
output_jsonl_filename = "/home/stirunag/work/github/source_data/training_data/train_data_floret.jsonl"

# Determine the total number of rows in the input file for the progress bar
with open(input_filename, 'r') as f:
    total_rows = sum(1 for line in f)

# Dictionary to hold the output data
output_dict = {}


# Function to process the content of column 1
def process_column_content(s):
    s = re.sub(r'\(.*?\)|\".*?\"|\[.*?\]', '', s).strip()
    return s.strip()


# Read the .dmp file and process the data
with open(input_filename, "r") as infile:
    # Create CSV reader object
    reader = csv.reader(infile, delimiter="|")

    # Iterate through each row in the input file with a progress bar
    for row in tqdm(reader, total=total_rows, desc="Processing"):
        if "authority" not in row[3]:
            extracted_text = process_column_content(row[1])
            # Update the dictionary with the extracted text and corresponding identifier
            output_dict[extracted_text] = row[0].strip()

# Dump the dictionary as a pickle file
with open(output_pickle_filename, "wb") as outfile:
    pickle.dump(output_dict, outfile)

# Append data to jsonl file
with open(output_jsonl_filename, "a") as jsonl_file:
    for term in output_dict.keys():
        json_line = json.dumps({"text": term})
        jsonl_file.write(json_line + "\n")


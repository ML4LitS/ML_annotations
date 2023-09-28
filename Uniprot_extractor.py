import re
import pickle
import csv
import json
from tqdm import tqdm

# Patterns for extracting relevant information
AC_PATTERN = re.compile(r"AC   (.*?);\n")
GN_PATTERN = re.compile(r"GN   (.+?)\n")
DE_PATTERN = re.compile(r"DE   (.+?)\n")

# List of keys we are interested in, for GN and DE values
GN_KEYS = ['Name', 'Synonyms', 'OrderedLocusNames', 'ORFNames', 'EC']
DE_KEYS = ['RecName: Full', 'AltName: Full', 'Short']

output_pickle_filename = "/home/stirunag/work/github/source_data/dictionaries/output.pkl"
output_csv_filename = "/home/stirunag/work/github/source_data/dictionaries/output.csv"
output_jsonl_filename = "/home/stirunag/work/github/source_data/training_data/train_data_floret.jsonl"

def extract_values_from_line(line, keys):
    values_list = []
    # Remove text enclosed in { }
    line = re.sub(r"\{.*?\}", "", line).strip()
    for key in keys:
        match = re.search(f"{key}=(.*?)(;|$)", line)
        if match:
            values = match.group(1).split(', ')
            values_list.extend(values)
    return values_list


def process_document(buffer, output_dict):
    doc = ''.join(buffer)

    ac_match = AC_PATTERN.search(doc)
    ac_values = ac_match.group(1).split("; ") if ac_match else None

    if ac_values:
        ac_value = ac_values[0]  # using the primary AC value
        # For DE values
        de_matches = DE_PATTERN.findall(doc)
        for de_line in de_matches:
            de_values = extract_values_from_line(de_line, DE_KEYS)
            for value in de_values:
                output_dict[value.strip()] = ac_value  # interchanging keys and values

        # For GN values
        gn_matches = GN_PATTERN.findall(doc)
        for gn_line in gn_matches:
            gn_values = extract_values_from_line(gn_line, GN_KEYS)
            for value in gn_values:
                output_dict[value.strip()] = ac_value  # interchanging keys and values


def process_file_line_by_line(filename):
    buffer = []
    output_dict = {}

    with open(filename, 'r') as file:
        for line in tqdm(file, desc="Processing file"):
            buffer.append(line)
            if line.startswith("//"):
                process_document(buffer, output_dict)
                buffer = []

    return output_dict


filename = "/home/stirunag/work/github/source_data/knowledge_base/uniprot/uniprot_sprot.dat"
output_dict = process_file_line_by_line(filename)

# Dump the dictionary as a pickle file
with open(output_pickle_filename, "wb") as outfile:
    pickle.dump(output_dict, outfile)

# Write to CSV file
with open(output_csv_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Term', 'AC'])  # header row
    for key, value in output_dict.items():
        writer.writerow([key, value])

# Append data to jsonl file
with open(output_jsonl_filename, "a") as jsonl_file:
    for key, value in output_dict.items():
        json_line = json.dumps({"text": key, "AC": value})  # getting term and AC for jsonl
        jsonl_file.write(json_line + "\n")
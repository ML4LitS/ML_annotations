import csv
import pickle
import json
from pronto import Ontology
from tqdm import tqdm

# Input and output filenames
input_filename = "/home/stirunag/work/github/source_data/knowledge_base/chebi/chebi.owl"
output_pickle_filename = "/home/stirunag/work/github/source_data/dictionaries/chebi_terms.pkl"
output_jsonl_filename = "/home/stirunag/work/github/source_data/training_data/train_data_floret.jsonl"

# Load the ontology
chebi = Ontology(input_filename)

# Dictionary to hold the output data
output_dict = {}

# Iterate through each term in the ontology with a progress bar
for term in tqdm(chebi.terms(), total=len(chebi.terms())):
    # Extract the ID and name of the term
    chebi_id = term.id
    term_name = term.name

    # Update the dictionary with the term name and corresponding identifier
    output_dict[term_name] = chebi_id

# Dump the dictionary as a pickle file
with open(output_pickle_filename, "wb") as outfile:
    pickle.dump(output_dict, outfile)

# Append data to jsonl file
with open(output_jsonl_filename, "a") as jsonl_file:
    for term in output_dict.keys():
        json_line = json.dumps({"text": term})
        jsonl_file.write(json_line + "\n")

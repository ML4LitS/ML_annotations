import csv
from pronto import Ontology
from tqdm import tqdm

input_filename = "/home/stirunag/work/github/source_data/chebi/chebi.owl"
output_filename = "/home/stirunag/work/github/source_data/chebi/chebi_terms.csv"
# load the ontology
chebi = Ontology(input_filename)

# open a CSV file to write the ID and term
with open(output_filename, 'w', newline='') as csvfile:
    fieldnames = ['chebi_id', 'term']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # write the header to the CSV file
    writer.writeheader()

    # iterate through each term in the ontology with a progress bar
    for term in tqdm(chebi.terms(), total=len(chebi.terms())):
        # extract the ID and name of the term
        chebi_id = term.id
        term_name = term.name

        # write the ID and term to the CSV file
        writer.writerow({'chebi_id': chebi_id, 'term': term_name})

import csv
from tqdm import tqdm
import re

# Input and output filenames
input_filename = "/home/stirunag/work/github/source_data/taxdump/names.dmp"
output_filename = "/home/stirunag/work/github/source_data/taxdump/output.csv"

# Determine the total number of rows in the input file for the progress bar
with open(input_filename, 'r') as f:
    total_rows = sum(1 for line in f)


# Function to process the content of column 1
def process_column_content(s):
    # Extract pattern from """ pattern"" and discard everything else in the string
    # if '"' in content:
    #     match = re.search(r'\"{3}\s*([^\"]*)\"{2}', content)
    #     if match:
    #         content = match.group(1)
    #     else:
    #         content = ""
    # else:
    #     # Remove patterns like "author et al." and "Yoshida and Oshima 1971"
    #     content = re.sub(r'[\w\s]+et al\.', '', content)
    #     content = re.sub(r'\w+\s+and\s+\w+\s+\d{4}', '', content)

    # Removing anything in parentheses or quotes
    s = re.sub(r'\(.*?\)|\".*?\"|\[.*?\]', '', s).strip()
    # Removing trailing author names and dates
    # s = re.sub(r'(\s+et\s+al\..*|\s+[0-9]{4})$', '', s).strip()

    return s.strip()


# Read the .dmp file and write the required columns to the output CSV file
with open(input_filename, "r") as infile, open(output_filename, "w", newline='') as outfile:
    # Create CSV reader and writer objects
    reader = csv.reader(infile, delimiter="|")
    writer = csv.writer(outfile)

    # Write the header to the output file
    writer.writerow(["AC", "OG"])

    # Iterate through each row in the input file with a progress bar
    for row in tqdm(reader, total=total_rows, desc="Processing"):
        if "authority" not in row[3]:
            extracted_text = re.sub(r'\(.*?\)|\".*?\"|\[.*?\]', '', row[1]).strip()
            # Write column 0 and modified column 1 to the output file
            writer.writerow([row[0].strip(), extracted_text.strip()])

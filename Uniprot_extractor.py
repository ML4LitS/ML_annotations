import re
import csv

# Patterns for extracting relevant information
AC_PATTERN = re.compile(r"AC   (.*?);\n")
GN_PATTERN = re.compile(r"GN   (.+?)\n")
DE_PATTERN = re.compile(r"DE   (.+?)\n")

# List of keys we are interested in, for GN and DE values
GN_KEYS = ['Name', 'Synonyms', 'OrderedLocusNames', 'ORFNames', 'EC']
DE_KEYS = ['RecName: Full', 'AltName: Full', 'Short']


def extract_values_from_line(line, keys):
    values_dict = {}
    # Remove text enclosed in { }
    line = re.sub(r"\{.*?\}", "", line).strip()
    for key in keys:
        match = re.search(f"{key}=(.*?)(;|$)", line)
        if match:
            values = match.group(1).split(', ')
            values_dict[key] = values
    return values_dict


def process_document(buffer, writer):
    doc = ''.join(buffer)

    ac_match = AC_PATTERN.search(doc)
    ac_value = ac_match.group(1) if ac_match else None

    # For DE values
    de_matches = DE_PATTERN.findall(doc)
    for de_line in de_matches:
        de_values = extract_values_from_line(de_line, DE_KEYS)
        for key, values in de_values.items():
            for value in values:
                writer.writerow([ac_value, "DE_" + key, value.strip()])

    # For GN values
    gn_matches = GN_PATTERN.findall(doc)
    for gn_line in gn_matches:
        gn_values = extract_values_from_line(gn_line, GN_KEYS)
        for key, values in gn_values.items():
            for value in values:
                writer.writerow([ac_value, "GN_" + key, value.strip()])


def process_file_line_by_line(filename, csv_filename):
    buffer = []
    with open(filename, 'r') as file, open(csv_filename, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['AC', 'Type', 'Value'])  # header row

        for line in file:
            buffer.append(line)
            if line.startswith("//"):
                process_document(buffer, writer)
                buffer = []


filename = "/home/stirunag/work/github/source_data/uniprot/uniprot_sprot.dat"
csv_filename = "/home/stirunag/work/github/source_data/uniprot/output_file_v3.csv"
process_file_line_by_line(filename, csv_filename)

import re
import csv

# Patterns for extracting relevant information
AC_PATTERN = re.compile(r"AC   (.*?);\n")

DE_PATTERNS = [re.compile(pattern) for pattern in [
    r"DE   RecName: Full=(.*?);\n",
    r"DE   AltName: Full=(.*?);\n",
    r"DE            Short=(.*?);\n"
]]

GN_PATTERN = re.compile(r"GN   (.+?)\n")

# List of keys we are interested in, for GN values
GN_KEYS = ['Name', 'Synonyms', 'OrderedLocusNames', 'ORFNames', 'EC']


# def extract_values_from_gn_line(gn_line):
#     gn_values = {}
#     for key in GN_KEYS:
#         match = re.search(f"{key}=(.*?)(;|$)", gn_line)
#         if match:
#             values = match.group(1).split(', ')
#             # Remove text enclosed in { }
#             values = [re.sub(r"\{.*?\}", "", v).strip() for v in values]
#             gn_values[key] = values
#     return gn_values
def extract_values_from_gn_line(gn_line):
    gn_values = {}
    # Remove text enclosed in { }
    # gn_line = re.sub(r"\{[^}]*\}", "", gn_line).strip() #re.sub(r"\{[^}]*\}", "", gn_line).strip()
    for key in GN_KEYS:
        match = re.search(f"{key}=(.*?)(;|$)", gn_line)
        if match:
            values = match.group(1).split(', ')
            gn_values[key] = values
    return gn_values

def process_document(buffer, writer):
    doc = ''.join(buffer)

    ac_match = AC_PATTERN.search(doc)
    ac_value = ac_match.group(1) if ac_match else None

    # For DE values
    for pattern in DE_PATTERNS:
        de_match = pattern.search(doc)
        if de_match:
            de_value = de_match.group(1)
            writer.writerow([ac_value, "DE", de_value])

    # For GN values
    gn_matches = GN_PATTERN.findall(doc)
    for gn_line in gn_matches:
        gn_values = extract_values_from_gn_line(gn_line)
        for key, values in gn_values.items():
            for value in values:
                value = re.sub(r"\{[^}]*\}", "", value).strip()
                value = value.replace('\"', '')
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
csv_filename = "/home/stirunag/work/github/source_data/uniprot/output_file_v2.csv"
process_file_line_by_line(filename, csv_filename)

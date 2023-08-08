import csv
import re

patterns = [
    r'(?<=Full=)[^}]+',
    r'(?<=Name=)[^ }]+',
    r'(?<=OrderedLocusNames=)[^ ]+',
    r'(?<=Synonyms=)[^ }]+',
    r'(?<=ORFNames=)[^ ]+',
    r'Name=([^ {]+)|OrderedLocusNames=([^ ,]+)|ORFNames=([^ ,]+)'
]


def extract_information(input_file):
    with open(input_file, 'r') as file:
        ac_value = None
        de_values = []
        gn_values = []

        for line in file:
            if line.strip() == "//":
                if ac_value:
                    for de_value in de_values:
                        yield ac_value, de_value
                    for gn_value in gn_values:
                        yield ac_value, gn_value
                ac_value = None
                de_values = []
                gn_values = []
            elif line.startswith("AC   "):
                ac_value = line.strip().split()[-1].replace(';', '')
            elif line.startswith("DE   "):
                de_value = line.strip().split("DE   ", 1)[-1].replace(';', '')
                de_values.append(de_value)
            elif line.startswith("GN   "):
                gn_value = line.strip().split("GN   ", 1)[-1].replace(';', '')
                gn_values.append(gn_value)



# def extract_names(input_string):
#     extracted_names = []
#     regex = r'=\s*([^{}]+)'  # Regular expression to match text after the "=" symbol and exclude text within curly braces {}
#     matches = re.findall(regex, input_string)
#     extracted_names = [name.strip() for name in matches]
#     return extracted_names

def extract_names(input_string, patterns):
    extracted_values = []
    for pattern in patterns:
        matches = re.findall(pattern, input_string)
        names = [match.split("{")[0].strip() for match in matches]
        extracted_values.extend(names)
    return extracted_values
# Test the function with the given input string and patterns



def write_to_csv(input_file, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['AC value', 'Description', 'real'])

        for ac_value, description in extract_information(input_file):
            extracted_names = extract_names(description, patterns)
            for each_name in extracted_names:
                csv_writer.writerow([ac_value, each_name, description])


if __name__ == "__main__":
    input_file_path = "/home/stirunag/work/github/source_data/uniprot/uniprot_sprot.dat"
    output_file_path = "/home/stirunag/work/github/source_data/uniprot/output_file.csv"

    write_to_csv(input_file_path, output_file_path)

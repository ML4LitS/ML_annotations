import csv

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
                ac_value = line.strip().split()[-1]
            elif line.startswith("DE   "):
                de_value = line.strip().split("DE   ", 1)[-1]
                de_values.append(de_value)
            elif line.startswith("GN   "):
                gn_value = line.strip().split("GN   ", 1)[-1]
                gn_values.append(gn_value)

def write_to_csv(input_file, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['AC value', 'Description'])

        for ac_value, description in extract_information(input_file):
            csv_writer.writerow([ac_value, description])



if __name__ == "__main__":
    input_file_path = "/home/stirunag/work/github/source_data/uniprot/uniprot_sprot.dat"
    output_file_path = "/home/stirunag/work/github/source_data/uniprot/output_file.csv"

    write_to_csv(input_file_path, output_file_path)

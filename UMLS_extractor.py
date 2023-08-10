import csv

resources = {
    'HL7V2.5': '1',
    'ICD10AM': '1',
    'ICD10AMAE': '1',
    'LCH': '1',
    'MTHICPC2ICD10AE': '1',
    'MTHMST': '1',
    'NCI_RENI': '1',
    'SNM': '1',
    'SNMI': '1',
    'SNOMEDCT_VET': '1',
    'FMA': '1',
    'GO': '1',
    'ICD10': '1',
    'ICD10AE': '1',
    'ICD10CM': '1',
    'ICD9CM': '1',
    'LNC': '1',
    'MDR': '1',
    'MEDLINEPLUS': '1',
    'MSH': '1',
    'MTH': '1',
    'MTHICD9': '1',
    'NCI': '1',
    'NCI_BRIDG': '1',
    'NCI_CDISC': '1',
    'NCI_CTCAE': '1',
    'NCI_CTEP-SDC': '1',
    'NCI_FDA': '1',
    'NCI_NCI-GLOSS': '1',
    'NDFRT': '1',
    'OMIM': '1',
    'SNOMEDCT_US': '1',
    'WHO': '1',
}


def filter_term(term):
    if len(term) < 3:
        return False
    return True


def modify_term(term):
    replacements = [
        '-- ',
        ' (physical finding)', ' (diagnosis)', ' (disorder)', ' (procedure)', ' (finding)',
        ' (symptom)', ' (history)', ' (treatment)', ' (manifestation)', ' [Disease/Finding]',
        ' (morphologic abnormality)', ' (etiology)', ' (observable entity)', ' (event)',
        ' (situation)', ' (___ degrees)', ' (in some patients)', ' (___ cm)', ' (___ mm)',
        ' (#___)', ' (rare)', ' (___ degree.)', ' (including anastomotic)', ' (navigational concept)',
        ' (___cm)', ' (1 patient)', ' (qualifier value)', ' (lab test)', ' (unintentional)',
        ' (tophi)', ' (NOS)', ' (___ msec)', ' (RENI)', ' (less common)', ' [as symptom]', ' (s)'
    ]

    for replacement in replacements:
        term = term.replace(replacement, '')

    term = term.replace('-', ' ')

    return term

def is_required_category(category):
    required_categories = ["T020", "T190", "T049", "T019", "T047", "T050", "T033", "T037", "T048", "T191", "T046", "T184"]
    return category in required_categories


input_path = "/home/stirunag/work/github/source_data/umls-2023AA-mrconso/MRCONSO.RRF"
output_path = "/home/stirunag/work/github/source_data/umls-2023AA-mrconso/output.csv"

with open(input_path, 'r', newline='', encoding='utf-8') as infile, open(output_path, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile, delimiter='|')
    writer = csv.writer(outfile)

    for row in reader:
        # if row and resources.get(row[11], '0') == '1':  # Assuming the 12th column (index 11) represents the resource
        if row and len(row[14]) > 3 and row[1] == "ENG" and row[16] != "O" and resources.get(row[11],'0') == '1' and is_required_category(row[0]):
            term = modify_term(row[14])  # Assuming the 15th column (index 14) represents the term
            if filter_term(term):
                writer.writerow([row[0], term])

print("Processing complete!")



print("Processing complete!")
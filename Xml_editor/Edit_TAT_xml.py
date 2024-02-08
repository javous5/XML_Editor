import os
import csv
import xml.etree.ElementTree as ET

# File path to the folder containing all XML files
directory_path = '/home/caritas/Desktop/Bash_files/Open_ALL_TAT_FORMS/XML_FILES'

# File path to the CSV file containing patient IDs and contents
csv_file_path = '/home/caritas/Desktop/Bash_files/Open_ALL_TAT_FORMS/visit_id.csv'

# Read patient IDs and contents from the CSV file
patient_data = {}
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip header row
    for row in csv_reader:
        if len(row) >= 2:
            patient_id = row[0].strip()
            content_to_replace = row[1].strip()
            patient_data[patient_id] = content_to_replace

# Loop through each XML file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.xml'):
        file_path = os.path.join(directory_path, filename)

        # Extract patient ID from the XML file name
        patient_id = filename.split('_')[2]

        # Check if the patient ID exists in the CSV data
        if patient_id in patient_data:
            # Load the XML file
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Find all occurrences of the <mortality> tag
            mortality_tags = root.findall('.//mortality')

            # Check if there are any occurrences
            if mortality_tags:
                # Access the last occurrence
                last_mortality_tag = mortality_tags[-1]

                # Find the <visit_id> tag within the last <mortality> tag
                visit_id_tag = last_mortality_tag.find('.//visit_id')

                # Check if the <visit_id> tag is found
                if visit_id_tag is not None:
                    # Change the content of the <visit_id> tag
                    visit_id_tag.text = patient_data[patient_id]
                else:
                    print(f'<visit_id></visit_id> tag not found within {filename}')

                # Save the modified XML back to the file
                tree.write(file_path)
            else:
                print(f'<mortality></mortality> tag not found in {filename}')
        else:
            print(f'Patient ID {patient_id} not found in CSV data for {filename}')


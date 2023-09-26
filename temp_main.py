import pandas as pd
import os
import glob
import numpy as np
import tabula
from helpers import search_splice_index, update_previous_row, clean_data

# Load in all your files
path = 'files.pdf'
pdf_files = glob.glob(os.path.join(path, "*.pdf"))

print(pdf_files)

# Process each PDF file
for pdf_file in pdf_files:
    print(f"Processing: {pdf_file}")

    # Load the PDF using tabula
    df = tabula.read_pdf(pdf_file, stream=True, pages='1900')
    
    # Initialize data dictionary for each PDF file
    data = {
        'Proposal Number': [],
        'Proposal Text': [],
        'Mgmt Rec': [],
        'Vote Instruction': [],
    }

    # Process each page of the PDF
    for line in df:
        headers = line.columns.tolist()
        split_index = search_splice_index(line)
        new_df = line.iloc[split_index:].reset_index(drop=True)
        
        if not new_df.empty:
            for index, row in new_df.iterrows():
                values = row.values.tolist()
                
                if 'Number Proposal Text' in str(values[headers.index('Proposal Number')]):
                    clean_row = clean_data([values])[0]
                    data['Proposal Number'].append(str(clean_row[0]))
                    data['Proposal Text'].append(str(clean_row[1]))
                    data['Mgmt Rec'].append(str(clean_row[2]))
                    data['Vote Instruction'].append(str(clean_row[3]))

    # Creating a pandas DataFrame from the extracted data dictionary
    df = pd.DataFrame(data)

    # Saving the DataFrame as CSV
    csv_filename = os.path.splitext(pdf_file)[0] + '_output.csv'
    df.to_csv(csv_filename, index=False)

    # Saving the DataFrame as Excel
    excel_filename = os.path.splitext(pdf_file)[0] + '_output.xlsx'
    df.to_excel(excel_filename, index=False)

print("CSV and Excel files created.")

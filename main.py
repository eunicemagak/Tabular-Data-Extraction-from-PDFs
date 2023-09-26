import pandas as pd
import os
import glob
import numpy as np
import tabula
from helpers import search_splice_index, update_previous_row, clean_data

# load in all your files
path = 'files.pdf'
pdf_files = glob.glob(os.path.join(path, "*.pdf"))

print(pdf_files)

data = {
    # 'headers': [],
    'Proposal Number': [],
    'Proposal Text': [],
    'Mgmt Rec': [],
    'Vote Instruction': [],
}

df = tabula.read_pdf(path, stream=True, pages='7')
print(df)
table_data = []
rows_delete = []
headers = []
for line in df:
    headers = line.columns.tolist()
    split_index = search_splice_index(line)
    new_df = line.iloc[split_index:].reset_index(drop=True)
    if not new_df.empty:
        for index, row in new_df.iterrows():
            values = row.values.tolist()
            table_data.append(values)

print(table_data)
for index in range(len(table_data) - 1, 0, -1):
    row = table_data[index]

    if all(pd.isna(value) for value in row[-2:]):
        # Append the text of the current row to the previous row
        table_data[index - 1] = update_previous_row(table_data[index - 1], table_data[index])
        rows_delete.append(index)

# Delete the rows marked for deletion
for index in rows_delete:
    del table_data[index]

clean_data = clean_data(table_data)
print(clean_data)
for row in clean_data[1:]:
    data['Proposal Number'].append(str(row[0]))
    data['Proposal Text'].append(str(row[1]))
    data['Mgmt Rec'].append(str(row[2]))
    data['Vote Instruction'].append(str(row[3]))

# Creating a pandas DataFrame from the data dictionary
df = pd.DataFrame(data)


# Saving the DataFrame as CSV
csv_filename = 'output.csv'
df.to_csv(csv_filename, index=False)


# Saving the DataFrame as Excel
excel_filename = 'output.xlsx'
df.to_excel(excel_filename, index=False)

print("CSV and Excel files created.")


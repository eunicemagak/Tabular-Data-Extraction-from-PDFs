import pandas as pd

# split the provided dataframe to separate the headers data from table data
def search_splice_index(data_frame):
    headers = data_frame.columns.tolist()
    print(headers)
    start_index = 0
    # print(line[])
    for df_index, df_row in data_frame.iterrows():
        if 'Number Proposal Text' in str(data_frame[headers[0]].values[df_index]):
            start_index = df_index + 1
        # print("eunice", [data_frame[header].values[df_index] for header in headers])
    return start_index


# cleaning the column data, some of the columns are so long that they flow to the next line so this function 
# tries to identify these colummns that have overflowed to the next line and appends / concatenate to the desired column 
def update_previous_row(previous_row, current_row):
    for i in range(len(current_row[:-2])):
        if not pd.isna(current_row[i]):
            previous_row[i] = previous_row[i] + ' ' + current_row[i]
            return previous_row


#on then generating the final table data , you get scenarios where proposal number and proposal texts 
# have been concatenated so this function cleans those columns
def clean_data(table_data):
    for row in table_data:
        for i, v in enumerate(row):
            if pd.isna(v) and i != 0:
                values = row[i-1].strip().split()
                row[i-1] = values[0]
                row[i] = ' '.join(values[1:])
    return table_data

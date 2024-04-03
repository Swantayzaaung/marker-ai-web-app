# https://johnvastola.medium.com/how-to-combine-multiple-csv-files-using-python-to-analyze-797fc825c541
import csv
import glob
from helpers import sort_nicely

filepath = "./output/bio ms csv/tables/"
csv_files = glob.glob(filepath + "*.csv")
sort_nicely(csv_files)

# Use a wildcard pattern to match all CSV files in the directory
# Initialize an empty list to store rows from each file
combined_data = []
tableQ = []
# Read and append rows from each CSV file to the combined_data list
for file in csv_files:
    with open(file, 'r', encoding="utf-8-sig") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        # print(header)
        if 'Question' in header[0]:
            if not combined_data:  # Include header only once
                combined_data.append(list(filter(None, header)))
            # combined_data.extend(row for row in reader)
            for row in reader:
                try:
                    nextRow = next(reader)
                    if nextRow[0] == '':
                        tableQ.append(row)
                        tableQ.append(nextRow)     
                    else:
                        combined_data.append(row)                   
                        combined_data.append(nextRow)                   
                except:
                    combined_data.append(row)                   
    
for row in combined_data:
    # row.pop()
    print(row)
    
for row in tableQ:
    print(row)
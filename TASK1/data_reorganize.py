from sys import argv
s,f=argv     # f is input file
import pandas as pd
import numpy as np

#Input CSV file loading
data = pd.read_csv(f)
print(data.columns)
data.columns = data.columns.str.strip()
#Creating a unique identifier for each strand and CpG_Coordinates combination
data['Strand_CpG'] = data['strand'].astype(str)+"_"+data['CpG_Coordinates'].astype(str)

#Generating all unique combinations of Strand_CpG and pattern columns
unique_strand_cpg = data['Strand_CpG'].unique()
patterns = ['`000', '`001', '`010', '`011', '`100', '`101', '`110', '`111']

#Creating all combinations of Strand_CpG and patterns
columns = [f"{strand_cpg}_{pattern}" for strand_cpg in unique_strand_cpg for pattern in patterns]

#Initializing the new DataFrame with Sample_ID_Replicate as rows and generated columns
samples = data['Sample_ID'].astype(str)+ "_" + data['Replicate'].astype(str)
unique_samples = samples.unique()

#Creating an empty DataFrame to hold the reorganized data
new_data = pd.DataFrame(index=unique_samples, columns=columns)

#adding the new DataFrame with values from the original dataset
for _, row in data.iterrows():
    sample_id_rep = str(row['Sample_ID']) + "_" + str(row['Replicate'])
    for pattern in patterns:
        col_name = f"{row['Strand_CpG']}_{pattern}"
        if col_name in new_data.columns:
            new_data.at[sample_id_rep, col_name] = row[pattern]

#Adding 'Tissue' column
new_data['Tissue'] = data.groupby(samples)['Tissue'].first()

#Saving the reorganized data to a new CSV file
new_data.to_csv("reorganized_data.csv", index_label="Sample_ID_Replicate")

print("Data reorganization complete. Saved to 'reorganized_data.csv'")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sys import argv
import seaborn as sns

# Load the input data
s,f=argv # f is input file
df = pd.read_csv(f,header=None)
# Sum eight columns having methylation information for total coverage
df["Total_Coverage"] = df.iloc[:, 2:10].sum(axis=1)

# Group by strand and CpG, calculate total coverage as a list
#df["strand_cpg"] = df["strand"] + "_" + df["cpg"]  
df["strand_cpg"] = df.iloc[:, 0] + "_" + df.iloc[:, 1]
grouped = df.groupby("strand_cpg")["Total_Coverage"].apply(list).reset_index(name="Coverage_List")

# Calculate median and CV for each group
grouped["Median"] = grouped["Coverage_List"].apply(np.median)
grouped["CV"] = grouped["Coverage_List"].apply(
    lambda x: (np.std(x) / np.mean(x) * 100) if np.mean(x) != 0 else 0
)

# Prepare the output
output = grouped[["strand_cpg", "Median", "CV"]]

# Save the results to a CSV file
output_file = "Median_coverage_and_CV_output.csv" 
output.to_csv(output_file, index=False)
print(f"Results saved to {output_file}")
#print(output)
# Plotting
plt.figure(figsize=(10, 6))
sns.lineplot(data=output, x="strand_cpg", y="Median")
plt.xticks(visible=False)
plt.xticks(ticks=[], labels=[])
#plt.title("Median for CpG Coverage")
plt.xlabel("CpG coordinates")
plt.ylabel("median of coverage")
plt.tight_layout()
plt.savefig("median_coverage.png")

plt.figure(figsize=(10, 6))
sns.lineplot(data=output, x="strand_cpg", y="CV")
plt.xticks(visible=False)
plt.xticks(ticks=[], labels=[])
plt.ylabel("CV (%)")
plt.xlabel("CpGs coordinates")
plt.tight_layout()
plt.savefig("CV_coverage.png")



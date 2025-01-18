from sys import argv
import statistics
import csv
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt

# Initialize storage for data storing
read_depth = defaultdict(list)
variant_fractions = defaultdict(list)

# Open and read the file
_, f,prefix = argv
with open(f, "r") as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        # Extract CpG coordinates and read counts
        strand = row["strand"]
        cpg_coordinates = row["CpG_Coordinates"]
        total_reads = sum(int(row[var]) for var in ["`000", "`001", "`010", "`011", "`100", "`101", "`110", "`111"])
        
        # Skip rows where total reads are zero to avoid division by zero
        if total_reads == 0:
            continue
        
        # Calculate fractions for each variant
        for variant in ["`000", "`001", "`010", "`011", "`100", "`101", "`110", "`111"]:
            site_variant = f"{strand}_{cpg_coordinates}_{variant}"
            read_depth[site_variant].append(int(row[variant]))
            fraction = int(row[variant]) / total_reads
            variant_fractions[site_variant].append(fraction)

# Calculate median read depth and coefficient of variation (CV)
median_read_depth = []
cv_values = []
for site_variant, values in read_depth.items():
    median_depth = statistics.median(values)
    mean_depth = statistics.mean(values)
    stdev_depth = statistics.stdev(values) if len(values) > 1 else 0
    cv = round((stdev_depth / mean_depth) * 100, 2) if mean_depth > 0 else 0
    median_read_depth.append([site_variant, median_depth])
    cv_values.append([site_variant, cv])

# Calculate mean variant read fractions
mean_variant_fractions = []
for site_variant, fractions in variant_fractions.items():
    mean_fraction = round(sum(fractions) / len(fractions), 3)
    mean_variant_fractions.append([site_variant, mean_fraction])

# Save results to a new CSV file
with open(prefix+"_mean_variant_read_fractions.csv", "w", newline="") as output_file:
    writer = csv.writer(output_file)
    writer.writerow(["CpG", "Median_Read_Depth", "CV", "Mean_Variant_Read_Fraction"])
    for i in range(len(median_read_depth)):
        writer.writerow([
            median_read_depth[i][0], 
            median_read_depth[i][1], 
            cv_values[i][1], 
            mean_variant_fractions[i][1]
        ])

# Plot data and save as PNG
cpg_coordinates = [item[0] for item in median_read_depth]
median_depths = [item[1] for item in median_read_depth]
cv_list = [item[1] for item in cv_values]
mean_fractions = [item[1] for item in mean_variant_fractions]

'''#CpG vs Median Read Depth plotting
sns.lineplot(x=cpg_coordinates, y=median_depths)
plt.title(prefix+"CpG vs Median Read Depth")
plt.xticks(visible=False)
plt.xticks(ticks=[], labels=[])
plt.savefig(prefix+"cpg_vs_median_read_depth.png")
plt.clf()

# CpG vs CV 
sns.lineplot(x=cpg_coordinates, y=cv_list)
plt.title("CpG vs CV")
plt.xticks(visible=False)
plt.xticks(ticks=[], labels=[])
plt.savefig(prefix+"cpg_vs_cv.png")
plt.clf()''''

# CpG vs Mean Variant Read Fraction
sns.lineplot(x=cpg_coordinates, y=mean_fractions)
plt.title(prefix+"CpG vs Mean Variant Read Fraction")
plt.xticks(visible=False)
plt.xticks(ticks=[], labels=[])
plt.savefig(prefix+"cpg_vs_mean_variant_read_fraction.png")
plt.clf()

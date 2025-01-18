import sys
import pandas as pd
from sys import argv
_,f=argv

output_file = "selected_columns.csv"  # output file names

# Columns to select
columns_to_select = ["Sample_ID_Replicate",
    "r_10035:10044:10046_`000",
    "r_10035:10044:10140_`000",
    "r_10035:10044:10179_`000",
    "Tissue"
]

try:
    # Read the CSV file
    df = pd.read_csv(f)

    # Check if all specified columns exist in the input file
    missing_columns = [col for col in columns_to_select if col not in df.columns]
    if missing_columns:
        print(f"Error: The following columns are missing in the input file: {missing_columns}")
        sys.exit(1)

    # Select only the specified columns
    selected_df = df[columns_to_select]

    # Saving the dataframe to a new CSV file
    selected_df.to_csv(output_file, index=False)
    print(f"Selected columns saved to {output_file}")

except FileNotFoundError:
    print(f"Error: File {input_file} not found.")
except pd.errors.EmptyDataError:
    print(f"Error: File {input_file} is empty.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

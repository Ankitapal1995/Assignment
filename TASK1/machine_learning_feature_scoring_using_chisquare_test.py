from sys import argv
import pandas as pd
import numpy as np
from sklearn.feature_selection import chi2
from sklearn.preprocessing import MinMaxScaler

# Load the dataset and clean empty columns
_, f = argv  # f is input file
data = pd.read_csv(f)
data.dropna(axis=1, how='all', inplace=True)  # Remove columns with all NaN values
if data.isnull().values.any():
    print("Found NaN values. Filling with 0.")
    data.fillna(0, inplace=True)

# Check for infinite values
'''if np.isinf(data.values).any():
    print("Found infinite values. Replacing with 0.")
    data.replace([np.inf, -np.inf], 0, inplace=True)'''
# Separate features and target
X = data.drop(['Sample_ID_Replicate', 'Tissue'], axis=1)
y = data['Tissue'].apply(lambda x: 0 if x == 'Islet' else 1)

print("Features shape:", X.shape)
print("Target shape:", y.shape)

# Normalize feature values to a [0,1] range (required for chi2)
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Perform Chi-Square test
chi2_scores, p_values = chi2(X_scaled, y)

# Create DataFrame for features and their Chi-Square scores
chi2_importance = pd.DataFrame({
    'Feature': X.columns,
    'Chi2_Score': chi2_scores,
    'P_Value': p_values
})

# Sort features by Chi-Square score in descending order
chi2_importance.sort_values(by='Chi2_Score', ascending=False, inplace=True)

# Save the Chi-Square scores to a CSV file
output_file = "chi2_feature_scores.csv"
chi2_importance.to_csv(output_file, index=False)

print(f"Chi-Square feature scores saved to {output_file}")

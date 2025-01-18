from sys import argv
import pandas as pd
import shap
from xgboost import XGBClassifier
import numpy as np
#Load the dataset and clean empty columns
_, f = argv  # f is the input file
data = pd.read_csv(f)
data.dropna(axis=1, how='all', inplace=True)  # Remove columns with all NaN values

# Separate features and target
X = data.drop(['Sample_ID_Replicate', 'Tissue'], axis=1)
y = data['Tissue'].apply(lambda x: 0 if x == 'Islet' else 1)

print("Features shape:", X.shape)
print("Target shape:", y.shape)

# Initialize and train the XGBoost Classifier
model = XGBClassifier(eval_metric='logloss', use_label_encoder=False)
model.fit(X, y)

#Initialize SHAP TreeExplainer
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

#Calculate mean absolute SHAP values for each feature
mean_shap_values = np.abs(shap_values).mean(axis=0)

#Create DataFrame for feature names and their SHAP importance scores
shap_importance = pd.DataFrame({
    'Feature': X.columns,
    'SHAP_Score': mean_shap_values
})

# Sort features by SHAP score in descending order
shap_importance.sort_values(by='SHAP_Score', ascending=False, inplace=True)

# Save the SHAP scores to a CSV file
output_file = "shap_feature_scores.csv"
shap_importance.to_csv(output_file, index=False)

print(f"SHAP feature scores saved to {output_file}")


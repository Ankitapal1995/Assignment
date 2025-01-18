from sys import argv
s,f=argv  #f is input file
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, cross_val_predict, StratifiedKFold
from sklearn.metrics import (confusion_matrix, roc_auc_score, roc_curve, precision_recall_curve, 
                             accuracy_score, precision_score, recall_score, f1_score, matthews_corrcoef)
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
import shap

# Load the dataset and clean empty columns
data = pd.read_csv(f)  # Replace with your input file path
data.dropna(axis=1, how='all', inplace=True)  # Remove columns with all NaN values

# Separate features and target
X = data.drop(['Sample_ID_Replicate', 'Tissue'], axis=1)
y = data['Tissue']
y = data['Tissue'].apply(lambda x: 0 if x == 'Islet' else 1)
#X = data.iloc[:, 1:-1]  
#y = data.iloc[:, -1]
print(X.shape)
print(y.shape)
# Initialize XGBoost Classifier
model = XGBClassifier(eval_metric='logloss', use_label_encoder=False)
model.fit(X,y)
feature_importance_scores= model.feature_importances_

feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'XGB_Score_Avg': feature_importance_scores,
})

# sorting based on xgboost score
feature_importance.sort_values(by='XGB_Score_Avg', ascending=False, inplace=True)
# saving output file
feature_importance.to_csv('aggregated_feature_importance.csv', index=False)

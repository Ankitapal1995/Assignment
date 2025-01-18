from sys import argv
s,f, k=argv  # f is file and k is fold value i.e for 2 fold k=2.
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
# Cross-validation based the value given by user
fold = int(k)
skf = StratifiedKFold(n_splits=fold, shuffle=True, random_state=42)
y_pred = cross_val_predict(model, X, y, cv=skf, method='predict')
y_pred_proba = cross_val_predict(model, X, y, cv=skf, method='predict_proba')[:, 1]
cm = confusion_matrix(y, y_pred)
sensitivity = cm[0, 0] / (cm[0, 0] + cm[0, 1])
specificity = cm[1, 1] / (cm[1, 1] + cm[1, 0])
precision = precision_score(y, y_pred, average='binary')
recall = recall_score(y, y_pred, average='binary')
f1 = f1_score(y, y_pred, average='binary')
npv = cm[1,1]/(cm[1,1]+cm[0,1]) 
mcc = matthews_corrcoef(y, y_pred)
auc = roc_auc_score(y, y_pred_proba)

print(f'cm: {cm}')
print(f'sensitivity: {sensitivity}')
print(f'specificity: {specificity}')
print(f'precision: {precision}')
print(f'npv: {npv}')
print(f'recall: {recall}')
print(f'f1 score: {f1}')
print(f'mcc: {mcc}')
print(f'auc: {auc}')


# ROC and Precision-Recall curves
fpr, tpr, _ = roc_curve(y, y_pred_proba)
precision_vals, recall_vals, _ = precision_recall_curve(y, y_pred_proba)
plt.figure(1)
plt.plot(fpr, tpr, label=f'{fold}-fold ROC (AUC = {auc:.2f})')
plt.figure(2)
plt.plot(recall_vals, precision_vals, label=f'{fold}-fold PR Curve')

# Plot Combined ROC and PR Curves
plt.figure(1)
plt.title('ROC Curves')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend()
plt.savefig('2fold_roc_curves.png')
plt.close()

plt.figure(2)
plt.title('Precision-Recall Curves')
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.legend()
plt.savefig('2fold_precision_recall_curves.png')
plt.close()


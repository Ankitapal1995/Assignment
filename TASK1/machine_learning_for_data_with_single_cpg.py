from sys import argv
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import (roc_auc_score, classification_report,confusion_matrix, roc_curve, auc)
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
import shap

# Load dataset 
s,f=argv  # f is input file
data = pd.read_csv(f)

# Sum up counts across methylation patterns to compute coverage
data['Coverage'] = data.iloc[:, 2:10].sum(axis=1)

# Prepare feature matrix (X) and target variable (y)
X = data.iloc[:, 2:10].values  # Methylation pattern columns
y = data['Tissue'].apply(lambda x: 1 if x == 'Islet' else 0).values

# Stratified train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f'X-train shape {X_train.shape}')
print(f'y-train shape {y_train.shape}')
print(f'X-test shape {X_test.shape}')
print(f'y_test shape {y_test.shape}')

# Define individual models
xgb = XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')
xgb.fit(X_train, y_train)


# Predictions and Probabilities
y_pred_proba = xgb.predict_proba(X_test)[:, 1]
y_pred = xgb.predict(X_test)

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)

# model evaluation
sensitivity = cm[1, 1] / (cm[1, 1] + cm[1, 0])
print(f"Sensitivity: {sensitivity:.2f}")

specificity = cm[0, 0] / (cm[0, 0] + cm[0, 1])
print(f"Specificity: {specificity:.2f}")

fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
roc_auc = auc(fpr, tpr)
print(f"ROC-AUC Score: {roc_auc:.2f}")

# Plot ROC Curve
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {roc_auc:.2f})")
plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.savefig("roc_curve.png")
plt.show()

# Classification Report
print("Classification Report:")
print(classification_report(y_test, y_pred))



# -*- coding: utf-8 -*-
"""assignment2

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SzgyxG6hHJcq0s18vS1mLFMNzyJRqjze
"""

from google.colab import files
uploaded= files.upload()

# STEP 2: Install and import necessary libraries
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import mutual_info_classif
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
import matplotlib.pyplot as plt
import seaborn as sns

# STEP 2: Load the dataset
import io
df = pd.read_excel(io.BytesIO(uploaded['h1b_visa.xlsx']))
df.head()

# Remove missing CASE_STATUS
df = df.dropna(subset=['CASE_STATUS'])

# Convert CASE_STATUS to string
df['CASE_STATUS'] = df['CASE_STATUS'].astype(str)

# Split on '-' if exists, keep first part
df['CASE_STATUS'] = df['CASE_STATUS'].str.split('-').str[0]

# Keep only CERTIFIED and DENIED
df = df[df['CASE_STATUS'].isin(['CERTIFIED', 'DENIED'])]

# Drop any remaining rows with missing values
df = df.dropna()

print(df.shape)
print(df['CASE_STATUS'].value_counts())

# Encode target
df['CASE_STATUS'] = LabelEncoder().fit_transform(df['CASE_STATUS'])  # CERTIFIED=0, DENIED=1

# Encode categorical columns
categorical_features = ['EMPLOYER_NAME', 'SOC_NAME', 'JOB_TITLE', 'FULL_TIME_POSITION', 'WORKSITE']
for col in categorical_features:
    df[col] = LabelEncoder().fit_transform(df[col])

X = df.drop(columns=['CASE_STATUS'])
y = df['CASE_STATUS']

# split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# STEP 3: Information Gain (Mutual Information) calculation
info_gain = mutual_info_classif(X_train, y_train, discrete_features='auto')
info_gain_df = pd.DataFrame({'Feature': X.columns, 'InfoGain': info_gain})
info_gain_df = info_gain_df.sort_values(by='InfoGain', ascending=False)
info_gain_df

# STEP 4: Train models and evaluate based on different thresholds

thresholds = [0, 0.01, 0.05, 0.1]
results = []

for thresh in thresholds:
    selected_features = info_gain_df[info_gain_df['InfoGain'] > thresh]['Feature'].values

    if len(selected_features) == 0:
        # Skip this threshold if no features selected
        continue

    X_train_sel = X_train[selected_features]
    X_test_sel = X_test[selected_features]

    # Decision Tree
    dt = DecisionTreeClassifier(random_state=42)
    dt.fit(X_train_sel, y_train)
    dt_pred = dt.predict(X_test_sel)

    # k-NN
    knn = KNeighborsClassifier()
    knn.fit(X_train_sel, y_train)
    knn_pred = knn.predict(X_test_sel)

    # Naive Bayes
    nb = GaussianNB()
    nb.fit(X_train_sel, y_train)
    nb_pred = nb.predict(X_test_sel)

    for model_name, pred in zip(['Decision Tree', 'k-NN', 'Naive Bayes'], [dt_pred, knn_pred, nb_pred]):
        results.append({
            'Threshold': thresh,
            'Model': model_name,
            'Accuracy': accuracy_score(y_test, pred),
            'Precision': precision_score(y_test, pred, zero_division=0),
            'Recall': recall_score(y_test, pred, zero_division=0)
        })

# STEP 5: Visualize results
results_df = pd.DataFrame(results)

plt.figure(figsize=(12, 6))
sns.lineplot(data=results_df, x='Threshold', y='Accuracy', hue='Model', marker='o')
plt.title('Accuracy vs. Information Gain Threshold')
plt.grid(True)
plt.show()

plt.figure(figsize=(12, 6))
sns.lineplot(data=results_df, x='Threshold', y='Precision', hue='Model', marker='o')
plt.title('Precision vs. Information Gain Threshold')
plt.grid(True)
plt.show()

plt.figure(figsize=(12, 6))
sns.lineplot(data=results_df, x='Threshold', y='Recall', hue='Model', marker='o')
plt.title('Recall vs. Information Gain Threshold')
plt.grid(True)
plt.show()

from sklearn.feature_selection import mutual_info_classif
# Calculate Information Gain
info_gain = mutual_info_classif(X_train, y_train, discrete_features='auto')

# Create a DataFrame to store the Information Gain for each feature
info_gain_df = pd.DataFrame({'Feature': X.columns, 'InfoGain': info_gain})

# Sort the features by Information Gain
info_gain_df = info_gain_df.sort_values(by='InfoGain', ascending=False)

# Display the result
print(info_gain_df)

thresholds = [0, 0.001, 0.005, 0.1]
selected_features_dict = {}

for thresh in thresholds:
    # Select features with Information Gain above the threshold
    selected_features = info_gain_df[info_gain_df['InfoGain'] > thresh]['Feature'].values
    selected_features_dict[thresh] = selected_features

    print(f"Features selected for threshold {thresh}: {selected_features}")

# Loop through different thresholds and create subsets of features
for thresh in thresholds:
    selected_features = selected_features_dict[thresh]
    X_train_sel = X_train[selected_features]
    X_test_sel = X_test[selected_features]

    print(f"Training and testing data for threshold {thresh} prepared.")

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Initialize results list to store model performance metrics
results = []

# Define the thresholds you want to evaluate
thresholds = [0.000, 0.001, 0.005, 0.01]

for thresh in thresholds:
    # Select features based on the threshold of Information Gain
    selected_features = info_gain_df[info_gain_df['InfoGain'] > thresh]['Feature'].values

    if len(selected_features) == 0:
        print(f"No features selected for threshold: {thresh}")
        continue  # Skip this threshold if no features are selected

    # Filter training and testing data to include only the selected features
    X_train_sel = X_train[selected_features]
    X_test_sel = X_test[selected_features]

    # Train Decision Tree model
    dt = DecisionTreeClassifier(random_state=42)
    dt.fit(X_train_sel, y_train)
    dt_pred = dt.predict(X_test_sel)

    # Train k-NN model
    knn = KNeighborsClassifier()
    knn.fit(X_train_sel, y_train)
    knn_pred = knn.predict(X_test_sel)

    # Train Naive Bayes model
    nb = GaussianNB()
    nb.fit(X_train_sel, y_train)
    nb_pred = nb.predict(X_test_sel)

    # Store results for each model
    for model_name, pred in zip(['Decision Tree', 'k-NN', 'Naive Bayes'], [dt_pred, knn_pred, nb_pred]):
        results.append({
            'Threshold': thresh,
            'Model': model_name,
            'Accuracy': accuracy_score(y_test, pred),
            'Precision': precision_score(y_test, pred, average='macro', zero_division=0),
            'Recall': recall_score(y_test, pred, average='macro', zero_division=0)
        })

# Convert the results into a DataFrame
results_df = pd.DataFrame(results)

# Display the results
print(results_df)

# Train and evaluate models using the full feature set (without feature selection)

# Full feature set (all columns in the dataset)
X_train_full = X_train
X_test_full = X_test

# Train Decision Tree model
dt_full = DecisionTreeClassifier(random_state=42)
dt_full.fit(X_train_full, y_train)
dt_full_pred = dt_full.predict(X_test_full)

# Train k-NN model
knn_full = KNeighborsClassifier()
knn_full.fit(X_train_full, y_train)
knn_full_pred = knn_full.predict(X_test_full)

# Train Naive Bayes model
nb_full = GaussianNB()
nb_full.fit(X_train_full, y_train)
nb_full_pred = nb_full.predict(X_test_full)

# Store results for the full feature set
results_full = []
for model_name, pred in zip(['Decision Tree', 'k-NN', 'Naive Bayes'], [dt_full_pred, knn_full_pred, nb_full_pred]):
    results_full.append({
        'Threshold': 'Full Set',  # Label the full feature set
        'Model': model_name,
        'Accuracy': accuracy_score(y_test, pred),
        'Precision': precision_score(y_test, pred, average='macro', zero_division=0),
        'Recall': recall_score(y_test, pred, average='macro', zero_division=0)
    })

# Convert the results for full feature set into a DataFrame
results_full_df = pd.DataFrame(results_full)

# Append full feature results to the previous results DataFrame
results_df = pd.concat([results_df, results_full_df], ignore_index=True)

# Display the final results
print(results_df)

# Convert "Full Set" to 0 in the 'Threshold' column for visualization
results_df['Threshold'] = pd.to_numeric(results_df['Threshold'], errors='coerce')
results_df['Threshold'].fillna(0, inplace=True)  # Replace "Full Set" with 0

# Now, plot again
plt.figure(figsize=(12, 6))
sns.lineplot(data=results_df, x='Threshold', y='Accuracy', hue='Model', marker='o')
plt.title('Accuracy vs. Information Gain Threshold')
plt.grid(True)
plt.show()

# Plot Precision vs. Threshold
plt.figure(figsize=(12, 6))
sns.lineplot(data=results_df, x='Threshold', y='Precision', hue='Model', marker='o')
plt.title('Precision vs. Information Gain Threshold')
plt.grid(True)
plt.show()

# Plot Recall vs. Threshold
plt.figure(figsize=(12, 6))
sns.lineplot(data=results_df, x='Threshold', y='Recall', hue='Model', marker='o')
plt.title('Recall vs. Information Gain Threshold')
plt.grid(True)
plt.show()

# Creating a DataFrame to store the performance metrics for comparison
performance_df = pd.DataFrame({
    'Threshold': results_df['Threshold'],
    'Model': results_df['Model'],
    'Accuracy': results_df['Accuracy'],
    'Precision': results_df['Precision'],
    'Recall': results_df['Recall']
})

# Now let's compare the performance for each model using the full feature set and different thresholds

# Group by model and compare performance across different thresholds
performance_comparison = performance_df.groupby('Model').agg({
    'Accuracy': ['mean', 'max', 'min'],
    'Precision': ['mean', 'max', 'min'],
    'Recall': ['mean', 'max', 'min']
}).reset_index()

# Display the comparison
print(performance_comparison)

# Optional: To better visualize the comparison, we can plot it
plt.figure(figsize=(12, 6))
sns.lineplot(data=performance_df, x='Threshold', y='Accuracy', hue='Model', marker='o')
plt.title('Comparison of Model Accuracy with Different Feature Sets')
plt.xlabel('Threshold')
plt.ylabel('Accuracy')
plt.grid(True)
plt.show()

plt.figure(figsize=(12, 6))
sns.lineplot(data=performance_df, x='Threshold', y='Precision', hue='Model', marker='o')
plt.title('Comparison of Model Precision with Different Feature Sets')
plt.xlabel('Threshold')
plt.ylabel('Precision')
plt.grid(True)
plt.show()

plt.figure(figsize=(12, 6))
sns.lineplot(data=performance_df, x='Threshold', y='Recall', hue='Model', marker='o')
plt.title('Comparison of Model Recall with Different Feature Sets')
plt.xlabel('Threshold')
plt.ylabel('Recall')
plt.grid(True)
plt.show()

# We will create a function to find the best threshold for each model based on a specific metric

def get_best_threshold_for_model(model_name, metric):
    # Filter results for the given model
    model_results = performance_df[performance_df['Model'] == model_name]

    # Get the threshold corresponding to the maximum value of the chosen metric (Accuracy, Precision, or Recall)
    best_threshold = model_results.loc[model_results[metric].idxmax()]

    return best_threshold

# Find the best threshold based on Accuracy for each model
best_accuracy_dt = get_best_threshold_for_model('Decision Tree', 'Accuracy')
best_accuracy_knn = get_best_threshold_for_model('k-NN', 'Accuracy')
best_accuracy_nb = get_best_threshold_for_model('Naive Bayes', 'Accuracy')

# Find the best threshold based on Precision for each model
best_precision_dt = get_best_threshold_for_model('Decision Tree', 'Precision')
best_precision_knn = get_best_threshold_for_model('k-NN', 'Precision')
best_precision_nb = get_best_threshold_for_model('Naive Bayes', 'Precision')

# Find the best threshold based on Recall for each model
best_recall_dt = get_best_threshold_for_model('Decision Tree', 'Recall')
best_recall_knn = get_best_threshold_for_model('k-NN', 'Recall')
best_recall_nb = get_best_threshold_for_model('Naive Bayes', 'Recall')

# Print the best thresholds for each model based on each metric
print(f"Best Threshold for Accuracy (Decision Tree): {best_accuracy_dt['Threshold']}, Accuracy: {best_accuracy_dt['Accuracy']}")
print(f"Best Threshold for Accuracy (k-NN): {best_accuracy_knn['Threshold']}, Accuracy: {best_accuracy_knn['Accuracy']}")
print(f"Best Threshold for Accuracy (Naive Bayes): {best_accuracy_nb['Threshold']}, Accuracy: {best_accuracy_nb['Accuracy']}")

print(f"Best Threshold for Precision (Decision Tree): {best_precision_dt['Threshold']}, Precision: {best_precision_dt['Precision']}")
print(f"Best Threshold for Precision (k-NN): {best_precision_knn['Threshold']}, Precision: {best_precision_knn['Precision']}")
print(f"Best Threshold for Precision (Naive Bayes): {best_precision_nb['Threshold']}, Precision: {best_precision_nb['Precision']}")

print(f"Best Threshold for Recall (Decision Tree): {best_recall_dt['Threshold']}, Recall: {best_recall_dt['Recall']}")
print(f"Best Threshold for Recall (k-NN): {best_recall_knn['Threshold']}, Recall: {best_recall_knn['Recall']}")
print(f"Best Threshold for Recall (Naive Bayes): {best_recall_nb['Threshold']}, Recall: {best_recall_nb['Recall']}")

import matplotlib.pyplot as plt
import seaborn as sns

# Plot Accuracy vs. Threshold
plt.figure(figsize=(12, 6))
sns.lineplot(data=results_df, x='Threshold', y='Accuracy', hue='Model', marker='o')
plt.title('Accuracy vs. Information Gain Threshold')
plt.xlabel('Information Gain Threshold')
plt.ylabel('Accuracy')
plt.grid(True)
plt.show()

# Plot Precision vs. Threshold
plt.figure(figsize=(12, 6))
sns.lineplot(data=results_df, x='Threshold', y='Precision', hue='Model', marker='o')
plt.title('Precision vs. Information Gain Threshold')
plt.xlabel('Information Gain Threshold')
plt.ylabel('Precision')
plt.grid(True)
plt.show()

# Plot Recall vs. Threshold
plt.figure(figsize=(12, 6))
sns.lineplot(data=results_df, x='Threshold', y='Recall', hue='Model', marker='o')
plt.title('Recall vs. Information Gain Threshold')
plt.xlabel('Information Gain Threshold')
plt.ylabel('Recall')
plt.grid(True)
plt.show()
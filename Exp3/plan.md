# Plan for Experiment 3: Heart Disease Classification using Decision Trees and Random Forests

## 1. Objective
Apply Decision Tree and Random Forest algorithms to classify patients as having heart disease or not, using the provided dataset.

## 2. Dataset Overview
- **Path**: `Exp3/archive/heart.csv`
- **Features**: 
    - `age`: Age in years
    - `sex`: (1 = male; 0 = female)
    - `cp`: Chest pain type
    - `trestbps`: Resting blood pressure
    - `chol`: Serum cholestoral in mg/dl
    - `fbs`: Fasting blood sugar > 120 mg/dl
    - `restecg`: Resting electrocardiographic results
    - `thalach`: Maximum heart rate achieved
    - `exang`: Exercise induced angina
    - `oldpeak`: ST depression induced by exercise relative to rest
    - `slope`: The slope of the peak exercise ST segment
    - `ca`: Number of major vessels (0-3) colored by flourosopy
    - `thal`: 3 = normal; 6 = fixed defect; 7 = reversable defect
- **Target**: `target` (1 = disease, 0 = no disease)

## 3. Implementation Plan

### Step 1: Setup and Data Loading
- Import necessary libraries: `pandas`, `numpy`, `matplotlib`, `seaborn`, `sklearn`.
- Load the dataset using pandas.
- Display the first few rows (`head()`) and check the shape of the data.

### Step 2: Exploratory Data Analysis (EDA)
- Check for missing values (`isnull().sum()`).
- Check data types (`info()`).
- Analyze the distribution of the target variable (`value_counts()`).
- Visualize correlations using a heatmap (`sns.heatmap`).
- Visualize relationships between key features and the target.

### Step 3: Data Preprocessing
- Handle missing values (if any).
- Split the dataset into features (`X`) and target (`y`).
- Split the data into training and testing sets (e.g., 80% train, 20% test) using `train_test_split`.
- (Optional) Feature scaling - Note: Decision Trees and Random Forests are generally robust to unscaled data, but it's good practice to be aware of.

### Step 4: Model 1 - Decision Tree Classifier
- Initialize `DecisionTreeClassifier` (e.g., with `entropy` or `gini` criterion).
- Train the model on the training set.
- Predict on the test set.
- Evaluate performance:
    - **Accuracy Score**
    - **Confusion Matrix**
    - **Classification Report** (Precision, Recall, F1-Score)
- Visualize the Decision Tree using `export_graphviz` or `plot_tree`.

### Step 5: Model 2 - Random Forest Classifier
- Initialize `RandomForestClassifier` (e.g., `n_estimators=100`).
- Train the model on the training set.
- Predict on the test set.
- Evaluate performance:
    - **Accuracy Score**
    - **Confusion Matrix**
    - **Classification Report**

### Step 6: Comparison and Conclusion
- Compare the accuracy and other metrics of both models.
- Discuss which model performed better and why (e.g., Random Forest typically reduces overfitting compared to a single Decision Tree).
- Analyze feature importance provided by the Random Forest model to see which factors contribute most to heart disease prediction.

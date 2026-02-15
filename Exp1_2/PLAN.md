# Plan for Linear, Logistic, and Regularization Experiments (Exp 1 & 2)

This plan outlines the implementation of regression and classification models using `insurance.csv` and `bank.csv`.

## Experiment 1: Linear and Logistic Regression (File 1)

**File Name:** `Exp1_2/1_Linear_Logistic_Regression.ipynb`

### Part A: Simple Linear Regression
*   **Dataset:** `insurance.csv` (Regression task).
*   **Goal:** Predict `expenses` using a single feature (e.g., `bmi` or `age`).
*   **Steps:**
    1.  **Load Data:** Import `pandas`, load `insurance.csv`.
    2.  **Visualization:** Plot a scatter plot of `bmi` vs `expenses` to see the relationship.
    3.  **Preprocessing:** Select `X` (`bmi`) and `y` (`expenses`). No complex encoding needed for this simple case.
    4.  **Split:** Use `train_test_split` (80% train, 20% test).
    5.  **Model:**
        *   Import `LinearRegression` from `sklearn.linear_model`.
        *   Instantiate and fit the model on the training set.
    6.  **Evaluation:**
        *   Predict on the test set.
        *   Calculate **Mean Squared Error (MSE)** and **R2 Score**.
        *   Plot the regression line over the scatter plot.

### Part B: Logistic Regression
*   **Dataset:** `bank.csv` (Classification task).
*   **Goal:** Predict if a client will subscribe to a term deposit (`deposit` column).
*   **Steps:**
    1.  **Load Data:** Load `bank.csv`.
    2.  **Preprocessing:**
        *   Check for missing values.
        *   **Encoding:** Convert categorical features (`job`, `marital`, `education`, etc.) into numbers using `pd.get_dummies(drop_first=True)`.
        *   **Target:** Ensure `deposit` is binary (0/1).
    3.  **Split:** Use `train_test_split`.
    4.  **Model:**
        *   Import `LogisticRegression` from `sklearn.linear_model`.
        *   Instantiate (consider increasing `max_iter` if convergence warning appears) and fit.
    5.  **Evaluation:**
        *   Predict on the test set.
        *   Calculate **Accuracy Score**.
        *   Display **Confusion Matrix** (use `seaborn.heatmap`).
        *   Print **Classification Report**.

---

## Experiment 2: Multiple, Lasso, and Ridge Regression (File 2)

**File Name:** `Exp1_2/2_Multi_Lasso_Ridge_Regression.ipynb`

### Setup
*   **Dataset:** `insurance.csv`.
*   **Goal:** Predict `expenses` using **all valid features** and compare Regularization techniques.

### Steps
1.  **Data Preprocessing (Common for all models):**
    *   **Load Data:** Load `insurance.csv`.
    *   **Encoding:** One-hot encode categorical columns: `sex`, `smoker`, `region`. Drop first to avoid dummy variable trap.
    *   **Feature Selection:** Use all features (`age`, `bmi`, `children`, plus encoded columns).
    *   **Splitting:** Split data into Train and Test sets.
    *   **Scaling (CRITICAL):**
        *   Import `StandardScaler` from `sklearn.preprocessing`.
        *   Fit scaler on **Training Data** and transform both Train and Test data.
        *   *Why?* Regularization (Lasso/Ridge) is sensitive to the scale of input features.

2.  **Model 1: Multiple Linear Regression**
    *   Train a standard `LinearRegression` model.
    *   Evaluate using MSE and R2 Score on the test set.

3.  **Model 2: Lasso Regression (L1)**
    *   Import `Lasso` from `sklearn.linear_model`.
    *   Try a default `alpha=1.0` or small value like `0.1`.
    *   Fit the model.
    *   Evaluate MSE and R2.
    *   **Analysis:** Check which coefficients are reduced to zero (feature selection property).

4.  **Model 3: Ridge Regression (L2)**
    *   Import `Ridge` from `sklearn.linear_model`.
    *   Try `alpha=1.0`.
    *   Fit the model.
    *   Evaluate MSE and R2.

5.  **Comparison & Visualization:**
    *   Create a DataFrame to compare the R2 scores of all three models.
    *   (Optional) Plot the coefficients of the three models to see how Lasso shrinks them to zero vs Ridge.

---
## Coding Instructions for Both Files

*   **Imports:**
    ```python
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression, LogisticRegression, Lasso, Ridge
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, confusion_matrix, classification_report
    ```
*   **Visualization:** Use `matplotlib` and `seaborn` for clear plots.
*   **Reproducibility:** Set `random_state=42` in `train_test_split` to ensure consistent results.

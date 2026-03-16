import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


def load_data(path):
    df = pd.read_csv(path)
    return df


def build_pipeline():
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("svc", SVC())
    ])
    return pipe


def get_param_grid():
    param_grid = [
        {
            'svc__kernel': ['linear'],
            'svc__C': [0.01, 0.1, 1, 10, 100]
        },
        {
            'svc__kernel': ['rbf'],
            'svc__C': [0.1, 1, 10, 100],
            'svc__gamma': ['scale', 'auto', 0.01, 0.001]
        },
        {
            'svc__kernel': ['poly'],
            'svc__C': [0.1, 1, 10],
            'svc__degree': [2, 3]
        }
    ]
    return param_grid


def main():
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, 'diabetes.csv')

    df = load_data(csv_path)

    if 'Outcome' not in df.columns:
        raise ValueError("Expected target column 'Outcome' in dataset")

    X = df.drop(columns=['Outcome'])
    y = df['Outcome']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = build_pipeline()
    param_grid = get_param_grid()

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    gs = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        scoring='accuracy',
        cv=cv,
        n_jobs=-1,
        verbose=1
    )

    print('Running GridSearchCV for SVM...')
    gs.fit(X_train, y_train)

    print('\nBest parameters:')
    print(gs.best_params_)
    print('\nBest CV score: {:.4f}'.format(gs.best_score_))

    best = gs.best_estimator_
    y_pred = best.predict(X_test)

    print('\nTest Accuracy: {:.4f}'.format(accuracy_score(y_test, y_pred)))
    print('\nClassification Report:')
    print(classification_report(y_test, y_pred))
    print('\nConfusion Matrix:')
    print(confusion_matrix(y_test, y_pred))

    model_path = os.path.join(base_dir, 'svm_diabetes_model.joblib')
    joblib.dump(gs.best_estimator_, model_path)
    print(f"Saved best model to {model_path}")


if __name__ == '__main__':
    main()

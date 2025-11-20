import numpy as np
from sklearn.impute import KNNImputer

def treat_missing_values(df):
    # Median
    for col in [" BMI ", "Polio", "Income composition of resources"]:
        df[col].fillna(df[col].median(), inplace=True)

    # KNN imputation
    imputer = KNNImputer()
    numeric_cols = df.select_dtypes(include="number").columns

    df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
    return df

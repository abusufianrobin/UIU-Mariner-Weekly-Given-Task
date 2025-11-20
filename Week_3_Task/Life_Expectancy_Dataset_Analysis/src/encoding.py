import pandas as pd

def encode_categorical(df):
    df = pd.get_dummies(df, columns=["Country", "Status"], drop_first=True)
    return df

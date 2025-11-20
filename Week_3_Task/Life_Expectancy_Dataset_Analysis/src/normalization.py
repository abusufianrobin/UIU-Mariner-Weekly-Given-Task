from sklearn.preprocessing import MinMaxScaler

def normalize_data(df):
    scaler = MinMaxScaler()
    num_cols = df.select_dtypes(include="number").columns
    df[num_cols] = scaler.fit_transform(df[num_cols])
    return df



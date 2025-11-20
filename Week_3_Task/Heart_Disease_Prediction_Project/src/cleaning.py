def clean_dataset(df):
    print("\nDuplicate Rows Found:", df.duplicated().any())
    df = df.drop_duplicates()
    print("New Shape After Removing Duplicates:", df.shape)

    print("\nStatistics Summary:")
    print(df.describe())

    return df

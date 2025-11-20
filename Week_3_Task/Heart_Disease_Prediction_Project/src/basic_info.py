def dataset_overview(df):
    print("\nTop 5 Rows:\n", df.head())
    print("\nLast 5 Rows:\n", df.tail())

    print("\nDataset Shape:", df.shape)
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    print("\nDataset Info:")
    print(df.info())

    print("\nNull Values:")
    print(df.isnull().sum())
    print("\nStatistical Summary:\n", df.describe())


    
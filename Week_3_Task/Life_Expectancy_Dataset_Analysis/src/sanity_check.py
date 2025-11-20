def sanity_check(df):
    print("\nShape:", df.shape)
    print("\nInfo:")
    print(df.info())

    print("\nMissing values:")
    print(df.isnull().sum())
    print("\nMissing %:")
    print(df.isnull().sum() / df.shape[0] * 100)

    print("\nDuplicated rows:", df.duplicated().sum())

    print("\nGarbage values (categorical counts):")
    for col in df.select_dtypes(include="object").columns:
        print(df[col].value_counts())
        print("***" * 10)

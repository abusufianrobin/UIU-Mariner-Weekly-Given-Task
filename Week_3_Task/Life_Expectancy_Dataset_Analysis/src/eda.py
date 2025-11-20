import seaborn as sns
import matplotlib.pyplot as plt

def run_eda(df):
    print("\nNumerical Summary:")
    print(df.describe().T)

    print("\nCategorical Summary:")
    print(df.describe(include="object"))

    # Histograms
    for col in df.select_dtypes(include="number"):
        sns.histplot(df[col])
        plt.title(f"Distribution: {col}")
        plt.show()

    # Boxplots
    for col in df.select_dtypes(include="number"):
        sns.boxplot(df[col])
        plt.title(f"Outliers in: {col}")
        plt.show()

    # Correlation Heatmap
    corr = df.select_dtypes(include="number").corr()
    sns.heatmap(corr)
    plt.show()

    plt.figure(figsize=(15, 15))
    sns.heatmap(corr, annot=True)
    plt.show()



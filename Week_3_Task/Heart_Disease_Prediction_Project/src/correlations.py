import seaborn as sns
import matplotlib.pyplot as plt

def plot_correlation(df):
    plt.figure(figsize=(15, 6))
    sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
    plt.title("Correlation Matrix")
    plt.show()

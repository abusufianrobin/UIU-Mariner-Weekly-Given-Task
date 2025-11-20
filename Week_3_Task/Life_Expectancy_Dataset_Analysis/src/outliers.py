import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def whisker_bounds(col):
    q1, q3 = np.percentile(col, [25, 75])
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr

def treat_outliers(df):
    cols_to_fix = ['GDP', 'Total expenditure', ' thinness  1-19 years', ' thinness 5-9 years']

    for col in cols_to_fix:
        lower, upper = whisker_bounds(df[col])
        df[col] = np.clip(df[col], lower, upper)

    # Optional: visualize
    for col in cols_to_fix:
        sns.boxplot(df[col])
        plt.title(f"Outlier treated: {col}")
        plt.show()

    return df

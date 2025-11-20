import seaborn as sns
import matplotlib.pyplot as plt

def age_distribution(df):
    sns.histplot(df['age'], bins=20, kde=True)
    plt.title("Age Distribution")
    plt.show()

def chest_pain_type(df):
    sns.countplot(x='cp', data=df, palette='viridis')
    plt.xticks([0,1,2,3], ["Typical", "Atypical", "Non-anginal", "Asymptomatic"], rotation=75)
    plt.title("Chest Pain Type Distribution")
    plt.show()

def chest_pain_vs_target(df):
    sns.countplot(x='cp', hue='target', data=df)
    plt.title("Chest Pain vs Target")
    plt.show()

def fbs_vs_target(df):
    sns.countplot(x='fbs', hue='target', data=df)
    plt.title("Fasting Blood Sugar vs Target")
    plt.show()

def resting_bp(df):
    df['trestbps'].hist()
    plt.title("Resting Blood Pressure")
    plt.show()

def resting_bp_by_sex(df):
    g = sns.FacetGrid(df, hue="sex", aspect=4)
    g.map(sns.kdeplot, 'trestbps', shade=True)
    plt.legend(labels=['Male', 'Female'])
    plt.title("Resting BP by Sex")
    plt.show()

def cholesterol_distribution(df):
    df['chol'].hist()
    plt.title("Serum Cholesterol Distribution")
    plt.show()

def plot_continuous(df):
    cate_val = []
    cont_val = []

    for col in df.columns:
        if df[col].nunique() <= 10:
            cate_val.append(col)
        else:
            cont_val.append(col)

    print("Categorical Columns:", cate_val)
    print("Continuous Columns:", cont_val)

    df[cont_val].hist(figsize=(15, 6))
    plt.tight_layout()
    plt.show()

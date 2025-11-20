import seaborn as sns
import matplotlib.pyplot as plt

def target_distribution(df):
    counts = df['target'].value_counts()
    print("\nHeart Disease Counts:\n", counts)

    sns.barplot(x=counts.index, y=counts.values, palette=['green', 'red'])
    plt.xticks([0, 1], ['No', 'Yes'])
    plt.title("Heart Disease Distribution")
    plt.show()

def sex_distribution(df):
    counts = df['sex'].value_counts()
    print("\nMale/Female Count:", counts)

    sns.barplot(x=counts.index, y=counts.values, palette=['orange', 'blue'])
    plt.xticks([0, 1], ['Female', 'Male'])
    plt.title("Sex Distribution")
    plt.show()

def sex_vs_target(df):
    sns.countplot(x='sex', hue='target', data=df)
    plt.xticks([1, 0], ['Male', 'Female'])
    plt.legend(labels=['No Disease', 'Disease'])
    plt.title("Gender vs Target")
    plt.show()

from .loader import load_data
from .basic_info import dataset_overview
from .cleaning import clean_dataset
from .correlations import plot_correlation
from .eda import target_distribution, sex_distribution, sex_vs_target
from .charts import (
    age_distribution, chest_pain_type, chest_pain_vs_target,
    fbs_vs_target, resting_bp, resting_bp_by_sex,
    cholesterol_distribution, plot_continuous
)
from .config import PROCESSED_PATH

def run_pipeline():
    df = load_data()

    dataset_overview(df)
    df = clean_dataset(df)

    plot_correlation(df)

    target_distribution(df)
    sex_distribution(df)
    sex_vs_target(df)
    age_distribution(df)
    chest_pain_type(df)
    chest_pain_vs_target(df)
    fbs_vs_target(df)
    resting_bp(df)
    resting_bp_by_sex(df)
    cholesterol_distribution(df)
    plot_continuous(df)

    df.to_csv(PROCESSED_PATH, index=False)
    print(f"Processed data saved at: {PROCESSED_PATH}")

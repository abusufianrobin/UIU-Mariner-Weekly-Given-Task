from .loader import load_data
from .sanity_check import sanity_check
from .eda import run_eda
from .missing_values import treat_missing_values
from .outliers import treat_outliers
from .duplicates_garbage import remove_duplicates_and_garbage
from .normalization import normalize_data
from .encoding import encode_categorical
from .config import PROCESSED_PATH

def run_pipeline():
    df = load_data()

    sanity_check(df)
    run_eda(df)

    df = treat_missing_values(df)
    df = treat_outliers(df)
    df = remove_duplicates_and_garbage(df)
    df = normalize_data(df)
    df = encode_categorical(df)

    df.to_csv(PROCESSED_PATH, index=False)
    print(f"\nPreprocessed file saved at: {PROCESSED_PATH}")



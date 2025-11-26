import pandas as pd
from sqlalchemy import create_engine

def read_students_pandas():
    engine = create_engine(
        "mysql+pymysql://root:AJecDSgxvS8eai4#@localhost:3306/Team_AURA"
    )
    df = pd.read_sql("SELECT * FROM students", engine)
    print("\n--- Pandas DataFrame ---")
    print(df)
    return df

def export_to_csv(filename="students.csv"):
    df = read_students_pandas()
    df.to_csv(filename, index=False)
    print(f"Data exported to {filename}")

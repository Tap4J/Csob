import numpy as np

def value_counts(df):
    for column in df.columns:
        print(f"Value counts for column '{column}':")
        print(df[column].value_counts())
        print("\n")

def missing_values(df):
    for column in df.columns:
        pct_missing = np.mean(df[column].isnull()) *100
        print('{} - {}%'.format(column, pct_missing))
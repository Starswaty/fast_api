import pandas as pd
from pandas.tseries.offsets import QuarterEnd
import numpy as np

# Helper function to clean NaN and infinity values
def clean_df(df):
    # Replace NaN values with None (or 0, if you prefer)
    df = df.replace({np.nan: None, np.inf: None, -np.inf: None})
    return df

def load_and_filter_by_quarter(file_path, date_column, quarter_str):
    quarter_end = pd.Timestamp(quarter_str) + QuarterEnd(0)
    target_date = quarter_end - pd.Timedelta(days=90)
    df = pd.read_excel(file_path)
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    df = clean_df(df)  # Clean NaN and infinite values
    return df[df[date_column] >= target_date]

def get_zero_interest_accounts(file_path, int_rate_col):
    df = pd.read_excel(file_path)
    df = clean_df(df)  # Clean NaN and infinite values
    return df[df[int_rate_col] == 0]


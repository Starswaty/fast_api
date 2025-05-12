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
    df = clean_df(df)
    return df[df[date_column] >= target_date]

def get_matured_with_balance(file_path, maturity_col, balance_col, cutoff_date):
    df = pd.read_excel(file_path)
    df[maturity_col] = pd.to_datetime(df[maturity_col], errors='coerce')
    df = df.dropna(subset=[maturity_col])
    df = clean_df(df)
    target_date = pd.to_datetime(cutoff_date)
    return df[(df[maturity_col] <= target_date) & (df[balance_col] > 0)]

def get_zero_interest_accounts(file_path, int_rate_col):
    df = pd.read_excel(file_path)
    df = clean_df(df)
    return df[df[int_rate_col] == 0]

def disbursement_and_writeoff(file_path, disbursement_column, writeoff_column, account_number_column, cif_id_column, disbursement_months):
    df = pd.read_excel(file_path)
    df[disbursement_column] = pd.to_datetime(df[disbursement_column], errors='coerce')
    df[writeoff_column] = pd.to_datetime(df[writeoff_column], errors='coerce')
    df = clean_df(df)
    df_disbursement = df[df[disbursement_column].dt.month.isin(disbursement_months)]
    df_writeoff = df[df[writeoff_column].notna()]
    merged_df = pd.merge(df_disbursement, df_writeoff, on=cif_id_column, how='inner')
    merged_df = merged_df[merged_df[f'{account_number_column}_x'] != merged_df[f'{account_number_column}_y']]
    merged_df = merged_df.dropna(axis=1, how='any')
    return clean_df(merged_df)

def disbursement_and_npa(file_path, disbursement_column, npa_column, account_number_column, cif_id_column, disbursement_months):
    df = pd.read_excel(file_path)
    df[disbursement_column] = pd.to_datetime(df[disbursement_column], errors='coerce')
    df[npa_column] = pd.to_datetime(df[npa_column], errors='coerce')
    df = clean_df(df)
    df_q4 = df[df[disbursement_column].dt.month.isin(disbursement_months)]
    df_npa = df[df[npa_column].notna()]
    merged_df = pd.merge(df_q4, df_npa, on=cif_id_column, how='inner')
    merged_df = merged_df[merged_df[f'{account_number_column}_x'] != merged_df[f'{account_number_column}_y']]
    merged_df = merged_df.dropna(axis=1, how='any')
    return clean_df(merged_df)

def get_same_day_closure_disbursement(file_path, disbursement_column, closure_date):
    df = pd.read_excel(file_path)
    
    # Convert both columns to datetime and drop rows where conversion failed
    df[disbursement_column] = pd.to_datetime(df[disbursement_column], errors='coerce')
    df[closure_date] = pd.to_datetime(df[closure_date], errors='coerce')
    
    # Drop rows where either column is NaT
    df = df.dropna(subset=[disbursement_column, closure_date])
    
    df = clean_df(df)  # Clean other NaN and infinite values if needed
    
    # Now safe to use .dt.date
    return df[df[disbursement_column].dt.date == df[closure_date].dt.date]


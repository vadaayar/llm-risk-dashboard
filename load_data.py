import pandas as pd

def load_supplier_data(path="Processed_Supplier_Data.csv"):
    return pd.read_csv(path)

def load_delay_data(path="processed_data_cleaned.csv"):
    return pd.read_csv(path)

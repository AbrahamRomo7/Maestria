import pandas as pd
from config.paths import RAW_DATA

def extract_data():
    return pd.read_excel(RAW_DATA, engine="openpyxl")

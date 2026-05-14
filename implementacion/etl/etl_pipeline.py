from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data

def run_etl():

    print("Iniciando ETL")

    df = extract_data()

    df_clean = transform_data(df)

    load_data(df_clean)

    print("ETL finalizado")

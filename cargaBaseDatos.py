import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

file_path = "archivo.xlsx"
table_name = "importaciones"

columns = [
    "DESCRIPCIÓN ARANCELARIA",
    "DESCRIPCION PRODUCTO COMERCIAL",
    "MARCA",
    "ESTADO DE MERCANCIA",
    "RUC IMPORTADOR",
    "PROBABLE IMPORTADOR",
    "PAÍS DE ORIGEN",
    "PAÍS DE PROCEDENCIA",
    "DIA",
    "MES",
    "AÑO",
    "ADVALOREM",
    "US$ FOB",
    "US$ FLETE",
    "US$ SEGURO",
    "US$ CIF"
]

dtype_map = {
    "DESCRIPCIÓN ARANCELARIA": "string",
    "DESCRIPCION PRODUCTO COMERCIAL": "string",
    "MARCA": "string",
    "ESTADO DE MERCANCIA": "string",
    "RUC IMPORTADOR": "string",
    "PROBABLE IMPORTADOR": "string",
    "PAÍS DE ORIGEN": "string",
    "PAÍS DE PROCEDENCIA": "string"
}

numeric_cols = [
    "ADVALOREM",
    "US$ FOB",
    "US$ FLETE",
    "US$ SEGURO",
    "US$ CIF"
]

date_cols = ["DIA", "MES", "AÑO"]

df = pd.read_excel(
    file_path,
    usecols=columns,
    dtype=dtype_map,
    engine="openpyxl"
)

df.columns = df.columns.str.strip().str.upper()

df = df.replace(r"^\s*$", np.nan, regex=True)

df = df.dropna(how="all")

df = df.drop_duplicates()

for col in numeric_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.strip()
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")

for col in date_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["FECHA"] = pd.to_datetime(
    dict(year=df["AÑO"], month=df["MES"], day=df["DIA"]),
    errors="coerce"
)

text_cols = list(dtype_map.keys())

for col in text_cols:
    df[col] = (
        df[col]
        .str.normalize("NFKC")
        .str.strip()
        .str.upper()
    )

df = df.dropna(subset=[
    "DESCRIPCIÓN ARANCELARIA",
    "RUC IMPORTADOR",
    "US$ CIF"
])

df = df.sort_values(by="FECHA").reset_index(drop=True)

rename_map = {
    "DESCRIPCIÓN ARANCELARIA": "descripcion_arancelaria",
    "DESCRIPCION PRODUCTO COMERCIAL": "descripcion_producto_comercial",
    "MARCA": "marca",
    "ESTADO DE MERCANCIA": "estado_mercancia",
    "RUC IMPORTADOR": "ruc_importador",
    "PROBABLE IMPORTADOR": "probable_importador",
    "PAÍS DE ORIGEN": "pais_origen",
    "PAÍS DE PROCEDENCIA": "pais_procedencia",
    "DIA": "dia",
    "MES": "mes",
    "AÑO": "anio",
    "ADVALOREM": "advalorem",
    "US$ FOB": "fob",
    "US$ FLETE": "flete",
    "US$ SEGURO": "seguro",
    "US$ CIF": "cif",
    "FECHA": "fecha"
}

df = df.rename(columns=rename_map)

with engine.begin() as conn:
    conn.execute(text(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            descripcion_arancelaria TEXT,
            descripcion_producto_comercial TEXT,
            marca TEXT,
            estado_mercancia TEXT,
            ruc_importador TEXT,
            probable_importador TEXT,
            pais_origen TEXT,
            pais_procedencia TEXT,
            dia INTEGER,
            mes INTEGER,
            anio INTEGER,
            advalorem NUMERIC,
            fob NUMERIC,
            flete NUMERIC,
            seguro NUMERIC,
            cif NUMERIC,
            fecha TIMESTAMP
        );
    """))

df.to_sql(
    table_name,
    engine,
    if_exists="append",
    index=False,
    method="multi",
    chunksize=1000
)
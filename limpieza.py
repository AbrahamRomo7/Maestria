import pandas as pd
import numpy as np

file_path = "dataImportaciones.xlsx"
output_path = "resultado_procesado.xlsx"

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

df = df.sort_values(by="FECHA", ascending=True)

df = df.reset_index(drop=True)

df.to_excel(output_path, index=False)
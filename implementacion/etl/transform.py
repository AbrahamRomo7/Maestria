import pandas as pd
import numpy as np

def transform_data(df):

    df.columns = df.columns.str.strip().str.upper()

    numeric_cols = [
        "ADVALOREM",
        "US$ FOB",
        "US$ FLETE",
        "US$ SEGURO",
        "US$ CIF"
    ]

    for col in numeric_cols:

        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("$", "", regex=False)
            .str.strip()
        )

        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["FECHA"] = pd.to_datetime(
        dict(
            year=df["AÑO"],
            month=df["MES"],
            day=df["DIA"]
        ),
        errors="coerce"
    )

    rename_map = {
        "DESCRIPCIÓN ARANCELARIA": "partida",
        "US$ CIF": "cif",
        "US$ FOB": "fob",
        "US$ FLETE": "flete",
        "US$ SEGURO": "seguro",
        "FECHA": "fecha"
    }

    df = df.rename(columns=rename_map)

    df = df.dropna(subset=["partida", "cif"])

    return df

import pandas as pd

from prophet import Prophet

from database.connection import engine

from config.settings import (
    FORECAST_MONTHS,
    PREDICTIONS_PATH
)

def generate_forecast():

    df = pd.read_sql(
        "SELECT * FROM importaciones",
        engine
    )

    df["fecha"] = pd.to_datetime(df["fecha"])

    df["anio_mes"] = (
        df["fecha"]
        .dt.to_period("M")
    )

    df_monthly = (
        df.groupby(
            ["partida", "anio_mes"]
        )["cif"]
        .sum()
        .reset_index()
    )

    resultados = []

    categorias = df_monthly["partida"].unique()

    for cat in categorias:

        df_temp = (
            df_monthly[
                df_monthly["partida"] == cat
            ]
            .copy()
        )

        if len(df_temp) < 24:
            continue

        df_temp["ds"] = (
            df_temp["anio_mes"]
            .dt.to_timestamp()
        )

        df_temp = df_temp[["ds", "cif"]]

        df_temp.columns = ["ds", "y"]

        model = Prophet()

        model.fit(df_temp)

        future = model.make_future_dataframe(
            periods=FORECAST_MONTHS,
            freq="ME"
        )

        forecast = model.predict(future)

        forecast["partida"] = cat

        resultados.append(
            forecast[["ds", "yhat", "partida"]]
        )

    pd.concat(resultados).to_csv(
        PREDICTIONS_PATH,
        index=False
    )

    print("Predicciones generadas")

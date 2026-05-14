import pandas as pd

from prophet import Prophet
from sklearn.model_selection import TimeSeriesSplit

from database.connection import engine
from models.evaluate_model import calculate_metrics

from config.settings import (
    N_SPLITS,
    METRICS_PATH
)

def train_model():

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

    metricas = []

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

        tscv = TimeSeriesSplit(
            n_splits=N_SPLITS
        )

        maes = []
        rmses = []
        mapes = []

        for train_index, test_index in tscv.split(df_temp):

            train = df_temp.iloc[train_index]

            test = df_temp.iloc[test_index]

            model = Prophet(
                yearly_seasonality=True
            )

            model.fit(train)

            future = model.make_future_dataframe(
                periods=len(test),
                freq="ME"
            )

            forecast = model.predict(future)

            pred_test = (
                forecast[["ds", "yhat"]]
                .merge(test, on="ds", how="inner")
            )

            mae, rmse, mape = calculate_metrics(
                pred_test["y"],
                pred_test["yhat"]
            )

            maes.append(mae)
            rmses.append(rmse)
            mapes.append(mape)

        metricas.append({
            "Partida": cat,
            "MAE": round(sum(maes)/len(maes), 2),
            "RMSE": round(sum(rmses)/len(rmses), 2),
            "MAPE (%)": round(sum(mapes)/len(mapes), 2)
        })

    pd.DataFrame(metricas).to_csv(
        METRICS_PATH,
        index=False
    )

    print("Entrenamiento finalizado")

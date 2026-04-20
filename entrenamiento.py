import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

query = "SELECT * FROM importaciones"
df = pd.read_sql(query, engine)

df = df.dropna(subset=["fecha", "cif"])

df["fecha"] = pd.to_datetime(df["fecha"])
df = df.sort_values("fecha")

df["year"] = df["fecha"].dt.year
df["month"] = df["fecha"].dt.month
df["day"] = df["fecha"].dt.day
df["weekday"] = df["fecha"].dt.weekday

df["lag_1"] = df["cif"].shift(1)
df["lag_2"] = df["cif"].shift(2)
df["rolling_mean_3"] = df["cif"].rolling(window=3).mean()
df["rolling_std_3"] = df["cif"].rolling(window=3).std()

df = df.dropna()

features = [
    "year", "month", "day", "weekday",
    "lag_1", "lag_2",
    "rolling_mean_3", "rolling_std_3",
    "fob", "flete", "seguro", "advalorem"
]

target = "cif"

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", RandomForestRegressor(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    ))
])

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

metrics = pd.DataFrame({
    "MAE": [mae],
    "RMSE": [rmse],
    "R2": [r2]
})

metrics.to_csv("metricas_modelo.csv", index=False)

joblib.dump(pipeline, "modelo_tendencias.pkl")

future_df = df.tail(1).copy()

future_predictions = []

for i in range(1, 13):
    future_df["month"] = (future_df["month"] % 12) + 1
    pred = pipeline.predict(future_df[features])[0]
    future_df["lag_2"] = future_df["lag_1"]
    future_df["lag_1"] = pred
    future_df["rolling_mean_3"] = future_df[["lag_1", "lag_2"]].mean(axis=1)
    future_df["rolling_std_3"] = future_df[["lag_1", "lag_2"]].std(axis=1)
    future_predictions.append(pred)

pd.DataFrame({
    "predicciones_cif": future_predictions
}).to_csv("predicciones_futuras.csv", index=False)
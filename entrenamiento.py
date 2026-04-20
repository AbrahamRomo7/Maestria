import os
import numpy as np
import pandas as pd
import joblib
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sklearn.model_selection import TimeSeriesSplit, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

load_dotenv()

# 1. Conexión y Carga de Datos
engine = create_engine(f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
query = "SELECT * FROM importaciones"
df = pd.read_sql(query, engine)

# 2. Preprocesamiento e Ingeniería de Detalles
df["fecha"] = pd.to_datetime(df["fecha"])
df = df.sort_values("fecha").dropna(subset=["cif"])

# Nuevas características para captar estacionalidad y tendencia
df["year"] = df["fecha"].dt.year
df["month"] = df["fecha"].dt.month
df["weekday"] = df["fecha"].dt.weekday
df["trend"] = np.arange(len(df))  # Índice temporal para tendencia
df["lag_1"] = df["cif"].shift(1)
df["lag_2"] = df["cif"].shift(2)
df["rolling_mean_3"] = df["cif"].rolling(window=3).mean()

df = df.dropna()

features = ["year", "month", "weekday", "trend", "lag_1", "lag_2", "rolling_mean_3", "fob", "flete", "seguro"]
target = "cif"

X = df[features]
y = df[target]

# 3. Validación Cruzada y Ajuste de Hiperparámetros
# Usamos TimeSeriesSplit para validar cronológicamente
tscv = TimeSeriesSplit(n_splits=5)

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", RandomForestRegressor(random_state=42))
])

param_dist = {
    "model__n_estimators": [100, 300, 500],
    "model__max_depth": [10, 20, None],
    "model__min_samples_split": [2, 5, 10],
    "model__bootstrap": [True, False]
}

# Búsqueda aleatoria de los mejores parámetros
random_search = RandomizedSearchCV(
    pipeline, param_distributions=param_dist, 
    n_iter=15, cv=tscv, scoring='neg_root_mean_squared_error', 
    n_jobs=-1, random_state=42
)

random_search.fit(X, y)
best_model = random_search.best_estimator_

# 4. Evaluación Estadística Final
y_pred = best_model.predict(X)
mae = mean_absolute_error(y, y_pred)
rmse = np.sqrt(mean_squared_error(y, y_pred))
r2 = r2_score(y, y_pred)

print(f"Mejoras logradas: MAE: {mae:.2f}, RMSE: {rmse:.2f}, R2: {r2:.2f}")

# Guardar métricas para el reporte
pd.DataFrame({"Métrica": ["MAE", "RMSE", "R2"], "Valor": [mae, rmse, r2]}).to_csv("analisis_estadistico.csv", index=False)
joblib.dump(best_model, "modelo_final_importaciones.pkl")

# 5. Predicción Futura (Proyección 12 meses)
# Tomamos el último registro para empezar la cadena de predicción
last_data = df.tail(1).copy()
future_predictions = []

for i in range(12):
    # Predecir el siguiente valor
    current_pred = best_model.predict(last_data[features])[0]
    future_predictions.append(current_pred)
    
    # Actualizar lags para la siguiente iteración
    new_month = (last_data["month"].iloc[0] % 12) + 1
    new_year = last_data["year"].iloc[0] + (1 if new_month == 1 else 0)
    
    last_data["lag_2"] = last_data["lag_1"]
    last_data["lag_1"] = current_pred
    last_data["month"] = new_month
    last_data["year"] = new_year
    last_data["trend"] += 1
    last_data["rolling_mean_3"] = (last_data["lag_1"] + last_data["lag_2"]) / 2 # Aproximación

pd.DataFrame({"Mes_Proyectado": range(1, 13), "CIF_Predicho": future_predictions}).to_csv("proyeccion_12_meses.csv", index=False)

print("Proceso completado. Modelo y predicciones guardadas.")
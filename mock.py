import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

# =========================
# 1. CARGAR DATOS
# =========================
df = pd.read_excel("Oresa.xlsx", sheet_name="Datasur")
df.columns = df.columns.str.strip()

# =========================
# 2. LIMPIEZA
# =========================
df["fecha"] = pd.to_datetime(
    df["AÑO"].astype(str) + "-" +
    df["MES"].astype(str) + "-" +
    df["DIA"].astype(str),
    errors="coerce"
)

df.rename(columns={
    "US$ CIF": "cif"
}, inplace=True)

df["cif"] = pd.to_numeric(df["cif"], errors="coerce")

# limpiar datos malos
df = df[(df["cif"] > 0) & (df["cif"] < 1e9)]

# =========================
# 🔥 3. TOP PRODUCTOS (LO QUE SE REPITE)
# =========================
top_productos = df.groupby("PRODUCTO").agg({
    "cif": "sum",
    "PRODUCTO": "count"
}).rename(columns={"PRODUCTO": "frecuencia"}).reset_index()

top_productos = top_productos.sort_values("cif", ascending=False)

top_productos.to_csv("top_productos_real.csv", index=False)

# =========================
# 🤖 4. CLUSTERING DE PRODUCTOS
# =========================
productos_cluster = df.groupby("PRODUCTO").agg({
    "cif": "sum",
    "CANTIDAD": "sum",
    "RUC IMPORTADOR": "nunique"
}).reset_index()

productos_cluster.columns = ["producto", "volumen", "cantidad", "competencia"]

# limpiar
productos_cluster.replace([np.inf, -np.inf], np.nan, inplace=True)
productos_cluster = productos_cluster.dropna()

# escalar
scaler = MinMaxScaler()
X = scaler.fit_transform(productos_cluster[["volumen", "cantidad", "competencia"]])

# clustering
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
productos_cluster["cluster"] = kmeans.fit_predict(X)

productos_cluster.to_csv("cluster_productos.csv", index=False)

# =========================
# 🌎 5. PAÍSES MÁS IMPORTANTES
# =========================
paises = df.groupby("PAÍS DE ORIGEN").agg({
    "cif": "sum",
    "CANTIDAD": "sum"
}).reset_index()

paises = paises.sort_values("cif", ascending=False)

paises.to_csv("ranking_paises.csv", index=False)

# =========================
# 📈 6. TENDENCIA POR PAÍS
# =========================
tendencia_pais = df.groupby(
    ["PAÍS DE ORIGEN", pd.Grouper(key="fecha", freq="M")]
).agg({
    "cif": "sum"
}).reset_index()

tendencia_pais.to_csv("tendencia_pais.csv", index=False)

print("✅ Archivos generados:")
print("- top_productos_real.csv")
print("- cluster_productos.csv")
print("- ranking_paises.csv")
print("- tendencia_pais.csv")
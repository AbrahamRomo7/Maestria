import pandas as pd

# Cargar archivo
df = pd.read_excel('Oresa.xlsx')

# Ver columnas
print(df.columns)
df.head()
columnas_utiles = [
    'AÑO', 'MES', 'DIA',
    'PAÍS DE ORIGEN',
    'PAÍS DE PROCEDENCIA',
    'DESCRIPCION PRODUCTO COMERCIAL',
    'PARTIDA ARANCELARIA',
    'CANTIDAD',
    'PESO NETO KG',
    'US$ FOB',
    'US$ FLETE',
    'US$ SEGURO',
    'US$ CIF'
]

df = df[columnas_utiles]
df.columns = [
    'anio', 'mes', 'dia',
    'pais_origen',
    'pais_procedencia',
    'producto',
    'partida',
    'cantidad',
    'peso_kg',
    'fob',
    'flete',
    'seguro',
    'cif'
]
# Eliminar filas sin datos clave
df = df.dropna(subset=['producto', 'cif', 'cantidad'])

# Rellenar opcionales
df['flete'] = df['flete'].fillna(0)
df['seguro'] = df['seguro'].fillna(0)
df['anio'] = df['anio'].astype(int)
df['mes'] = df['mes'].astype(int)
df['dia'] = df['dia'].astype(int)

numericas = ['cantidad', 'peso_kg', 'fob', 'flete', 'seguro', 'cif']
for col in numericas:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df['fecha'] = pd.to_datetime(df[['anio', 'mes', 'dia']])
    # Costo total logístico
df['costo_logistico'] = df['flete'] + df['seguro']

# Costo unitario CIF
df['cif_unitario'] = df['cif'] / df['cantidad']

# Costo por kg
df['costo_por_kg'] = df['cif'] / df['peso_kg']

# Mes como categoría temporal
df['mes_nombre'] = df['fecha'].dt.month_name()
df['producto'] = df['producto'].str.upper().str.strip()
df['pais_origen'] = df['pais_origen'].str.upper().str.strip()
# Quitar valores extremos de CIF
q1 = df['cif'].quantile(0.01)
q99 = df['cif'].quantile(0.99)

df = df[(df['cif'] >= q1) & (df['cif'] <= q99)]
df.to_csv('dataset_limpio_importaciones.csv', index=False)
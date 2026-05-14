# Sistema Predictivo de Importaciones con Inteligencia Artificial

Proyecto de análisis predictivo orientado a la estimación de demanda de importaciones utilizando técnicas de ETL, almacenamiento en PostgreSQL, modelos de inteligencia artificial y visualización en Power BI.

---

# Arquitectura del Proyecto

El sistema sigue una arquitectura basada en pipeline:

```text
Datos Externos → ETL → PostgreSQL → Modelos Predictivos → Power BI
```

---

# Tecnologías Utilizadas

| Tecnología | Uso |
|---|---|
| Python | Desarrollo del pipeline |
| Pandas | Transformación y análisis de datos |
| PostgreSQL | Almacenamiento |
| SQLAlchemy | Conexión a base de datos |
| Prophet | Predicción de series temporales |
| Scikit-learn | Métricas y validación |
| Power BI | Visualización |
| OpenPyXL | Lectura de Excel |

---

# Estructura del Proyecto

```text
tesis_importaciones_ai/
│
├── config/
│   ├── settings.py
│   └── paths.py
│
├── database/
│   └── connection.py
│
├── etl/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── etl_pipeline.py
│
├── models/
│   ├── evaluate_model.py
│   ├── train_model.py
│   └── forecast.py
│
├── data/
│   ├── raw/
│   │   └── data_mock.xlsx
│   │
│   ├── processed/
│   │
│   └── predictions/
│       ├── metricas_modelo.csv
│       └── predicciones_12_meses.csv
│
├── outputs/
│
├── main.py
├── requirements.txt
├── .env
└── README.md
```

---

# Flujo del Pipeline

## 1. Extracción de Datos

Se leen datos desde el archivo:

```text
data/raw/data_mock.xlsx
```

---

## 2. Transformación

Durante el proceso ETL se realizan:

- limpieza de valores nulos,
- eliminación de duplicados,
- conversión numérica,
- normalización de texto,
- generación de fechas,
- validación de columnas.

---

## 3. Carga a PostgreSQL

Los datos procesados se almacenan en la tabla:

```sql
importaciones
```

---

## 4. Entrenamiento del Modelo

El sistema:

- agrupa importaciones por partida arancelaria,
- genera series temporales mensuales,
- aplica Prophet,
- utiliza validación temporal con TimeSeriesSplit,
- calcula métricas:
  - MAE
  - RMSE
  - MAPE

---

## 5. Generación de Predicciones

El modelo proyecta:

```text
12 meses futuros
```

por cada partida arancelaria válida.

---

# Métricas Utilizadas

## MAE

Error absoluto promedio.

```math
MAE = \frac{1}{n}\sum |y_{real} - y_{predicho}|
```

---

## RMSE

Penaliza errores grandes.

```math
RMSE = \sqrt{\frac{1}{n}\sum (y_{real} - y_{predicho})^2}
```

---

## MAPE

Error porcentual promedio.

```math
MAPE = \frac{100}{n}\sum \left|\frac{y_{real} - y_{predicho}}{y_{real}}\right|
```

---

# Requisitos Previos

## Instalar PostgreSQL

Crear una base de datos para el proyecto.

---

# Configuración del Archivo `.env`

Crear un archivo `.env` en la raíz del proyecto:

```env
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nombre_base_datos
```

---

# Instalación

## 1. Crear entorno virtual

### Windows

```bash
python -m venv venv
```

Activar:

```bash
venv\Scripts\activate
```

---

## 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Ejecución del Pipeline

Ejecutar:

```bash
python main.py
```

---

# Salidas Generadas

## Métricas

```text
data/predictions/metricas_modelo.csv
```

Contiene:

- MAE
- RMSE
- MAPE

por partida arancelaria.

---

## Predicciones

```text
data/predictions/predicciones_12_meses.csv
```

Contiene:

- fecha,
- predicción,
- partida arancelaria.

---

# Integración con Power BI

Power BI puede conectarse directamente a:

- PostgreSQL,
- archivos CSV generados,
- o tablas exportadas.

Se recomienda implementar dashboards para:

- tendencias CIF,
- análisis por país,
- análisis por partida arancelaria,
- proyección futura de demanda.

---

# Validación del Modelo

El proyecto utiliza:

```text
TimeSeriesSplit
```

para garantizar:

- validación cronológica,
- reducción de sobreajuste,
- evaluación sobre datos no vistos.

---

# Objetivo del Proyecto

Desarrollar un sistema predictivo que permita:

- estimar demanda de importaciones,
- mejorar planificación,
- apoyar toma de decisiones,
- reducir riesgos operativos,
- optimizar gestión empresarial.

---

# Autor

Abraham Romo-Anthony Reyna

Proyecto académico de Inteligencia Artificial aplicada a análisis predictivo de importaciones.
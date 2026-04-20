# Sistema de Prediccion de Tendencias de Importaciones (CIF)

Este repositorio contiene el prototipo final de inteligencia artificial diseñado para el analisis y pronostico del valor CIF en importaciones. El sistema integra una base de datos PostgreSQL, un proceso ETL automatizado y un modelo predictivo basado en Bosques Aleatorios (Random Forest) optimizado para series temporales.

## 1. Descripcion del Proyecto

El objetivo de este proyecto es transformar datos crudos de importaciones almacenados en un servidor local de PostgreSQL en proyecciones estrategicas de valor CIF para los proximos 12 meses. El modelo utiliza tecnicas de aprendizaje supervisado para identificar patrones historicos, estacionalidad y tendencias de mercado.

## 2. Instrucciones de Ejecucion

### Configuracion de Variables de Entorno
Antes de iniciar, es obligatorio crear un archivo denominado `.env` en la raiz del proyecto con las siguientes claves:

DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nombre_de_tu_bd

### Paso a Paso para la Ejecucion
1. Asegurarse de que el servicio de PostgreSQL este activo y con la tabla 'importaciones' cargada.
2. Abrir una terminal en la carpeta del proyecto.
3. Instalar las dependencias (ver seccion 3).
4. Ejecutar el script principal:
   python predictor_importaciones.py

El sistema generara automaticamente tres archivos:
- modelo_final_importaciones.pkl (Binario del modelo)
- analisis_estadistico.csv (Metricas de desempeño)
- proyeccion_12_meses.csv (Predicciones futuras)

## 3. Dependencias y Versiones

El proyecto fue desarrollado y probado con las siguientes versiones de librerias:

- Python: 3.9.x
- pandas: 2.1.0
- numpy: 1.24.3
- scikit-learn: 1.3.0
- sqlalchemy: 2.0.20
- psycopg2-binary: 2.9.7
- python-dotenv: 1.0.0
- joblib: 1.3.2

## 4. Registro de Cambios (Bitacora)

### Version 1.0.0 (Prototipo Inicial)
- Implementacion de conexion basica a base de datos.
- Modelo inicial de Random Forest con division de datos simple (80/20).
- Script de preprocesamiento lineal.

### Version 2.0.0 (Optimizacion y Ajuste Tecnico) - ACTUAL
- Ajuste de Hiperparametros: Implementacion de RandomizedSearchCV para optimizar profundidad y estimadores del modelo.
- Validacion Estadistica: Sustitucion de split simple por TimeSeriesSplit (Validacion Cruzada Temporal).
- Ingenieria de Caracteristicas: Adicion de variables de tendencia (trend) y calculo dinamico de rezagos (lags).
- Robustez del Pipeline: Inclusion de escalamiento de datos (StandardScaler) dentro del flujo de entrenamiento.
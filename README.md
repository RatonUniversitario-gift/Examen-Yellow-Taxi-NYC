# Examen — Pipeline de Datos y Predicción Yellow Taxi NYC
 
## Descripción
 
Pipeline de datos completo desarrollado sobre el dataset Yellow Taxi Trip Records de NYC TLC. El sistema implementa un flujo de ingesta, limpieza, transformación, modelado y predicción de datos, con el objetivo de predecir el monto total de un viaje (`total_amount`) mediante modelos de regresión. Incluye una aplicación Streamlit para explorar los datos procesados y realizar predicciones con el modelo entrenado.
 
---
 
## Requisitos
 
- Python 3.12+
- Las dependencias están listadas en `requirements.txt`
Instalación:
 
```bash
pip install -r requirements.txt
```
 
---
 
## Estructura del proyecto
 
```
examen_yellow_taxi/
│
├── data/
│   ├── raw/                        # Datos originales descargados de NYC TLC (no incluidos en el repo)
│   ├── processed/                  # Dataset limpio con features (no incluido en el repo)
│   └── outputs/                    # Resultados generados por el pipeline (no incluidos en el repo)
│       ├── metricas_modelos.csv
│       ├── predicciones.csv
│       └── importancia_variables.csv
│
├── models/                         # Modelos entrenados (no incluidos en el repo)
│   ├── LinearRegression.pkl
│   ├── RandomForest.pkl
│   └── modelo_final.pkl
│
├── src/                            # Módulos del pipeline
│   ├── data_loader.py              # Ingesta de datos (carga múltiples archivos Parquet)
│   ├── cleaning.py                 # Limpieza y validación
│   ├── features.py                 # Ingeniería de características
│   ├── preprocessing.py            # Split cronológico train/test
│   └── modeling.py                 # Entrenamiento y evaluación de modelos
│
├── app/                            # Aplicación Streamlit
│   ├── app.py                      # Página principal
│   ├── pages/
│   │   ├── 01_Exploracion_Datos.py
│   │   ├── 02_Indicadores.py
│   │   ├── 03_Consulta_Viajes.py
│   │   ├── 04_Visualizaciones.py
│   │   ├── 05_Evaluacion_Modelo.py
│   │   └── 06_Prediccion.py
│   └── utils/
│       ├── load_data.py
│       └── predict.py
│
├── reports/
│   ├── graficos/
│   │   ├── distribucion_target.png
│   │   ├── errores_modelo.png
│   │   └── importancia_variables.png
│   └── informe_resultados.md
│
├── docs/
│   └── diccionario_variables.md
│
├── main.py                         # Punto de entrada del pipeline
├── generar_graficos.py             # Genera los gráficos de reports/graficos/
├── requirements.txt
├── .gitignore
└── README.md
```
 
---
 
## Ejecución
 
**1. Descargar los datos**
 
Descargar los archivos Parquet de NYC TLC (diciembre 2023 a abril 2024) y colocarlos en `data/raw/`:
```
yellow_tripdata_2023-12.parquet
yellow_tripdata_2024-01.parquet
yellow_tripdata_2024-02.parquet
yellow_tripdata_2024-03.parquet
yellow_tripdata_2024-04.parquet
```
 
**2. Ejecutar el pipeline**
 
```bash
python main.py
```
 
Esto ejecuta automáticamente: carga de los 5 meses, limpieza, ingeniería de características, split cronológico, entrenamiento y evaluación de modelos, y genera los archivos de salida (`data/processed/`, `data/outputs/`, `models/`).
 
**3. Generar gráficos de evaluación**
 
```bash
python generar_graficos.py
```
 
**4. Levantar la aplicación Streamlit**
 
```bash
streamlit run app/app.py
```
 
La app se abre en el navegador en `http://localhost:8501`.
 
---
 
## Dataset
 
- **Fuente:** NYC Taxi & Limousine Commission (TLC)
- **Período:** Diciembre 2023 - Abril 2024 (5 meses)
- **Registros cargados:** 16.445.634
- **Registros tras limpieza:** 14.533.124
- **Pérdida:** 11.63%
---
 
## Variable objetivo
 
Se eligió `total_amount` como variable objetivo por ser la variable más representativa del valor de un viaje para el negocio. Es un problema de regresión — el modelo predice un valor numérico continuo.
 
Las siguientes variables fueron excluidas por data leakage, ya que forman parte del cálculo de `total_amount`:
 
`fare_amount`, `tip_amount`, `tolls_amount`, `extra`, `mta_tax`, `congestion_surcharge`, `Airport_fee`, `improvement_surcharge`
 
---
 
## Reglas de limpieza aplicadas
 
| Regla | Registros eliminados |
|---|---|
| Fechas fuera de dic 2023 - abr 2024 | 51 |
| trip_distance <= 0 | 334.909 |
| fare_amount <= 0 | 221.446 |
| total_amount <= 0 | 0 |
| duracion_minutos <= 0 | 602 |
| duracion_minutos > 240 | 10.148 |
| trip_distance > 100 | 438 |
| passenger_count inválido o nulo | 1.344.916 |
 
---
 
## Ingeniería de características
 
Se crearon 13 variables nuevas agrupadas en:
 
- **Temporales:** `pickup_hour`, `pickup_dayofweek`, `pickup_month`, `is_weekend`, `is_rush_hour`, `es_temporada_alta`
- **Duración y velocidad:** `duracion_minutos`, `velocidad_promedio_mph`
- **Costos y viaje:** `tiene_peaje`, `tiene_propina`, `porcentaje_propina`, `es_aeropuerto`
- **Categóricas codificadas:** `VendorID`, `RatecodeID`, `payment_type`, `PULocationID`, `DOLocationID`
Detalle completo en `docs/diccionario_variables.md`.
 
---
 
## Decisiones técnicas
 
**Período elegido:** diciembre 2023 a abril 2024. Se incluyó diciembre para cumplir el mínimo de 5 meses solicitado, agregando la variable `es_temporada_alta` para capturar el efecto de fin de año.
 
**Split cronológico 80/20:** los datos se ordenan por `tpep_pickup_datetime` antes de dividir, evitando que el modelo aprenda del futuro.
 
**Modelos:** LinearRegression como baseline y RandomForestRegressor como modelo no lineal. El RandomForest se configuró con `n_estimators=50` y `max_depth=20` (en lugar de los 100 árboles sin límite de profundidad usados inicialmente) debido a restricciones de memoria al procesar 14.5 millones de registros, sin pérdida relevante de rendimiento.
 
---
 
## Resultados
 
| Modelo | MAE | RMSE | R² |
|---|---|---|---|
| LinearRegression | 3.1336 | 7.1836 | 0.8993 |
| RandomForest | 0.5170 | 2.7184 | 0.9856 |
 
El modelo RandomForest obtiene un error promedio de $0.52 por viaje y explica el 98.56% de la variabilidad del monto total. Análisis detallado en `reports/informe_resultados.md`.
 
---
 
## Aplicación Streamlit
 
La app cuenta con 6 páginas:
 
1. **Exploración de datos** — vista previa, tipos de datos, nulos y estadísticas descriptivas.
2. **Indicadores** — métricas operacionales del servicio (monto promedio, distancia, duración, propinas).
3. **Consulta de viajes** — filtros interactivos por hora, distancia, tipo de pago y vendor, con descarga de resultados.
4. **Visualizaciones** — gráficos de viajes por hora, monto promedio por hora y relación distancia-monto.
5. **Evaluación del modelo** — métricas, comparación real vs. predicho, distribución de errores e importancia de variables.
6. **Predicción** — formulario para estimar el monto total de un viaje nuevo usando el modelo entrenado.
---
 
## Autores
 
Ignacio Pizarro, Aracelly Salgado, Lucas Quitral y Gabriel Astorga
Asignatura: Gestión de Datos para IA — Duoc UC

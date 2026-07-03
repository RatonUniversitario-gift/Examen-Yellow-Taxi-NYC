# Examen — Pipeline de Datos y Predicción Yellow Taxi NYC

## Descripción

Pipeline de datos completo desarrollado sobre el dataset **Yellow Taxi Trip Records** de NYC TLC. El sistema implementa un flujo de ingesta, limpieza, transformación, modelado y predicción de datos con el objetivo de predecir el monto total de un viaje (`total_amount`) mediante modelos de regresión.

Incluye una aplicación **Streamlit** para explorar los datos procesados y realizar predicciones en tiempo real bajo una simulación de producción.

---

# Requisitos

- Python 3.12+
- Dependencias listadas en `requirements.txt`

## Instalación

```bash
pip install -r requirements.txt
```

---

# Estructura del proyecto

```text
taller_yellow_taxi/
│
├── data/
│   ├── raw/
│   │   ├── yellow_tripdata_2023-12.parquet
│   │   ├── yellow_tripdata_2024-01.parquet
│   │   ├── yellow_tripdata_2024-02.parquet
│   │   ├── yellow_tripdata_2024-03.parquet
│   │   └── yellow_tripdata_2024-04.parquet
│   │
│   ├── processed/
│   └── outputs/
│       ├── metricas_modelos.csv
│       ├── predicciones.csv
│       └── importancia_variables.csv
│
├── models/
│   ├── LinearRegression.pkl
│   ├── RandomForest.pkl
│   └── modelo_final.pkl
│
├── src/
│   ├── data_loader.py
│   ├── cleaning.py
│   ├── features.py
│   ├── preprocessing.py
│   └── modeling.py
│
├── app/
│   ├── app.py
│   ├── pages/
│   │   ├── 01_Exploracion_Datos.py
│   │   ├── 02_Indicadores.py
│   │   ├── 03_Consulta_Viajes.py
│   │   ├── 04_Visualizaciones.py
│   │   ├── 05_Evaluacion_Modelo.py
│   │   └── 06_Prediccion.py
│   │
│   └── utils/
│       ├── load_data.py
│       └── predict.py
│
├── reports/
│   └── graficos/
│       ├── distribucion_target.png
│       ├── errores_modelo.png
│       └── importancia_variables.png
│
├── main.py
├── generar_graficos.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Ejecución

## 1. Descargar los datos

Descargar los archivos Parquet de NYC TLC (diciembre 2023 a abril 2024) y colocarlos en la carpeta `data/raw/`.

```text
yellow_tripdata_2023-12.parquet
yellow_tripdata_2024-01.parquet
yellow_tripdata_2024-02.parquet
yellow_tripdata_2024-03.parquet
yellow_tripdata_2024-04.parquet
```

## 2. Ejecutar el pipeline

```bash
python main.py
```

Esto ejecuta automáticamente:

- Carga masiva indexada de los cinco archivos.
- Limpieza de anomalías.
- División cronológica.
- Ingeniería de características.
- Entrenamiento automatizado de modelos.
- Persistencia de resultados en `data/outputs/` y `models/`.

## 3. Generar gráficos

```bash
python generar_graficos.py
```

## 4. Ejecutar Streamlit

```bash
streamlit run app/app.py
```

La aplicación quedará disponible en:

```
http://localhost:8501
```

---

# Dataset

- **Fuente:** NYC Taxi & Limousine Commission (TLC)
- **Período:** Diciembre 2023 – Abril 2024
- **Archivos:** 5
- **Registros cargados:** 16.445.634
- **Registros después de limpieza:** 14.533.124
- **Registros eliminados:** 11,63%

---

# Variable objetivo

La variable objetivo seleccionada es:

```text
total_amount
```

Representa el monto total pagado por el viaje.

Como el modelo simula una predicción **antes de iniciar el trayecto**, se eliminaron todas las variables que sólo existen una vez finalizado el viaje.

## Variables excluidas

### Costos conocidos únicamente al finalizar

- `fare_amount`
- `tip_amount`
- `tolls_amount`
- `extra`
- `mta_tax`
- `congestion_surcharge`
- `Airport_fee`
- `improvement_surcharge`

### Variables posteriores al viaje

- `tpep_dropoff_datetime`
- `duracion_minutos`
- `velocidad_promedio_mph`
- `tiene_peaje`
- `tiene_propina`
- `porcentaje_propina`

---

# Reglas de limpieza

| Regla | Registros eliminados | Justificación |
|--------|---------------------:|--------------|
| Fechas fuera del período | 51 | Consistencia temporal |
| `trip_distance <= 0` | 335.376 | Viajes inválidos |
| `fare_amount <= 0` | 221.424 | Tarifas erróneas |
| `duracion_minutos <= 0` | 10.743 | Duraciones imposibles |
| `passenger_count` inválido | 1.344.916 | Registros inconsistentes |

---

# Ingeniería de características

Las 14 variables utilizadas corresponden únicamente a información disponible antes del inicio del viaje.

## Variables temporales

- `pickup_hour`
- `pickup_dayofweek`
- `pickup_month`
- `is_weekend`
- `is_rush_hour`
- `es_temporada_alta`

## Variables del viaje

- `trip_distance`
- `passenger_count`
- `es_aeropuerto`

## Variables categóricas

- `VendorID`
- `RatecodeID`
- `payment_type`
- `PULocationID`
- `DOLocationID`

---

# Decisiones técnicas

## División entrenamiento/prueba

Se realizó un **split cronológico 80/20** utilizando `tpep_pickup_datetime`.

- Entrenamiento: **11.626.499 registros**
- Prueba: **2.906.625 registros**

Esto evita fuga de información temporal (*data leakage*).

## Ajuste del Random Forest

Para reducir el consumo de memoria se utilizaron los siguientes parámetros:

- `n_estimators = 50`
- `max_depth = 15`
- `n_jobs = -1`

---

# Resultados

| Modelo | MAE | RMSE | R² |
|---------|----:|-----:|----:|
| Linear Regression | \$4.27 | \$8.11 | 0.8715 |
| Random Forest | **\$3.60** | **\$7.34** | **0.8948** |

## Análisis

- **Random Forest** obtuvo el mejor desempeño, alcanzando un MAE de **\$3.60** y explicando el **89,48 %** de la variabilidad.
- **Linear Regression** se utilizó como modelo base, logrando un desempeño competitivo.
- La diferencia entre MAE y RMSE evidencia la existencia de viajes atípicos con costos elevados.

---

# Aplicación Streamlit

La aplicación contiene seis módulos:

1. Exploración de datos.
2. Indicadores.
3. Consulta de viajes.
4. Visualizaciones.
5. Evaluación del modelo.
6. Predicción de nuevas tarifas.

---

# Autores

- Ignacio Pizarro
- Aracelly Salgado
- Lucas Quitral
- Gabriel Astorga

**Asignatura:** Gestión de Datos para IA — Duoc UC
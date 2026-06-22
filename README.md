# Taller — Pipeline de Gestión de Datos Yellow Taxi NYC

## Descripción

Pipeline de datos desarrollado sobre el dataset Yellow Taxi Trip Records de NYC TLC. El sistema implementa un flujo completo de ingesta, limpieza, transformación y modelado de datos, con el objetivo de predecir el monto total de un viaje (`total_amount`) mediante modelos de regresión.

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
taller_yellow_taxi/
│
├── data/
│   ├── raw/                        # Datos originales descargados de NYC TLC
│   │   └── yellow_tripdata_2024-01.parquet
│   └── outputs/                    # Resultados generados por el pipeline
│       ├── metricas_modelos.csv
│       └── predicciones.csv
│
├── models/                         # Modelos entrenados
│   ├── LinearRegression.pkl
│   └── RandomForest.pkl
│
├── src/                            # Módulos del pipeline
│   ├── data_loader.py              # Ingesta de datos
│   ├── cleaning.py                 # Limpieza y validación
│   ├── features.py                 # Ingeniería de características
│   ├── preprocessing.py            # Split cronológico train/test
│   └── modeling.py                 # Entrenamiento y evaluación de modelos
│
├── main.py                         # Punto de entrada del pipeline
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Ejecución

Desde la raíz del proyecto:

```bash
python main.py
```

El pipeline ejecuta automáticamente todas las etapas en orden: carga, limpieza, features, split y modelado.

---

## Dataset

- **Fuente:** NYC Taxi & Limousine Commission (TLC)
- **Período:** Enero 2024
- **Registros cargados:** 2.964.624
- **Registros tras limpieza:** 2.721.857
- **Pérdida:** 8.19%

---

## Variable objetivo

Se eligió `total_amount` como variable objetivo por ser la variable más representativa del valor de un viaje para el negocio. Es un problema de regresión — el modelo predice un valor numérico continuo.

Las siguientes variables fueron excluidas por data leakage, ya que forman parte del cálculo de `total_amount`:

- `fare_amount`, `tip_amount`, `tolls_amount`, `extra`, `mta_tax`, `congestion_surcharge`, `Airport_fee`, `improvement_surcharge`

---

## Reglas de limpieza aplicadas

| Regla                               |Registros eliminados|
|-------------------------------------|--------------------|            
| Fechas fuera de enero 2024          | 18                 |
| trip_distance                 <= 0  | 60.371             |
| fare_amount                   <= 0  | 34.538             |
| total_amount                  <= 0  | 0                  |
| duracion_minutos              <= 0  | 112                |
| duracion_minutos              > 240 | 1.842              |    
| trip_distance                 > 100 | 55                 |
| passenger_count      inválido o nulo| 145.831            |

---

## Decisiones técnicas

**Mes elegido:** Enero 2024. Es el mes más estable del año — sin fiestas ni estacionalidad de verano. Todos los archivos están consolidados sin datos parciales.

**Split cronológico 80/20:** Los datos se ordenan por `tpep_pickup_datetime` antes de dividir. Se usa split cronológico y no aleatorio porque los datos tienen componente temporal — mezclarlos aleatoriamente permitiría al modelo aprender del futuro.

**Modelos elegidos:** LinearRegression como baseline y RandomForest como modelo principal. LinearRegression permite establecer un punto de comparación simple. RandomForest captura relaciones no lineales entre variables.

---

## Resultados

| Modelo           | MAE    | RMSE   | R²     |
|------------------|--------|--------|--------|
| LinearRegression | 2.7950 | 6.3135 | 0.9073 |
| RandomForest     | 0.4714 | 2.6649 | 0.9835 |

El modelo RandomForest obtiene un error promedio de $0.47 por viaje y explica el 98.35% de la variabilidad del monto total.

---

## Autores

Nombre: Ignacio Pizarro, Aracelly Salgado, Lucas Quitral y Gabriel Astorga
Asignatura: ITY1101 Gestión de Datos para IA 
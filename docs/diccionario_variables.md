# Diccionario de Variables — Yellow Taxi NYC

## 1. Variables Nativas (NYC TLC)

| Variable | Tipo de Dato | Descripción |
| :--- | :--- | :--- |
| `VendorID` | `int32` | Código del proveedor del taxímetro (1 = Creative Mobile; 2 = VeriFone). |
| `tpep_pickup_datetime` | `datetime64` | Fecha y hora de inicio del viaje. |
| `tpep_dropoff_datetime` | `datetime64` | Fecha y hora de fin del viaje. |
| `passenger_count` | `float64` | Número de pasajeros en el vehículo. |
| `trip_distance` | `float64` | Distancia recorrida en millas. |
| `RatecodeID` | `float64` | Código de tarifa aplicada (1 = Estándar, 2 = JFK, 3 = Newark, etc). |
| `store_and_fwd_flag` | `object` | Indica si el viaje se guardó en memoria antes de enviarse (Y/N). |
| `PULocationID` | `int32` | Zona TLC donde comenzó el viaje (Origen). |
| `DOLocationID` | `int32` | Zona TLC donde terminó el viaje (Destino). |
| `payment_type` | `int64` | Forma de pago (1 = Tarjeta, 2 = Efectivo, 3 = Sin cargo, 4 = Disputa). |
| `fare_amount` | `float64` | Costo base del viaje según tiempo y distancia. |
| `extra` | `float64` | Cargos adicionales (hora punta o recargo nocturno). |
| `mta_tax` | `float64` | Impuesto fijo de la MTA ($0.50). |
| `tip_amount` | `float64` | Monto de la propina (solo registrado para pagos con tarjeta). |
| `tolls_amount` | `float64` | Suma de peajes pagados en el trayecto. |
| `improvement_surcharge` | `float64` | Recargo fijo por mejora de infraestructura ($1.00). |
| `total_amount` | `float64` | Variable Objetivo. Monto total cobrado al pasajero. |
| `congestion_surcharge` | `float64` | Recargo por congestión en zonas de Manhattan ($2.50). |
| `Airport_fee` | `float64` | Recargo por salida desde aeropuertos ($1.75). |

---

## 2. Variables Creadas (Ingeniería de Características)

### Grupo 1: Temporales
*   **`pickup_hour`** (`int64`): Hora del día (0 a 23).
*   **`pickup_dayofweek`** (`int64`): Día de la semana (0 = Lunes, 6 = Domingo).
*   **`pickup_month`** (`int64`): Mes del viaje (1 a 12).
*   **`is_weekend`** (`int32`): Indica si el viaje ocurrió en fin de semana (1 = Sí, 0 = No).
*   **`is_rush_hour`** (`int32`): Indica si el viaje ocurrió en hora pico (1 = Sí, 0 = No).
*   **`es_temporada_alta`** (`int32`): Indica si coincide con festividades de fin de año (1 = Sí, 0 = No).

### Grupo 2: Duración y Velocidad
*   **`duracion_minutos`** (`float64`): Tiempo transcurrido del viaje en minutos.
*   **`velocidad_promedio_mph`** (`float64`): Velocidad media calculada en millas por hora.

### Grupo 3: Costos y Viaje
*   **`tiene_peaje`** (`int32`): Indica si el viaje registró peajes (1 = Sí, 0 = No).
*   **`tiene_propina`** (`int32`): Indica si el viaje registró propina (1 = Sí, 0 = No).
*   **`porcentaje_propina`** (`float64`): Relación entre la propina y la tarifa base.
*   **`es_aeropuerto`** (`int32`): Indica si el destino u origen corresponde a un aeropuerto (1 = Sí, 0 = No).

### Grupo 4: Categóricas Codificadas
*   `VendorID`, `RatecodeID`, `payment_type`, `PULocationID` y `DOLocationID` convertidas a códigos numéricos indexados con `.cat.codes`.

import pandas as pd

# Variables que NO se pueden usar con target = total_amount (data leakage)
LEAKAGE_COLS = [
    "fare_amount", "tip_amount", "tolls_amount", "extra",
    "mta_tax", "congestion_surcharge", "Airport_fee",
    "improvement_surcharge", "store_and_fwd_flag",
    "tpep_pickup_datetime", "tpep_dropoff_datetime"
]

TARGET = "total_amount"

FEATURES = [
    "pickup_hour", "pickup_dayofweek", "pickup_month",
    "is_weekend", "is_rush_hour","es_temporada_alta",
    "duracion_minutos", "velocidad_promedio_mph",
    "tiene_peaje", "tiene_propina", "porcentaje_propina", "es_aeropuerto",
    "VendorID", "RatecodeID", "payment_type",
    "PULocationID", "DOLocationID",
    "passenger_count", "trip_distance"
]

def preparar_train_test(df: pd.DataFrame):
    df = df.sort_values("tpep_pickup_datetime").reset_index(drop=True)

    X = df[FEATURES]
    y = df[TARGET]

    corte = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:corte], X.iloc[corte:]
    y_train, y_test = y.iloc[:corte], y.iloc[corte:]

    print(f"Train: {len(X_train):,} registros")
    print(f"Test:  {len(X_test):,} registros")

    return X_train, X_test, y_train, y_test
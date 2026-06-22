import pandas as pd

def crear_features(df: pd.DataFrame) -> pd.DataFrame:

    # --- Temporales ---
    df["pickup_hour"]      = pd.to_datetime(df["tpep_pickup_datetime"]).dt.hour
    df["pickup_dayofweek"] = pd.to_datetime(df["tpep_pickup_datetime"]).dt.dayofweek
    df["pickup_month"]     = pd.to_datetime(df["tpep_pickup_datetime"]).dt.month
    df["is_weekend"]       = df["pickup_dayofweek"].isin([5, 6]).astype(int)
    df["is_rush_hour"]     = df["pickup_hour"].isin([7, 8, 9, 16, 17, 18, 19]).astype(int)
    df["es_temporada_alta"] = (
    ((df["pickup_month"] == 12) & (pd.to_datetime(df["tpep_pickup_datetime"]).dt.day >= 24)) |
    ((df["pickup_month"] == 1) & (pd.to_datetime(df["tpep_pickup_datetime"]).dt.day == 1))
    ).astype(int)

    # --- Duración y velocidad ---
    # duracion_minutos ya viene de cleaning.py
    df["velocidad_promedio_mph"] = df["trip_distance"] / (df["duracion_minutos"] / 60)

    # --- Costos y viaje ---
    df["tiene_peaje"]        = (df["tolls_amount"] > 0).astype(int)
    df["tiene_propina"]      = (df["tip_amount"] > 0).astype(int)
    df["porcentaje_propina"] = df["tip_amount"] / df["fare_amount"]
    df["es_aeropuerto"]      = df["RatecodeID"].isin([2, 3]).astype(int)

    # --- Categóricas ---
    df["VendorID"]      = df["VendorID"].astype("category").cat.codes
    df["RatecodeID"]    = df["RatecodeID"].astype("category").cat.codes
    df["payment_type"]  = df["payment_type"].astype("category").cat.codes
    df["PULocationID"]  = df["PULocationID"].astype("category").cat.codes
    df["DOLocationID"]  = df["DOLocationID"].astype("category").cat.codes

    print(f"Features creadas. Shape final: {df.shape}")
    return df
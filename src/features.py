import pandas as pd

TARGET = "total_amount"

def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    total_inicial = len(df)
    log = []

    df = df.copy()
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])

    fecha_inicio = pd.Timestamp("2023-12-01")
    fecha_fin = pd.Timestamp("2024-05-01") 
    df = df[(df["tpep_pickup_datetime"] >= fecha_inicio) & (df["tpep_pickup_datetime"] < fecha_fin)]
    log.append(("Fechas fuera de dic 2023 - abr 2024", total_inicial - len(df)))

    df["duracion_minutos"] = (df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]).dt.total_seconds() / 60

    antes = len(df)
    df = df[(df["trip_distance"] > 0) & (df["trip_distance"] <= 100)]
    log.append(("trip_distance <= 0", antes - len(df)))

    antes = len(df)
    df = df[(df["fare_amount"] > 0) & (df["total_amount"] > 0)]
    log.append(("fare_amount <= 0", antes - len(df)))

    antes = len(df)
    df = df[(df["duracion_minutos"] > 0) & (df["duracion_minutos"] <= 240)]
    log.append(("duracion_minutos <= 0", antes - len(df)))

    antes = len(df)
    df = df[df["passenger_count"].between(1, 8)]
    log.append(("passenger_count inválido", antes - len(df)))

    print("\n--- Reporte de limpieza ---")
    for regla, eliminados in log:
        print(f"  {regla}: {eliminados:,} registros eliminados")
    print(f"\n  Total inicial:  {total_inicial:,}")
    print(f"  Total final:    {len(df):,}")
    print(f"  Registros perdidos: {total_inicial - len(df):,} ({(total_inicial - len(df)) / total_inicial * 100:.2f}%)")

    return df.reset_index(drop=True)


def crear_features(df: pd.DataFrame) -> pd.DataFrame:
    df_feat = df.copy()
    pickup_dt = pd.to_datetime(df_feat["tpep_pickup_datetime"])
    dropoff_dt = pd.to_datetime(df_feat["tpep_dropoff_datetime"])

    df_feat["pickup_hour"] = pickup_dt.dt.hour
    df_feat["pickup_dayofweek"] = pickup_dt.dt.dayofweek
    df_feat["pickup_month"] = pickup_dt.dt.month
    df_feat["is_weekend"] = df_feat["pickup_dayofweek"].isin([5, 6]).astype(int)
    df_feat["is_rush_hour"] = df_feat["pickup_hour"].isin([7, 8, 9, 16, 17, 18, 19]).astype(int)
    df_feat["es_temporada_alta"] = (((df_feat["pickup_month"] == 12) & (pickup_dt.dt.day >= 24)) | 
                                    ((df_feat["pickup_month"] == 1) & (pickup_dt.dt.day == 1))).astype(int)

    df_feat["duracion_minutos"] = (dropoff_dt - pickup_dt).dt.total_seconds() / 60
    df_feat["velocidad_promedio_mph"] = df_feat["trip_distance"] / (df_feat["duracion_minutos"] / 60)
    df_feat["velocidad_promedio_mph"] = df_feat["velocidad_promedio_mph"].fillna(0)

    df_feat["tiene_peaje"] = (df_feat["tolls_amount"] > 0).astype(int)
    df_feat["tiene_propina"] = (df_feat["tip_amount"] > 0).astype(int)
    df_feat["porcentaje_propina"] = df_feat["tip_amount"] / df_feat["fare_amount"]
    df_feat["porcentaje_propina"] = df_feat["porcentaje_propina"].fillna(0)
    df_feat["es_aeropuerto"] = df_feat["RatecodeID"].isin([2, 3]).astype(int)

    for col in ["VendorID", "RatecodeID", "payment_type", "PULocationID", "DOLocationID"]:
        df_feat[col] = df_feat[col].astype("category").cat.codes

    print(f"Features creadas. Shape final: {df_feat.shape}")
    return df_feat


def preparar_train_test(df: pd.DataFrame):
    print("[INFO] Ordenando registros cronológicamente...")
    df = df.sort_values("tpep_pickup_datetime").reset_index(drop=True)

    corte = int(len(df) * 0.8)
    df_train = df.iloc[:corte].reset_index(drop=True)
    df_test  = df.iloc[corte:].reset_index(drop=True)

    print(f"  Registros asignados a Train: {len(df_train):,}")
    print(f"  Registros asignados a Test:  {len(df_test):,}")

    return df_train, df_test

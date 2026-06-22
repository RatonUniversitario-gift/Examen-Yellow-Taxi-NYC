import pandas as pd

def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    total_inicial = len(df)
    log = []

    # Duración en minutos
    df["duracion_minutos"] = (
        pd.to_datetime(df["tpep_dropoff_datetime"]) - 
        pd.to_datetime(df["tpep_pickup_datetime"])
    ).dt.total_seconds() / 60

    # Fechas fuera del período
    fecha_inicio = pd.Timestamp("2023-12-01")
    fecha_fin = pd.Timestamp("2024-05-01") 
    df = df[
        (pd.to_datetime(df["tpep_pickup_datetime"]) >= fecha_inicio) &
        (pd.to_datetime(df["tpep_pickup_datetime"]) < fecha_fin)
    ]
    log.append(("Fechas fuera de dic 2023 - abr 2024", total_inicial - len(df)))

    # trip_distance <= 0
    antes = len(df)
    df = df[df["trip_distance"] > 0]
    log.append(("trip_distance <= 0", antes - len(df)))

    # fare_amount <= 0
    antes = len(df)
    df = df[df["fare_amount"] > 0]
    log.append(("fare_amount <= 0", antes - len(df)))

    # total_amount <= 0
    antes = len(df)
    df = df[df["total_amount"] > 0]
    log.append(("total_amount <= 0", antes - len(df)))

    # duracion_minutos <= 0
    antes = len(df)
    df = df[df["duracion_minutos"] > 0]
    log.append(("duracion_minutos <= 0", antes - len(df)))

    # Duraciones extremas (> 4 horas)
    antes = len(df)
    df = df[df["duracion_minutos"] <= 240]
    log.append(("duracion_minutos > 240", antes - len(df)))

    # Distancias extremas (> 100 millas)
    antes = len(df)
    df = df[df["trip_distance"] <= 100]
    log.append(("trip_distance > 100", antes - len(df)))

    # passenger_count nulo o inválido
    antes = len(df)
    df = df[df["passenger_count"].between(1, 8)]
    log.append(("passenger_count inválido", antes - len(df)))

    # Reporte
    print("\n--- Reporte de limpieza ---")
    for regla, eliminados in log:
        print(f"  {regla}: {eliminados:,} registros eliminados")
    print(f"\n  Total inicial:  {total_inicial:,}")
    print(f"  Total final:    {len(df):,}")
    print(f"  Registros perdidos: {total_inicial - len(df):,} ({(total_inicial - len(df)) / total_inicial * 100:.2f}%)")

    return df.reset_index(drop=True)
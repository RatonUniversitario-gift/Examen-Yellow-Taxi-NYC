import pandas as pd

def preparar_train_test(df: pd.DataFrame):
    """
    Divide el DataFrame ordenándolo cronológicamente en un 80% para 
    entrenamiento (pasado) y un 20% para prueba (futuro).
    
    Recibe el DataFrame limpio original (con sus columnas nativas de fecha y costo).
    """
    # 1. Ordenar por la fecha de recogida nativa
    print("[INFO] Ordenando registros cronológicamente...")
    df = df.sort_values("tpep_pickup_datetime").reset_index(drop=True)

    # 2. Calcular el punto de corte (80% para Train, 20% para Test)
    corte = int(len(df) * 0.8)
    
    # 3. Dividir los DataFrames completos
    df_train = df.iloc[:corte].reset_index(drop=True)
    df_test  = df.iloc[corte:].reset_index(drop=True)

    print(f"  Registros asignados a Train: {len(df_train):,}")
    print(f"  Registros asignados a Test:  {len(df_test):,}")

    return df_train, df_test
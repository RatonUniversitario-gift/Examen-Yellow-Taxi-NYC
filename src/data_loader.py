import pandas as pd
import glob

def cargar_datos(carpeta: str = "data/raw") -> pd.DataFrame:
    rutas = sorted(glob.glob(f"{carpeta}/*.parquet"))
    print(f"Archivos encontrados: {len(rutas)}")
    for r in rutas:
        print(f"  - {r}")
   
    dfs = [pd.read_parquet(r) for r in rutas]
    df = pd.concat(dfs, ignore_index=True)
   
    print(f"Datos cargados: {df.shape[0]:,} filas, {df.shape[1]} columnas")
    print("\n--- Head ---")
    print(df.head())
    print("\n--- Info ---")
    df.info()
    print("\n--- Nulos ---")
    print(df.isnull().sum())
    return df
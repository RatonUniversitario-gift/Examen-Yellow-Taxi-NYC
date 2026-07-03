import os
import glob
import pandas as pd

def cargar_datos(carpeta: str = "data/raw") -> pd.DataFrame:
    # SOLUCIÓN DE RUTA ABSOLUTA: Convierte la ruta relativa en absoluta basada en la terminal actual
    ruta_absoluta = os.path.abspath(carpeta)
    
    rutas = sorted(glob.glob(os.path.join(ruta_absoluta, "*.parquet")))

    print(f"Archivos encontrados: {len(rutas)}")
    for r in rutas:
        print(f"  - {os.path.basename(r)}") # Imprime solo el nombre del archivo para limpiar la consola
   
    dfs = [pd.read_parquet(r) for r in rutas]
    df = pd.concat(dfs, ignore_index=True)
   
    print(f"\nDatos cargados correctamente: {df.shape[0]:,} filas, {df.shape[1]} columnas")
    print("\n--- Head ---")
    print(df.head())
    print("\n--- Info ---")
    df.info()
    print("\n--- Nulos ---")
    print(df.isnull().sum())
    
    return df

import os
import numpy as np
import pandas as pd
import shutil
from src.data_loader import cargar_datos
from src.cleaning import limpiar_datos
from src.features import crear_features
from src.preprocessing import preparar_train_test
from src.modeling import entrenar_modelos, evaluar_modelos, guardar_modelos, cargar_modelos

df_raw   = cargar_datos("data/raw")
df_clean = limpiar_datos(df_raw)
df       = crear_features(df_clean)

os.makedirs("data/processed", exist_ok=True)
df.to_parquet("data/processed/yellow_taxi_limpio.parquet", index=False)
print("Dataset procesado guardado.")

X_train, X_test, y_train, y_test = preparar_train_test(df)

del df, df_clean, df_raw

if os.path.exists("models/RandomForest.pkl"):
    print("Modelos ya existen, cargando...")
    modelos = cargar_modelos()
else:
    modelos = entrenar_modelos(X_train, y_train)
    guardar_modelos(modelos)

metricas = evaluar_modelos(modelos, X_test, y_test)

os.makedirs("data/outputs", exist_ok=True)

metricas.to_csv("data/outputs/metricas_modelos.csv", index=False)
print("Métricas guardadas.")

mejor_modelo = modelos["RandomForest"]
y_pred = mejor_modelo.predict(X_test)

predicciones = pd.DataFrame({
    "y_real": y_test.values,
    "y_pred": y_pred,
    "error":  np.abs(y_test.values - y_pred)
})
predicciones.to_csv("data/outputs/predicciones.csv", index=False)
print("Predicciones guardadas.")

importancia = pd.DataFrame({
    "variable": X_train.columns,
    "importancia": modelos["RandomForest"].feature_importances_
}).sort_values("importancia", ascending=False)

importancia.to_csv("data/outputs/importancia_variables.csv", index=False)
print("Importancia de variables guardada.")

shutil.copy("models/RandomForest.pkl", "models/modelo_final.pkl")
print("Modelo final copiado como modelo_final.pkl")
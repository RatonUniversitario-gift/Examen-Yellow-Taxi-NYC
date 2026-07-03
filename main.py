import os
import numpy as np
import pandas as pd
import shutil
from src.data_loader import cargar_datos
from src.features import limpiar_datos, preparar_train_test, crear_features
from src.modeling import entrenar_modelos, evaluar_modelos, guardar_modelos, cargar_modelos

RUTA = "data/raw"
df_raw = cargar_datos(RUTA)
df_clean = limpiar_datos(df_raw)

df_completo_con_features = crear_features(df_clean)

os.makedirs("data/processed", exist_ok=True)
df_completo_con_features.to_parquet("data/processed/yellow_taxi_limpio.parquet", index=False)
print("Dataset procesado guardado con todas sus variables para Streamlit.")

df_train_raw, df_test_raw = preparar_train_test(df_clean)

del df_clean, df_raw, df_completo_con_features

X_train_raw = crear_features(df_train_raw)
X_test_raw = crear_features(df_test_raw)

FEATURES_ENTRENAMIENTO = [
    "pickup_hour", "pickup_dayofweek", "pickup_month",
    "is_weekend", "is_rush_hour", "es_temporada_alta",
    "es_aeropuerto", "trip_distance", "passenger_count",
    "VendorID", "RatecodeID", "payment_type",
    "PULocationID", "DOLocationID"
]

X_train = X_train_raw[FEATURES_ENTRENAMIENTO]
X_test  = X_test_raw[FEATURES_ENTRENAMIENTO]

y_train = df_train_raw["total_amount"]
y_test  = df_test_raw["total_amount"]

del df_train_raw, df_test_raw, X_train_raw, X_test_raw

if os.path.exists("models/RandomForest.pkl") and os.path.exists("models/LinearRegression.pkl"):
    print("\nModelos ya existen, cargando...")
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
    "importancia": mejor_modelo.feature_importances_
}).sort_values("importancia", ascending=False)

importancia.to_csv("data/outputs/importancia_variables.csv", index=False)
print("Importancia de variables guardada.")

shutil.copy("models/RandomForest.pkl", "models/modelo_final.pkl")
print("Modelo final copiado como modelo_final.pkl")

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import joblib
import os

def entrenar_modelos(X_train, y_train):
    modelos = {
        "LinearRegression": LinearRegression(),
        "RandomForest":     RandomForestRegressor(n_estimators=50, max_depth=15, n_jobs=-1, random_state=42)
    }

    entrenados = {}
    for nombre, modelo in modelos.items():
        print(f"Entrenando {nombre}...")
        modelo.fit(X_train, y_train)
        entrenados[nombre] = modelo
        print(f"  {nombre} listo.")

    return entrenados

def evaluar_modelos(modelos: dict, X_test, y_test) -> pd.DataFrame:
    resultados = []

    for nombre, modelo in modelos.items():
        y_pred = modelo.predict(X_test)
        mae    = mean_absolute_error(y_test, y_pred)
        rmse   = np.sqrt(mean_squared_error(y_test, y_pred))
        r2     = r2_score(y_test, y_pred)

        resultados.append({"modelo": nombre, "MAE": mae, "RMSE": rmse, "R2": r2})
        print(f"\n{nombre} (Métricas):")
        print(f"  MAE (Error promedio):  ${mae:.2f}")
        print(f"  RMSE:                  ${rmse:.2f}")
        print(f"  R²:                    {r2:.4f}")

    return pd.DataFrame(resultados)

def guardar_modelos(modelos: dict, carpeta="models"):
    os.makedirs(carpeta, exist_ok=True)
    for nombre, modelo in modelos.items():
        ruta = os.path.join(carpeta, f"{nombre}.pkl")
        joblib.dump(modelo, ruta)
        print(f"Modelo guardado en {ruta}")

def cargar_modelos(carpeta="models"):
    nombres = ["LinearRegression", "RandomForest"]
    modelos = {}
    for nombre in nombres:
        ruta = os.path.join(carpeta, f"{nombre}.pkl")
        if os.path.exists(ruta):
            modelos[nombre] = joblib.load(ruta)
            print(f"Modelo cargado: {ruta}")
    return modelos

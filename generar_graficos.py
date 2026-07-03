import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("reports/graficos", exist_ok=True)

predicciones = pd.read_csv("data/outputs/predicciones.csv")

fig, ax = plt.subplots(figsize=(8, 5))
limite_target = predicciones["y_real"].quantile(0.99)
ax.hist(predicciones["y_real"], bins=100, range=(0, limite_target), color="#2563eb", edgecolor="white", linewidth=0.2)
ax.set_xlim(0, limite_target)
ax.set_xlabel("total_amount ($)")
ax.set_ylabel("Frecuencia")
ax.set_title("Distribución de la variable objetivo (total_amount)")
plt.tight_layout()
plt.savefig("reports/graficos/distribucion_target.png", dpi=150)
plt.close()

fig, ax = plt.subplots(figsize=(8, 5))
limite_error = predicciones["error"].quantile(0.95)
ax.hist(predicciones["error"], bins=100, range=(0, limite_error), color="#dc2626", edgecolor="white", linewidth=0.2)
ax.set_xlim(0, limite_error)
ax.set_xlabel("Error absoluto ($)")
ax.set_ylabel("Frecuencia")
ax.set_title("Distribución de errores del modelo RandomForest")
plt.tight_layout()
plt.savefig("reports/graficos/errores_modelo.png", dpi=150)
plt.close()

importancia = pd.read_csv("data/outputs/importancia_variables.csv").sort_values("importancia", ascending=True)

fig, ax = plt.subplots(figsize=(8, 7))
ax.barh(importancia["variable"], importancia["importancia"], color="#16a34a")
ax.set_xlabel("Importancia")
ax.set_title("Importancia de variables (RandomForest)")
plt.tight_layout()
plt.savefig("reports/graficos/importancia_variables.png", dpi=150)
plt.close()

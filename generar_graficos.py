import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("reports/graficos", exist_ok=True)

# --- 1. Distribución del target ---
predicciones = pd.read_csv("data/outputs/predicciones.csv")

fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(predicciones["y_real"], bins=80, color="#2563eb", edgecolor="white")
ax.set_xlim(0, predicciones["y_real"].quantile(0.99))  # recorta outliers extremos para visualizar mejor
ax.set_xlabel("total_amount ($)")
ax.set_ylabel("Frecuencia")
ax.set_title("Distribución de la variable objetivo (total_amount)")
plt.tight_layout()
plt.savefig("reports/graficos/distribucion_target.png", dpi=150)
plt.close()
print("Gráfico 1 guardado: distribucion_target.png")

# --- 2. Errores del modelo ---
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(predicciones["error"], range=(0, predicciones["error"].quantile(0.95)), color="#dc2626", edgecolor="white")
ax.set_xlim(0, predicciones["error"].quantile(0.99))
ax.set_xlabel("Error absoluto ($)")
ax.set_ylabel("Frecuencia")
ax.set_title("Distribución de errores del modelo RandomForest")
plt.tight_layout()
plt.savefig("reports/graficos/errores_modelo.png", dpi=150)
plt.close()
print("Gráfico 2 guardado: errores_modelo.png")

# --- 3. Importancia de variables ---
importancia = pd.read_csv("data/outputs/importancia_variables.csv").sort_values("importancia", ascending=True)

fig, ax = plt.subplots(figsize=(8, 7))
ax.barh(importancia["variable"], importancia["importancia"], color="#16a34a")
ax.set_xlabel("Importancia")
ax.set_title("Importancia de variables (RandomForest)")
plt.tight_layout()
plt.savefig("reports/graficos/importancia_variables.png", dpi=150)
plt.close()
print("Gráfico 3 guardado: importancia_variables.png")
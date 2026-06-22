import streamlit as st
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.load_data import cargar_metricas, cargar_predicciones, cargar_importancia

st.title("Evaluación del modelo")

metricas = cargar_metricas()
st.subheader("Métricas por modelo")
st.dataframe(metricas, use_container_width=True)

mejor_modelo = metricas.sort_values("RMSE").iloc[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Mejor modelo", mejor_modelo["modelo"])
col2.metric("MAE", f"{mejor_modelo['MAE']:.2f}")
col3.metric("RMSE", f"{mejor_modelo['RMSE']:.2f}")
col4.metric("R2", f"{mejor_modelo['R2']:.3f}")

try:
    pred = cargar_predicciones()
    muestra = pred.sample(min(5000, len(pred)), random_state=42)
    st.subheader("Valores reales vs predichos (muestra)")
    fig, ax = plt.subplots()
    ax.scatter(muestra["y_real"], muestra["y_pred"], alpha=0.3)
    ax.set_xlabel("Valor real")
    ax.set_ylabel("Valor predicho")
    st.pyplot(fig)

    st.subheader("Distribución de errores")
    fig, ax = plt.subplots()
    ax.hist(pred["error"], bins=100, range=(0, pred["error"].quantile(0.95)))
    ax.set_xlabel("Error absoluto ($)")
    ax.set_ylabel("Frecuencia")
    st.pyplot(fig)
except Exception:
    st.warning("No se encontró archivo de predicciones.")

try:
    importancia = cargar_importancia()
    st.subheader("Importancia de variables")
    fig, ax = plt.subplots(figsize=(8, 7))
    importancia_sorted = importancia.sort_values("importancia", ascending=True)
    ax.barh(importancia_sorted["variable"], importancia_sorted["importancia"])
    ax.set_xlabel("Importancia")
    st.pyplot(fig)
except Exception:
    st.warning("No se encontró archivo de importancia de variables.")
import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.load_data import cargar_datos_procesados

st.title("Indicadores principales")

df = cargar_datos_procesados()

col1, col2, col3 = st.columns(3)
col1.metric("Total de viajes", f"{len(df):,}")
col2.metric("Monto total promedio", f"${df['total_amount'].mean():.2f}")
col3.metric("Tarifa promedio", f"${df['fare_amount'].mean():.2f}")

col4, col5, col6 = st.columns(3)
col4.metric("Distancia promedio", f"{df['trip_distance'].mean():.2f} millas")
col5.metric("Duración promedio", f"{df['duracion_minutos'].mean():.2f} min")
col6.metric("Propina promedio", f"${df['tip_amount'].mean():.2f}")

if "tiene_propina" in df.columns:
    porcentaje_propina = df["tiene_propina"].mean() * 100
    st.metric("Viajes con propina", f"{porcentaje_propina:.1f}%")
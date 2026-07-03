import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.load_data import cargar_datos_procesados

st.title("Exploración de datos")

df = cargar_datos_procesados()

st.subheader("Vista previa")
st.dataframe(df.head(50), use_container_width=True)

col1, col2 = st.columns(2)
col1.metric("Filas", f"{df.shape[0]:,}")
col2.metric("Columnas", f"{df.shape[1]:,}")

st.subheader("Tipos de datos")
st.dataframe(df.dtypes.astype(str).reset_index().rename(columns={"index": "columna", 0: "tipo"}))

st.subheader("Valores nulos")
nulos = df.isnull().sum().reset_index()
nulos.columns = ["columna", "nulos"]
st.dataframe(nulos[nulos["nulos"] > 0], use_container_width=True)

st.subheader("Estadísticas descriptivas")
st.dataframe(df.describe(), use_container_width=True)

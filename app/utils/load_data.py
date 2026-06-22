import pandas as pd
import streamlit as st

@st.cache_data
def cargar_datos_procesados(path="data/processed/yellow_taxi_limpio.parquet"):
    df = pd.read_parquet(path)
    return df

@st.cache_data
def cargar_metricas(path="data/outputs/metricas_modelos.csv"):
    return pd.read_csv(path)

@st.cache_data
def cargar_predicciones(path="data/outputs/predicciones.csv"):
    return pd.read_csv(path)

@st.cache_data
def cargar_importancia(path="data/outputs/importancia_variables.csv"):
    return pd.read_csv(path)
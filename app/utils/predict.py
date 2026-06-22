import joblib
import streamlit as st

@st.cache_resource
def cargar_modelo(path="models/modelo_final.pkl"):
    return joblib.load(path)
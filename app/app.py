import streamlit as st

st.set_page_config(
    page_title="Yellow Taxi NYC Analytics",
    page_icon="🚕",
    layout="wide"
)

st.title("Yellow Taxi NYC Analytics")

st.markdown("""
## Sistema de consulta, análisis y predicción de viajes

Esta aplicación permite explorar datos procesados del dataset Yellow Taxi NYC,
consultar indicadores operacionales y utilizar un modelo de Machine Learning
para estimar el monto total de un viaje.

### Funcionalidades principales
- Exploración del dataset procesado.
- Consulta de viajes mediante filtros.
- Visualización de indicadores.
- Evaluación del modelo predictivo.
- Predicción de nuevos viajes.
""")

st.info("Utilice el menú lateral para navegar entre las secciones de la aplicación.")
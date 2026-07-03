import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.load_data import cargar_modelo

st.title("Predicción de viajes")

modelo = cargar_modelo()

st.subheader("Ingrese los datos para la cotización del viaje")

col1, col2, col3 = st.columns(3)
with col1:
    pickup_hour = st.slider("Hora de inicio", 0, 23, 12)
    pickup_month = st.selectbox("Mes del viaje", [12, 1, 2, 3, 4], index=1)
    passenger_count = st.number_input("Cantidad de pasajeros", min_value=1, max_value=8, value=1)

with col2:
    pickup_dayofweek = st.selectbox("Día de la semana (0=Lunes, 6=Domingo)", [0, 1, 2, 3, 4, 5, 6], index=0)
    trip_distance = st.number_input("Distancia estimada (millas por GPS)", min_value=0.1, value=2.5)
    payment_type = st.selectbox("Método de pago preseleccionado", [1, 2, 3, 4, 5, 6])

with col3:
    VendorID = st.selectbox("ID del Proveedor (VendorID)", [1, 2])
    RatecodeID = st.selectbox("Código de Tarifa (RatecodeID)", [1, 2, 3, 4, 5, 6, 99])
    PULocationID = st.number_input("Zona de Origen (PULocationID)", min_value=1, max_value=265, value=161)
    DOLocationID = st.number_input("Zona de Destino (DOLocationID)", min_value=1, max_value=265, value=236)

is_weekend = 1 if pickup_dayofweek in [5, 6] else 0
is_rush_hour = 1 if pickup_hour in [7, 8, 9, 16, 17, 18, 19] else 0
es_temporada_alta = 1 if pickup_month == 12 else 0
es_aeropuerto = 1 if RatecodeID in [2, 3] else 0

input_data = pd.DataFrame([{
    "pickup_hour": pickup_hour,
    "pickup_dayofweek": pickup_dayofweek,
    "pickup_month": pickup_month,
    "is_weekend": is_weekend,
    "is_rush_hour": is_rush_hour,
    "es_temporada_alta": es_temporada_alta,
    "es_aeropuerto": es_aeropuerto,
    "trip_distance": trip_distance,
    "passenger_count": passenger_count,
    "VendorID": VendorID,
    "RatecodeID": RatecodeID,
    "payment_type": payment_type,
    "PULocationID": PULocationID,
    "DOLocationID": DOLocationID,
}])

st.markdown("### Vector de características a evaluar (14 Features):")
st.dataframe(input_data, use_container_width=True)

if st.button("Calcular Tarifa Estimada", type="primary"):
    try:
        prediccion = modelo.predict(input_data)[0]
        st.success(f"### Monto total estimado para el viaje: ${prediccion:.2f}")
        st.info("💡 *Este cálculo simula una cotización previa al viaje libre de Data Leakage, considerando factores de tráfico histórico por zona y horario.*")
    except Exception as e:
        st.error(f"Error al realizar la predicción. Verifica que el modelo corresponda al set de 14 variables. Detalle: {e}")

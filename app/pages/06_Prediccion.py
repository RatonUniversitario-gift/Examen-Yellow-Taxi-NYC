import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.predict import cargar_modelo

st.title("Predicción de viajes")

modelo = cargar_modelo()

st.subheader("Ingrese los datos del viaje")

pickup_hour = st.slider("Hora de inicio", 0, 23, 12)
pickup_dayofweek = st.selectbox("Día de la semana (0=lunes, 6=domingo)", [0, 1, 2, 3, 4, 5, 6])
pickup_month = st.selectbox("Mes", [12, 1, 2, 3, 4])
passenger_count = st.number_input("Cantidad de pasajeros", min_value=1, max_value=8, value=1)
trip_distance = st.number_input("Distancia del viaje en millas", min_value=0.1, value=2.5)
duracion_minutos = st.number_input("Duración estimada del viaje en minutos", min_value=1.0, value=15.0)
VendorID = st.selectbox("VendorID", [1, 2, 6, 7])
RatecodeID = st.selectbox("RatecodeID", [1, 2, 3, 4, 5, 6, 99])
payment_type = st.selectbox("Tipo de pago", [0, 1, 2, 3, 4, 5, 6])
PULocationID = st.number_input("Zona origen", min_value=1, max_value=265, value=161)
DOLocationID = st.number_input("Zona destino", min_value=1, max_value=265, value=236)
tiene_peaje = st.checkbox("¿Tuvo peaje?")
tiene_propina = st.checkbox("¿Tuvo propina?", value=True)
porcentaje_propina = st.number_input("Porcentaje de propina (sobre fare_amount)", min_value=0.0, value=0.15)

is_weekend = 1 if pickup_dayofweek in [5, 6] else 0
is_rush_hour = 1 if pickup_hour in [7, 8, 9, 16, 17, 18, 19] else 0
es_temporada_alta = 1 if pickup_month == 12 else 0
es_aeropuerto = 1 if RatecodeID in [2, 3] else 0
velocidad_promedio_mph = trip_distance / (duracion_minutos / 60) if duracion_minutos > 0 else 0

input_data = pd.DataFrame([{
    "pickup_hour": pickup_hour,
    "pickup_dayofweek": pickup_dayofweek,
    "pickup_month": pickup_month,
    "is_weekend": is_weekend,
    "is_rush_hour": is_rush_hour,
    "es_temporada_alta": es_temporada_alta,
    "duracion_minutos": duracion_minutos,
    "velocidad_promedio_mph": velocidad_promedio_mph,
    "tiene_peaje": int(tiene_peaje),
    "tiene_propina": int(tiene_propina),
    "porcentaje_propina": porcentaje_propina,
    "es_aeropuerto": es_aeropuerto,
    "VendorID": VendorID,
    "RatecodeID": RatecodeID,
    "payment_type": payment_type,
    "PULocationID": PULocationID,
    "DOLocationID": DOLocationID,
    "passenger_count": passenger_count,
    "trip_distance": trip_distance,
}])

st.dataframe(input_data, use_container_width=True)

if st.button("Realizar predicción"):
    prediccion = modelo.predict(input_data)[0]
    st.success(f"Monto total estimado: ${prediccion:.2f}")
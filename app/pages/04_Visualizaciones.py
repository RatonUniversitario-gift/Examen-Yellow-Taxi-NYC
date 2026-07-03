import streamlit as st
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.load_data import cargar_datos_procesados

st.title("Visualizaciones")

df = cargar_datos_procesados()

st.subheader("Cantidad de viajes por hora")
viajes_hora = df.groupby("pickup_hour").size()
fig, ax = plt.subplots()
ax.bar(viajes_hora.index, viajes_hora.values)
ax.set_xlabel("Hora del día")
ax.set_ylabel("Cantidad de viajes")
st.pyplot(fig)

st.subheader("Monto promedio por hora")
monto_hora = df.groupby("pickup_hour")["total_amount"].mean()
fig, ax = plt.subplots()
ax.plot(monto_hora.index, monto_hora.values, marker="o")
ax.set_xlabel("Hora del día")
ax.set_ylabel("Monto promedio")
st.pyplot(fig)

st.subheader("Relación entre distancia y monto total")
muestra = df.sample(min(5000, len(df)), random_state=42)
fig, ax = plt.subplots()
ax.scatter(muestra["trip_distance"], muestra["total_amount"], alpha=0.3)
ax.set_xlabel("Distancia del viaje")
ax.set_ylabel("Monto total")
st.pyplot(fig)

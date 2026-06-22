import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.load_data import cargar_datos_procesados

st.title("Consulta de viajes")

df = cargar_datos_procesados()

st.sidebar.header("Filtros")

hora_min, hora_max = st.sidebar.slider(
    "Rango horario",
    min_value=0,
    max_value=23,
    value=(0, 23)
)

dist_min = float(df["trip_distance"].min())
dist_max = float(df["trip_distance"].quantile(0.95))

distancia_min, distancia_max = st.sidebar.slider(
    "Rango de distancia",
    min_value=dist_min,
    max_value=dist_max,
    value=(dist_min, dist_max)
)

payment_options = sorted(df["payment_type"].dropna().unique())
payment_selected = st.sidebar.multiselect(
    "Tipo de pago",
    payment_options,
    default=payment_options
)

vendor_options = sorted(df["VendorID"].dropna().unique())
vendor_selected = st.sidebar.multiselect(
    "Vendor",
    vendor_options,
    default=vendor_options
)

df_filtrado = df[
    (df["pickup_hour"].between(hora_min, hora_max)) &
    (df["trip_distance"].between(distancia_min, distancia_max)) &
    (df["payment_type"].isin(payment_selected)) &
    (df["VendorID"].isin(vendor_selected))
]

st.write(f"Registros encontrados: {len(df_filtrado):,}")
st.dataframe(df_filtrado.head(200), use_container_width=True)

csv = df_filtrado.head(5000).to_csv(index=False).encode("utf-8")
st.download_button(
    "Descargar datos filtrados (muestra de 5000)",
    data=csv,
    file_name="viajes_filtrados.csv",
    mime="text/csv"
)
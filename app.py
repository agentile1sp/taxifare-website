import streamlit as st

import requests
from datetime import datetime

st.title("TaxiFareModel front")
st.write("Selecciona los parámetros del viaje y calculamos la tarifa.")

# ---- Controles (inputs) ----
col1, col2 = st.columns(2)
with col1:
    date = st.date_input("Fecha de pickup")
    time = st.time_input("Hora de pickup")
with col2:
    passenger_count = st.number_input("Pasajeros", min_value=1, max_value=8, value=1)

pickup_longitude = st.number_input("Pickup longitude", value=-73.985428, format="%.6f")
pickup_latitude  = st.number_input("Pickup latitude",  value=40.748817,  format="%.6f")
dropoff_longitude = st.number_input("Dropoff longitude", value=-73.985000, format="%.6f")
dropoff_latitude  = st.number_input("Dropoff latitude",  value=40.758896,  format="%.6f")

# ---- Armar parámetros para la API ----
pickup_datetime = datetime.combine(date, time).strftime("%Y-%m-%d %H:%M:%S")

params = {
    "pickup_datetime": pickup_datetime,     # ojo: usualmente en UTC
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": int(passenger_count),
}

API_URL = "https://taxifare.lewagon.ai/predict"

# ---- Botón para predecir ----
if st.button("Calcular tarifa"):
    try:
        # en muchos ejercicios es GET; si tu API es POST, usa requests.post y json=params
        r = requests.get(API_URL, params=params, timeout=10)
        r.raise_for_status()
        result = r.json()  # típicamente {'fare': 12.34} o {'prediction': 12.34}
        # detectar la key
        fare = result.get("fare") or result.get("prediction")
        if fare is None:
            st.error(f"No encontré la tarifa en la respuesta: {result}")
        else:
            st.subheader(f"💵 Tarifa estimada: ${fare:,.2f}")
    except Exception as e:
        st.error(f"Falló la llamada a la API: {e}")

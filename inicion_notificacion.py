import streamlit as st
from datetime import datetime

def mostrar_recordatorio():
    # Obtener el día actual
    dia_actual = datetime.now().day

    # Verificar si es el día 12 o 27
    if dia_actual == 12 or dia_actual == 25:
        st.markdown(" # Recuerde realizar la conciliación bancaria")
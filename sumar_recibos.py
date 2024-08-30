import streamlit as st
import pandas as pd
import os

def sumar_recibos_excel():
    st.title("Sumador de Recibos Excel")

    uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

    if uploaded_file is not None:
        # Leer el archivo de Excel
        df = pd.read_excel(uploaded_file)

        # Verificar si las columnas necesarias existen
        if 'RECIBO' not in df.columns or 'Valor' not in df.columns:
            st.error("El archivo debe contener las columnas 'RECIBO' y 'Valor'")
            return

        # Agrupar por RECIBO y sumar los valores
        df_sumado = df.groupby('RECIBO')['Valor'].sum().reset_index()

        # Crear un nuevo nombre de archivo
        nombre_original = os.path.splitext(uploaded_file.name)[0]
        nuevo_nombre = f"Suma de recibos de - {nombre_original}.xlsx"

        # Guardar el nuevo dataframe en un archivo de Excel
        df_sumado.to_excel(nuevo_nombre, index=False)

        # Botón para descargar el archivo
        with open(nuevo_nombre, "rb") as file:
            st.download_button(
                label="Descargar archivo procesado",
                data=file,
                file_name=nuevo_nombre,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # Eliminar el archivo temporal después de la descarga
        os.remove(nuevo_nombre)

        # Mostrar una vista previa de los datos
        st.write("Vista previa de los datos sumados:")
        st.dataframe(df_sumado)
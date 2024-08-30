import streamlit as st
import pandas as pd
import io

def suma_recibos():
    st.title("Suma de Recibos por Excel")

    uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

    if uploaded_file is not None:
        # Leer el archivo de Excel
        df = pd.read_excel(uploaded_file)

        # Verificar si las columnas necesarias existen
        if 'RECIBO' not in df.columns or 'VALOR' not in df.columns:
            st.error("El archivo debe contener las columnas 'RECIBO' y 'VALOR'")
            return

        # Agrupar por RECIBO y sumar los VALORES
        df_sumado = df.groupby('RECIBO')['VALOR'].sum().reset_index()

        # Crear un nuevo nombre de archivo
        nuevo_nombre = f"Suma de recibos de - {uploaded_file.name}"

        # Crear un objeto BytesIO para guardar el Excel en memoria
        output = io.BytesIO()

        # Guardar el DataFrame sumado en un nuevo archivo de Excel
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_sumado.to_excel(writer, index=False, sheet_name='Suma de Recibos')

        # Preparar el archivo para descarga
        output.seek(0)

        # Botón de descarga
        st.download_button(
            label="Descargar archivo procesado",
            data=output,
            file_name=nuevo_nombre,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # Mostrar una vista previa de los resultados
        st.write("Vista previa de los resultados:")
        st.dataframe(df_sumado)
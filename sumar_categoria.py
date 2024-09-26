import streamlit as st
import pandas as pd
import numpy as np


def to_numeric(val):
    try:
        # Primero, intentamos convertir a float
        return float(val)
    except ValueError:
        # Si falla, intentamos limpiar la cadena y convertir nuevamente
        try:
            # Eliminamos comas y espacios, y reemplazamos - con 0
            cleaned = val.replace(',', '').replace(' ', '').replace('-', '0')
            return float(cleaned)
        except:
            return np.nan


def clean_category(val):
    if pd.isna(val) or not isinstance(val, str):
        return 'Sin categoría'
    return str(val).strip()


def sumarcategoria():
    st.title("Suma de Valores por Categoría")

    uploaded_file = st.file_uploader("Sube el archivo Excel", type=["xlsx"])

    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            required_columns = ['SUCURSAL/CANAL', 'DESCRIPCIÓN', 'VALOR']
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                st.error(f"Error: El archivo no contiene las columnas necesarias: {', '.join(missing_columns)}")
            else:
                # Limpiar y convertir datos
                df['VALOR'] = df['VALOR'].apply(to_numeric)
                df['SUCURSAL/CANAL'] = df['SUCURSAL/CANAL'].apply(clean_category)
                df['DESCRIPCIÓN'] = df['DESCRIPCIÓN'].apply(clean_category)

                # Eliminar filas donde VALOR es NaN
                df = df.dropna(subset=['VALOR'])

                st.success("Archivo cargado y procesado correctamente")

                # Combinar las categorías de ambas columnas
                categories = sorted(set(df['SUCURSAL/CANAL'].unique()) | set(df['DESCRIPCIÓN'].unique()))

                selected_category = st.selectbox("Selecciona una categoría", categories)

                # Filtrar el DataFrame para la categoría seleccionada
                filtered_df = df[(df['SUCURSAL/CANAL'] == selected_category) | (df['DESCRIPCIÓN'] == selected_category)]

                # Calcular la suma de VALOR para la categoría seleccionada
                suma = filtered_df['VALOR'].sum()

                # Mostrar resultados
                st.header("Resultados")
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Categoría seleccionada", selected_category)

                with col2:
                    st.metric("Suma total", f"${suma:,.2f}")

                with col3:
                    st.metric("Cantidad de datos sumados", len(filtered_df))

                # Mostrar los datos filtrados
                st.subheader("Datos de la categoría seleccionada")
                st.dataframe(filtered_df)

        except Exception as e:
            st.error(f"Error al procesar el archivo: {str(e)}")
            st.write("Detalles del error:")
            st.exception(e)
    else:
        st.warning("Por favor, sube un archivo Excel.")


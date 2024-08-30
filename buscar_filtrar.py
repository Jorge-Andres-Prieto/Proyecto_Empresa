import streamlit as st
import pandas as pd

def buscar_y_filtrar():
    st.title("Buscar y Filtrar Datos")

    # Subir archivo Excel
    uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

    if uploaded_file is not None:
        # Leer el archivo Excel
        df = pd.read_excel(uploaded_file)

        # Convertir todas las columnas a tipo string
        df = df.astype(str)

        # Campo de búsqueda
        search_term = st.text_input("Ingrese el término de búsqueda:")

        if st.button("Buscar"):
            if search_term:
                # Convertir el término de búsqueda a minúsculas
                search_term_lower = search_term.lower()

                # Filtrar el DataFrame
                filtered_df = df[df.apply(lambda row: row.astype(str).str.lower().str.contains(search_term_lower).any(), axis=1)]

                if not filtered_df.empty:
                    st.write(f"Resultados para '{search_term}':")
                    st.dataframe(filtered_df)
                else:
                    st.warning("No se encontraron resultados para la búsqueda.")
            else:
                st.warning("Por favor, ingrese un término de búsqueda.")
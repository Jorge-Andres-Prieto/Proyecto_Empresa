import streamlit as st
import pandas as pd
import io


def to_numeric(val):
    try:
        return pd.to_numeric(val)
    except ValueError:
        return 0


def verify_file(df, required_columns, file_name):
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return f"Error: El archivo {file_name} no contiene las columnas necesarias: {', '.join(missing_columns)}"
    return None


def app():
    st.title("Conciliación Bancaria ")

    # Crear dos columnas
    col1, col2 = st.columns(2)

    df1 = None
    df2 = None
    error_message = None

    with col1:
        st.header("Informe de banco")
        uploaded_file1 = st.file_uploader("Sube el primer archivo Excel", type=["xlsx"])

        if uploaded_file1 is not None:
            try:
                df1 = pd.read_excel(uploaded_file1)
                error = verify_file(df1, ['SUCURSAL/CANAL', 'VALOR'], "primer")
                if error:
                    st.error(error)
                    error_message = error
                else:
                    df1['VALOR'] = df1['VALOR'].apply(to_numeric)
                    st.success("Primer archivo cargado correctamente")
                    option = st.selectbox("Elige una opción", ["SANTUARIO", "CNB REDES"])
            except Exception as e:
                st.error(f"Error al cargar el primer archivo: {str(e)}")
                error_message = f"Error al cargar el primer archivo: {str(e)}"
        else:
            st.warning("Por favor, sube el primer archivo Excel.")

    with col2:
        st.header("Informe de sede")
        uploaded_file2 = st.file_uploader("Sube el segundo archivo Excel", type=["xlsx"])

        if uploaded_file2 is not None:
            try:
                df2 = pd.read_excel(uploaded_file2, sheet_name='Incorrecto')
                error = verify_file(df2, ['VALOR'], "segundo")
                if error:
                    st.error(error)
                    error_message = error
                else:
                    df2['VALOR'] = df2['VALOR'].apply(to_numeric)
                    st.success("Segundo archivo cargado correctamente")
            except Exception as e:
                st.error(f"Error al cargar el segundo archivo: {str(e)}")
                error_message = f"Error al cargar el segundo archivo: {str(e)}"
        else:
            st.warning("Por favor, sube el segundo archivo Excel.")

    # Sección de resultados
    if df1 is not None and df2 is not None and error_message is None:
        st.header("Resultados")

        suma1 = df1[df1['SUCURSAL/CANAL'] == option]['VALOR'].sum()
        suma2 = df2['VALOR'].sum()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(f"Total {option}", f"${suma1:,.2f}")

        with col2:
            st.metric("Total Segundo Archivo", f"${suma2:,.2f}")

        with col3:
            diferencia = abs(suma1 - suma2)
            st.metric("Diferencia", f"${diferencia:,.2f}")

        if diferencia == 0:
            st.success("Las cantidades son exactamente iguales.")
        else:
            st.info(f"Hay una diferencia de ${diferencia:,.2f} entre los totales.")
    elif error_message:
        st.error("No se pueden mostrar los resultados debido a errores en la carga de archivos.")
    else:
        st.warning("Por favor, sube ambos archivos para ver los resultados.")


if __name__ == "__main__":
    app()
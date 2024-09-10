import streamlit as st
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfgen import canvas
from io import BytesIO

def create_pdf(data):
    # El código de la función create_pdf permanece igual
    # ...

def main():
    st.title("Formulario de Transferencia")

    # Inicializar la lista de instrumentos en el estado de la sesión si no existe
    if 'instrumentos' not in st.session_state:
        st.session_state.instrumentos = []

    # Formulario principal
    with st.form("transferencia_form"):
        tipo_transferencia = st.selectbox("Tipo de transferencia", ["Emisora", "Receptora"])
        
        col1, col2 = st.columns(2)
        with col1:
            num_depositante_origen = st.text_input("Número de depositante origen")
            nombre_depositante_origen = st.text_input("Nombre de depositante origen")
            num_comitente_origen = st.text_input("Número de comitente origen")
        
        with col2:
            num_depositante_destino = st.text_input("Número de depositante destino")
            nombre_depositante_destino = st.text_input("Nombre de depositante destino")
            num_comitente_destino = st.text_input("Número de comitente destino")

        st.subheader("Instrumentos")
        
        # Mostrar la tabla de instrumentos si hay alguno
        if st.session_state.instrumentos:
            st.table(pd.DataFrame(st.session_state.instrumentos))

        # Botón de envío del formulario principal
        submitted = st.form_submit_button("Enviar")

    # Formulario para agregar instrumentos (fuera del formulario principal)
    with st.form("agregar_instrumento"):
        st.subheader("Agregar nuevo instrumento")
        col1, col2 = st.columns(2)
        with col1:
            ticker = st.text_input("Ticker del instrumento")
        with col2:
            cantidad = st.number_input("Cantidad", min_value=0, step=1)
        
        agregar_instrumento = st.form_submit_button("Agregar Instrumento")

        if agregar_instrumento:
            st.session_state.instrumentos.append({"ticker": ticker, "cantidad": cantidad})
            st.experimental_rerun()

    if submitted:
        data = {
            "Tipo de transferencia": tipo_transferencia,
            "Número de depositante origen": num_depositante_origen,
            "Nombre de depositante origen": nombre_depositante_origen,
            "Número de comitente origen": num_comitente_origen,
            "Número de depositante destino": num_depositante_destino,
            "Nombre de depositante destino": nombre_depositante_destino,
            "Número de comitente destino": num_comitente_destino,
            "instrumentos": st.session_state.instrumentos
        }

        pdf = create_pdf(data)
        st.success("Formulario enviado con éxito")
        st.download_button(
            label="Descargar PDF",
            data=pdf,
            file_name="transferencia.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()

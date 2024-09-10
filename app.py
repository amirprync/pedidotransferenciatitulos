import streamlit as st
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def create_pdf(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    
    # Datos principales
    elements.append(Paragraph("Datos de la Transferencia", title_style))
    data_list = [[k, v] for k, v in data.items() if k != "instrumentos"]
    t = Table(data_list)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.grey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (1, 0), (-1, -1), colors.beige),
        ('TEXTCOLOR', (1, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (1, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(t)

    # Instrumentos
    elements.append(Paragraph("Instrumentos", title_style))
    if data["instrumentos"]:
        instrumentos_list = [["Ticker", "Cantidad"]] + [[i["ticker"], i["cantidad"]] for i in data["instrumentos"]]
        t_instrumentos = Table(instrumentos_list)
        t_instrumentos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(t_instrumentos)
    else:
        elements.append(Paragraph("No se agregaron instrumentos.", styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return buffer

def main():
    st.title("Formulario de Transferencia de titutlos")

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

        # Botón de envío del formulario principal (al final)
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

    if agregar_instrumento and ticker and cantidad > 0:
        st.session_state.instrumentos.append({"ticker": ticker, "cantidad": cantidad})
        st.success(f"Instrumento {ticker} agregado con cantidad {cantidad}")

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
            label="Descargar PDF - Recorda que este PDF debe ser enviado a la casilla titulos@cohen.com.ar. Siempre desde la casilla declarada por el comitente ",
            data=pdf,
            file_name="transferencia.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()

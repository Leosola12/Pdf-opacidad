import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO

def create_opacity_overlay(width, height, opacity):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(width, height))
    c.setFillAlpha(opacity)
    c.setFillColorRGB(1, 1, 1)  # Blanco
    c.rect(0, 0, width, height, fill=1, stroke=0)
    c.save()
    buffer.seek(0)
    return buffer

def reduce_opacity(input_pdf, opacity):
    input_reader = PdfReader(input_pdf)
    output_writer = PdfWriter()

    for page in input_reader.pages:
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        overlay_stream = create_opacity_overlay(width, height, opacity)
        overlay_pdf = PdfReader(overlay_stream)
        overlay_page = overlay_pdf.pages[0]

        page.merge_page(overlay_page)
        output_writer.add_page(page)

    output_pdf = BytesIO()
    output_writer.write(output_pdf)
    output_pdf.seek(0)
    return output_pdf

# Streamlit UI
st.set_page_config(page_title="Reductor de Opacidad PDF", layout="centered")
st.title("🔍 Reductor Automático de Opacidad para PDFs")
st.write("Subí un PDF y descargá versiones con distintas opacidades para ahorrar tinta.")

uploaded_file = st.file_uploader("📄 Subí tu PDF", type=["pdf"])

if uploaded_file:
    if st.button("Procesar PDF con múltiples opacidades"):
        with st.spinner("Procesando... Esto puede tardar unos segundos."):
            resultados = {}
            for opacidad in [0.1, 0.2, 0.3, 0.4, 0.5]:
                processed = reduce_opacity(uploaded_file, opacidad)
                resultados[f"{int(opacidad * 100)}%"] = processed

        st.success("✅ PDFs procesados correctamente. Elegí una versión para descargar:")
        for label, data in resultados.items():
            st.download_button(
                label=f"📥 Descargar versión con {label} de opacidad",
                data=data,
                file_name=f"pdf_opacidad_{label}.pdf",
                mime="application/pdf"
            )

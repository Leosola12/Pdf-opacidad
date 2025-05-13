import streamlit as st
import io
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

# Subida del archivo PDF
st.title("Reducción de Opacidad en PDFs")
st.write("Sube tu archivo PDF y elige el nivel de opacidad.")
pdf_file = st.file_uploader("Sube un archivo PDF", type="pdf")

if pdf_file is not None:
    # Lectura del archivo PDF
    pdf_bytes = pdf_file.read()
    pdf_reader = PdfReader(io.BytesIO(pdf_bytes))

    # Opciones de opacidad (del 10% al 50%)
    opacities = [i / 100 for i in range(10, 51, 10)]
    selected_opacity = st.selectbox("Elige el nivel de opacidad", opacities, format_func=lambda x: f"{int(x * 100)}%")

    # Procesar el PDF con la opacidad seleccionada
    if st.button("Generar PDF con opacidad"):
        writer = PdfWriter()

        for page_num in range(len(pdf_reader.pages)):
            original_page = pdf_reader.pages[page_num]
            width = float(original_page.mediabox.width)
            height = float(original_page.mediabox.height)

            # Crear la capa de opacidad en memoria
            with io.BytesIO() as overlay_stream:
                c = canvas.Canvas(overlay_stream, pagesize=(width, height))
                c.setFillAlpha(selected_opacity)
                c.setFillColorRGB(1, 1, 1)  # blanco transparente
                c.rect(0, 0, width, height, fill=1)
                c.save()
                overlay_stream.seek(0)

                overlay_pdf = PdfReader(overlay_stream)
                overlay_page = overlay_pdf.pages[0]

                # Clonar la página original y superponer la capa de opacidad
                original_page.merge_page(overlay_page)
                writer.add_page(original_page)

        # Guardar el archivo PDF resultante
        output_pdf_path = "output_opacity.pdf"
        with open(output_pdf_path, "wb") as f:
            writer.write(f)

        st.success(f"✔️ PDF con opacidad {int(selected_opacity * 100)}% generado exitosamente.")
        
        # Permitir la descarga del PDF generado
        with open(output_pdf_path, "rb") as f:
            st.download_button("Descargar PDF", f, file_name=output_pdf_path)

import streamlit as st
import io
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas

def reduce_opacity(pdf_file, opacities):
    reader = PdfReader(pdf_file)
    results = {}

    for opacity in opacities:
        writer = PdfWriter()
        for i in range(len(reader.pages)):
            original_page = reader.pages[i]
            width = float(original_page.mediabox.width)
            height = float(original_page.mediabox.height)

            with io.BytesIO() as overlay_stream:
                c = canvas.Canvas(overlay_stream, pagesize=(width, height))
                c.setFillAlpha(opacity)
                c.setFillColorRGB(1, 1, 1)  # blanco transparente
                c.rect(0, 0, width, height, fill=1)
                c.save()
                overlay_stream.seek(0)

                overlay_pdf = PdfReader(overlay_stream)
                overlay_page = overlay_pdf.pages[0]

                original_page.merge_page(overlay_page)
                writer.add_page(original_page)

        output = io.BytesIO()
        writer.write(output)
        output.seek(0)
        results[f"PDF con {int(opacity*100)}% de opacidad"] = output

    return results

# Interfaz
st.title("🖋️ Reductor de opacidad de PDF")

uploaded_file = st.file_uploader("📤 Subí tu archivo PDF", type="pdf")

if uploaded_file:
    st.success("✅ Archivo cargado correctamente.")

    selected_opacities = st.multiselect(
        "Seleccioná los niveles de opacidad a aplicar:",
        [10, 20, 30, 40, 50],
        default=[10, 20, 30, 40, 50]
    )

    if st.button("Procesar PDF"):
        with st.spinner("Procesando..."):
            opacities = [i / 100 for i in selected_opacities]
            outputs = reduce_opacity(uploaded_file, opacities)

        st.success("🎉 PDFs generados:")
        for label, pdf_bytes in outputs.items():
            st.download_button(
                label=f"⬇️ Descargar {label}",
                data=pdf_bytes,
                file_name=f"{label.replace('%', '')}.pdf",
                mime="application/pdf"
            )

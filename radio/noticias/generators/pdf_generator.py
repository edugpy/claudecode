import os
from datetime import datetime
from fpdf import FPDF


class BulletinPDF(FPDF):
    def __init__(self, radio_name: str):
        super().__init__()
        self.radio_name = radio_name

    def header(self):
        # Franja de cabecera
        self.set_fill_color(20, 60, 140)
        self.rect(0, 0, 210, 20, style="F")
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(255, 255, 255)
        self.set_y(4)
        self.cell(0, 8, self.radio_name, align="C", new_x="LMARGIN", new_y="NEXT")

        self.set_font("Helvetica", "", 9)
        self.set_text_color(200, 215, 255)
        now = datetime.now().strftime("%d/%m/%Y  %H:%M hs")
        self.cell(0, 5, f"Boletin de Noticias  —  {now}", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(6)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, f"Pagina {self.page_no()}  —  {self.radio_name}", align="C")


def generate_pdf(news_list: list, output_dir: str, radio_name: str) -> str:
    """Genera el boletin en PDF. Retorna la ruta del archivo generado."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filepath = os.path.join(output_dir, f"boletin_{timestamp}.pdf")

    pdf = BulletinPDF(radio_name)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Agrupar por fuente
    sources: dict = {}
    for item in news_list:
        sources.setdefault(item["source"], []).append(item)

    for source_name, items in sources.items():
        # Encabezado de fuente
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_fill_color(230, 237, 255)
        pdf.set_text_color(20, 60, 140)
        pdf.cell(0, 7, f"  {source_name}", fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

        for item in items:
            # Titulo
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(15, 15, 15)
            pdf.multi_cell(0, 6, item["title"])

            # Resumen
            if item.get("summary"):
                pdf.set_font("Helvetica", "", 9)
                pdf.set_text_color(60, 60, 60)
                pdf.multi_cell(0, 5, item["summary"])

            # Hora y URL
            pub = item["published"]
            pub_str = pub.strftime("%H:%M") if hasattr(pub, "strftime") else ""
            pdf.set_font("Helvetica", "I", 8)
            pdf.set_text_color(130, 130, 130)
            pdf.cell(0, 5, f"{pub_str}  |  {item['url']}", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)

        pdf.ln(3)

    pdf.output(filepath)
    print(f"  [OK] PDF generado: {filepath}")
    return filepath

import os
import webbrowser

from fpdf import FPDF


class PdfReport:
    def __init__(self, filename):
        self.filename = filename

    def _make_uri(self):
        return "file://" + os.path.realpath(self.filename)

    def open(self):
        URI = self._make_uri()
        webbrowser.open(URI)

    def generate(self, bill, flatmates):
        pdf = FPDF(orientation="P", unit="pt", format="A4")
        pdf.add_page()
        image_path = os.path.join(os.getcwd(), "files", "house.png")

        pdf.image(name=image_path, w=30, h=30)
        pdf.set_font(family="arial", style="b", size=24)
        pdf.cell(w=0, h=60, txt="Flatmates Bill", align="C", ln=1)

        pdf.set_font(family="arial", style="b", size=14)
        pdf.cell(w=100, h=40, txt="Period:")
        pdf.cell(w=150, h=40, txt=f"{bill.period}", ln=1)

        pdf.set_font(family="arial", size=12)
        for mate in flatmates:
            pdf.cell(
                w=150, h=25, txt=f"{mate.name} is owe for {mate.days_in_house} days"
            )
            pdf.cell(w=150, h=25, txt=f"{round(mate.cost_for_flat, 2)}", ln=1)

        pdf.set_font(family="arial", style="b", size=14)
        pdf.cell(w=150, h=25, txt=f"Total bill:")
        pdf.cell(w=150, h=25, txt=f"{bill.amount}")
        pdf.output(name=f"{self.filename}")
        return self
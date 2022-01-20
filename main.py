import os
import webbrowser

from fpdf import FPDF


class Flatmate:
    def __init__(self, name, days_in_house):
        self.name = name
        self.days_in_house = days_in_house
        self.cost_for_flat = None

    @property
    def cost_for_flat(self):
        return self._cost_for_flat

    @cost_for_flat.setter
    def cost_for_flat(self, value):
        self._cost_for_flat = value


class Bill:

    def __init__(self, amount, period):
        self.amount = amount
        self.period = period

    def split_by_flatmates(self, *args) -> dict:
        bills = dict()
        delimiter = sum([mate.days_in_house for mate in args])
        for mate in args:
            bill = self.amount*(mate.days_in_house/delimiter)
            bills[mate.name] = bill
        return bills


class PdfReport:
    def __init__(self, filename):
        self.filename = filename

    def open(self, filename=None):
        URI = "file://" + os.path.realpath(filename or self.filename)
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
            pdf.cell(w=100, h=25, txt=f"{mate.name}")
            pdf.cell(w=150, h=25, txt=f"{round(mate.cost_for_flat, 2)}", ln=1)

        pdf.set_font(family="arial", style="b", size=14)
        pdf.cell(w=100, h=25, txt=f"Total bill:")
        pdf.cell(w=150, h=25, txt=f"{bill.amount}")
        pdf.output(name=f"{self.filename}")
        return self


def main():
    the_bill = Bill(amount=120, period="March 2020")

    adam = Flatmate(name="Adam", days_in_house=20)
    eva = Flatmate(name="Eva", days_in_house=25)
    charlie = Flatmate(name="Charlie", days_in_house=3)
    flatmates = (adam, eva, charlie)
    bills = the_bill.split_by_flatmates(*flatmates)

    for name, bill in bills.items():
        for mate in flatmates:
            if mate.name == name:
                mate.cost_for_flat = bill
                print(f"{mate.name} pays {mate.cost_for_flat}")

    report = PdfReport(filename="march.pdf")
    report.generate(bill=the_bill, flatmates=flatmates)
    report.open()


if __name__ == "__main__":
    main()

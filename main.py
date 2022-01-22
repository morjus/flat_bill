import os
import webbrowser

from fpdf import FPDF

from utils import input_handler


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
            bill = self.amount * (mate.days_in_house / delimiter)
            bills[mate.name] = bill
        return bills


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


def main():
    flatmates = []
    flatmates_qty = 2
    amount = input_handler(text="Enter the bill amount", return_type=int)
    period = input_handler(text="What is the bill period? E.g March 2020: ")
    the_bill = Bill(amount=amount, period=period)

    for mate_number in range(1, flatmates_qty + 1):
        name = input_handler(text=f"Enter the name of {mate_number} flatmate: ")
        days = input_handler(
            text=f"Enter the days in house of {name}: ", return_type=int
        )
        flatmates.append(Flatmate(name=name, days_in_house=days))

    bills = the_bill.split_by_flatmates(*flatmates)

    for name, bill in bills.items():
        for mate in flatmates:
            if mate.name == name:
                mate.cost_for_flat = bill
                print(f"{mate.name} pays {mate.cost_for_flat}")

    report = PdfReport(filename=f"{the_bill.period}.pdf")
    report.generate(bill=the_bill, flatmates=flatmates)
    report.open()


if __name__ == "__main__":
    main()

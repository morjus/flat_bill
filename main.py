from classes.bill import Bill
from classes.flatmate import Flatmate
from classes.report import PdfReport
from utils.utils import input_handler


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

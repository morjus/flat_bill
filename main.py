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

    def generate(self, bill, flatmates):
        pass


def main():
    bill = Bill(amount=120, period="March 2020")

    adam = Flatmate(name="Adam", days_in_house=20)
    eva = Flatmate(name="Eva", days_in_house=25)
    charlie = Flatmate(name="Charlie", days_in_house=0)
    flatmates = (adam, eva, charlie)
    bills = bill.split_by_flatmates(*flatmates)

    for name, bill in bills.items():
        for mate in flatmates:
            if mate.name == name:
                mate.cost_for_flat = bill
                print(f"{mate.name} pays {mate.cost_for_flat}")


if __name__ == "__main__":
    main()

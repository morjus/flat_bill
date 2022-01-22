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
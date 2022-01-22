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
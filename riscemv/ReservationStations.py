
class ReservationStation:
    def __init__(self, name):
        self.name = name
        self.clear()


    def clear(self):
        self.busy = False
        self.operation_number = None
        self.Vj = self.Vk = self.Qj = self.Qk = None


class ReservationStations:
    def __init__(self, adders_number, multipliers_number, dividers_number):
        self.adders_number = adders_number
        self.multipliers_number = multipliers_number
        self.dividers_number = dividers_number

        self.adders = []
        for i in range(self.adders_number):
            self.adders.append(ReservationStation("ADD" + str(i)))

        self.multipliers = []
        for i in range(self.multipliers_number):
            self.multipliers.append(ReservationStation("MULT" + str(i)))

        self.dividers = []
        for i in range(self.dividers_number):
            self.dividers.append(ReservationStation("DIV" + str(i)))

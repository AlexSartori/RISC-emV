
class ReservationStation:
    def __init__(self, name):
        self.name = name
        self.clear()


    def clear(self):
        self.time_remaining = None
        self.busy = False
        self.instruction = None
        self.result = None
        self.Vj = self.Vk = self.Qj = self.Qk = self.A = None


class ReservationStations:
    def __init__(self, adders_number, multipliers_number, dividers_number, loaders_number):
        self.set_adders_number(adders_number)
        self.set_multipliers_number(multipliers_number)
        self.set_dividers_number(dividers_number)
        self.set_loaders_number(loaders_number)


    def __iter__(self):
        return iter(
            self.adders
            + self.multipliers
            + self.dividers
            + self.loaders
        )


    def __len__(self):
        return (
            len(self.adders)
            + len(self.multipliers)
            + len(self.dividers)
            + len(self.loaders)
        )


    def get_function_units(self, functional_unit):
        functional_unit = functional_unit.lower()

        if functional_unit == 'add':
            fu_type = self.adders
        elif functional_unit == 'mult':
            fu_type = self.multipliers
        elif functional_unit == 'div':
            fu_type = self.dividers
        elif functional_unit == 'ld':
            fu_type = self.loaders
        else:
            raise NotImplementedError("Unknown functional unit: " + functional_unit)

        return fu_type


    def get_first_free(self, functional_unit):
        fu_type = self.get_function_units(functional_unit)

        for fu in fu_type:
            if not fu.busy:
                fu.busy = True
                return fu

        return None  # All busy


    def all_empty(self):
        for fu in self:
            if fu.busy:
                return False
        return True


    def set_adders_number(self, n):
        self.adders_number = n

        self.adders = []
        for i in range(self.adders_number):
            self.adders.append(ReservationStation("ADD" + str(i)))


    def set_multipliers_number(self, n):
        self.multipliers_number = n

        self.multipliers = []
        for i in range(self.multipliers_number):
            self.multipliers.append(ReservationStation("MULT" + str(i)))


    def set_dividers_number(self, n):
        self.dividers_number = n

        self.dividers = []
        for i in range(self.dividers_number):
            self.dividers.append(ReservationStation("DIV" + str(i)))


    def set_loaders_number(self, n):
        self.loaders_number = n

        self.loaders = []
        for i in range(self.loaders_number):
            self.loaders.append(ReservationStation("LD" + str(i)))

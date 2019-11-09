
class ReservationStation:
    def __init__(self, name):
        self.name = name
        self.clear()


    def clear(self):
        self.busy = False
        self.instruction = None
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

    
    def get_function_units(self, functional_unit):
        if functional_unit == 'add':
            fu_type = self.adders
        elif functional_unit == 'mult':
            fu_type = self.multipliers
        elif functional_unit == 'div':
            fu_type = self.dividers
        else:
            raise NotImplementedError("Invalid functional unit")

        return fu_type


    def get_first_free(self, functional_unit):
        fu_type = self.get_function_units(functional_unit)

        for fu in fu_type:
            if not fu.busy:
                fu.busy = True
                return fu


    def check_if_busy(self, functional_unit):
        fu_type = self.get_function_units(functional_unit)

        for fu in fu_type:
            if not fu.busy:
                return False
        return True

    
    def write_result(self, fu_name, result):
        fus = [self.adders, self.multipliers, self.dividers]
        for fu_coll in fus:
            for fu in fu_coll:
                if fu.Qj == fu_name:
                    fu.Vj = result
                    fu.Qj = 0
                elif fu.Qk == fu_name:
                    fu.Vk = result
                    fu.Qk = 0

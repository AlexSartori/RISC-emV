
class ReservationStation:
    def __init__(self, name):
        self.name = name
        self.clear()


    def clear(self):
        self.time_remaining = None
        self.busy = False
        self.instruction = None
        self.result = None
        self.thread_id = None
        self.Vj = self.Vk = self.Qj = self.Qk = self.A = None


class ReservationStations:
    RS_singleton = None

    def __init__(self, adders_number, multipliers_number, dividers_number, loaders_number, fp_adders_number, fp_multipliers_number, fp_dividers_number, fp_loaders_number):
        if ReservationStations.RS_singleton is None:
            self.set_adders_number(adders_number)
            self.set_multipliers_number(multipliers_number)
            self.set_dividers_number(dividers_number)
            self.set_loaders_number(loaders_number)
            self.set_fp_adders_number(fp_adders_number)
            self.set_fp_multipliers_number(fp_multipliers_number)
            self.set_fp_dividers_number(fp_dividers_number)
            self.set_fp_loaders_number(fp_loaders_number)

            ReservationStations.RS_singleton = {
                'add': self.adders,
                'mul': self.multipliers,
                'div': self.dividers,
                'ld': self.loaders,
                'fadd': self.fp_adders,
                'fmul': self.fp_multipliers,
                'fdiv': self.fp_dividers,
                'fld': self.fp_loaders
            }
        else:
            self.adders = ReservationStations.RS_singleton['add']
            self.multipliers = ReservationStations.RS_singleton['mul']
            self.dividers = ReservationStations.RS_singleton['div']
            self.loaders = ReservationStations.RS_singleton['ld']
            self.fp_adders = ReservationStations.RS_singleton['fadd']
            self.fp_multipliers = ReservationStations.RS_singleton['fmul']
            self.fp_dividers = ReservationStations.RS_singleton['fdiv']
            self.fp_loaders = ReservationStations.RS_singleton['fld']


    def __iter__(self):
        return iter(
            self.adders
            + self.multipliers
            + self.dividers
            + self.loaders
            + self.fp_adders
            + self.fp_multipliers
            + self.fp_dividers
            + self.fp_loaders
        )


    def __len__(self):
        return (
            len(self.adders)
            + len(self.multipliers)
            + len(self.dividers)
            + len(self.loaders)
            + len(self.fp_adders)
            + len(self.fp_multipliers)
            + len(self.fp_dividers)
            + len(self.fp_loaders)
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
        elif functional_unit == 'fadd':
            fu_type = self.fp_adders
        elif functional_unit == 'fmult':
            fu_type = self.fp_multipliers
        elif functional_unit == 'fdiv':
            fu_type = self.fp_dividers
        elif functional_unit == 'fld':
            fu_type = self.fp_loaders
        else:
            raise NotImplementedError("Unknown functional unit: " + functional_unit)

        return fu_type


    def get_first_free(self, functional_unit, thread_id):
        fu_type = self.get_function_units(functional_unit)

        for fu in fu_type:
            if not fu.busy:
                fu.busy = True
                fu.thread_id = thread_id
                return fu

        return None  # All busy

    
    def get_fus_of_thread(self, thread_id):
        return list(filter(lambda fu: fu.thread_id == thread_id, self))


    def all_empty(self):
        for fu in self:
            if fu.busy:
                return False
        return True


    def set_adders_number(self, n):
        self.adders = []
        for i in range(n):
            self.adders.append(ReservationStation("ADD" + str(i)))


    def set_multipliers_number(self, n):
        self.multipliers = []
        for i in range(n):
            self.multipliers.append(ReservationStation("MULT" + str(i)))


    def set_dividers_number(self, n):
        self.dividers = []
        for i in range(n):
            self.dividers.append(ReservationStation("DIV" + str(i)))


    def set_loaders_number(self, n):
        self.loaders = []
        for i in range(n):
            self.loaders.append(ReservationStation("LD" + str(i)))


    def set_fp_adders_number(self, n):
        self.fp_adders = []
        for i in range(n):
            self.fp_adders.append(ReservationStation("FADD" + str(i)))


    def set_fp_multipliers_number(self, n):
        self.fp_multipliers = []
        for i in range(n):
            self.fp_multipliers.append(ReservationStation("FMULT" + str(i)))


    def set_fp_dividers_number(self, n):
        self.fp_dividers = []
        for i in range(n):
            self.fp_dividers.append(ReservationStation("FDIV" + str(i)))


    def set_fp_loaders_number(self, n):
        self.fp_loaders = []
        for i in range(n):
            self.fp_loaders.append(ReservationStation("FLD" + str(i)))

from riscemv.ReservationStations import ReservationStations
from riscemv.RegisterFile import RegisterFile
from riscemv.RegisterStatus import RegisterStatus

class Tomasulo:
    def __init__(self, adders_number, multipliers_number, dividers_number):
        self.__steps = 0

        self.RS = ReservationStations(adders_number, multipliers_number, dividers_number)
        self.Regs = RegisterFile()
        self.RegisterStat = RegisterStatus()


    def step(self):
        self.__steps += 1

        self.write()
        self.execute()
        self.issue()


    def issue(self):
        raise NotImplementedError()
    

    def execute(self):
        raise NotImplementedError()

    
    def write(self):
        raise NotImplementedError()


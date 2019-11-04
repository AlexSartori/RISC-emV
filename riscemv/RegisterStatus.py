
class RegisterStatus:
    def __init__(self):
        self.__reg_status = {}

    
    def add_status(self, register, operation):
        self.__reg_status[register] = operation

    
    def remove_status(self, register):
        del self.__reg_status[register]
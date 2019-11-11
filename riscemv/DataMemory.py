
class DataMemory:
    def __init__(self):
        self.__memory = {}

    #TODO: add checks on address
    def store(self, address, value):
        self.__memory[address] = value


    def load(self, address):
        return self.__memory[address]

import abc # = abstract class


class Instruction(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def parse(binary_code):
        pass


    program_counter = None

    execution_code = None # will be modified on loading
    functional_unit = None
    clock_needed = None


    def __str__(self):
        if self.string is not None:
            return self.string
        else:
            return self.execution_code

    
    @staticmethod
    def imm_bin_to_int(value):
        bits = len(value)
        dec = int(value, 2)

        if int(value[0]) == 1:
            dec = -1 * (2**bits - dec)
        return dec


    @abc.abstractmethod
    def to_binary(self):
        pass


    @abc.abstractmethod
    def execute(self):
        pass

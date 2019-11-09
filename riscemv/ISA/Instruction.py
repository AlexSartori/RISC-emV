import abc # = abstract class


class Instruction(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def parse(binary_code):
        pass


    execution_code = None # will be modified on loading
    functional_unit = None
    clock_needed = None


    # @abc.abstractmethod
    # def to_binary(self):
    #     pass

    @abc.abstractmethod
    def execute(self):
        pass

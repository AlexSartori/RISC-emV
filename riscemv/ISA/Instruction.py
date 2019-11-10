import abc # = abstract class


class Instruction(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def parse(binary_code):
        pass


    execution_code = None # will be modified on loading
    functional_unit = None
    clock_needed = None


    def __str__(self):
        if self.string is not None:
            return self.string
        else:
            return self.execution_code

    # @abc.abstractmethod
    # def to_binary(self):
    #     pass

    @abc.abstractmethod
    def execute(self):
        pass

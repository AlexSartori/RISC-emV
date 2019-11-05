import abc


class Instruction(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def parse(binary_code):
        pass


    @abc.abstractmethod
    def execute(self):
        pass

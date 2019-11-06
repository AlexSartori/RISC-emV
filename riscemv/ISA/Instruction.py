import abc # = abstract class


class Instruction(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def parse(binary_code):
        pass


    # @abc.abstractmethod
    # def to_binary(self):
    #     pass

    @abc.abstractmethod
    def execute(self):
        pass

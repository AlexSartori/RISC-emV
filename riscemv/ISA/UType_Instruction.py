import os, json
from riscemv.ISA.Instruction import Instruction


class UType_Instruction(Instruction):
    rd_type = "int"


    def __init__(self, opcode, rd, imm):
        self.opcode = opcode
        self.imm = imm
        self.rd = rd


    def to_binary(self):
        if type(self.imm) == str:
            imm_bin = '0' * 20
        else:
            imm_bin = "{:020b}".format(self.imm)
        return "{0}$rd{1}".format(
            imm_bin, self.opcode
        ).replace("$rd", "{:05b}".format(self.rd))


    @staticmethod
    def parse(binary_code):
        imm = Instruction.imm_bin_to_int(binary_code[:20])
        rd = int(binary_code[20:25], 2)
        opcode = binary_code[25:32]
        return UType_Instruction(opcode, rd, imm)


    def execute(self, PC_value):
        code = self.execution_code
        code = code.replace('PC', str(PC_value))

        return eval(code)


    def __str__(self):
        return '{} {}, {}'.format(self.instr_name, self.__map_reg_name__(self.rd, self.rd_type), self.imm)

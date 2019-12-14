import os, json
from riscemv.ISA.Instruction import Instruction


class IType_Instruction(Instruction):
    rd_type = "int"
    rs_type = "int"


    def __init__(self, opcode, rd, funct3, rs, imm):
        self.opcode = opcode
        self.rd = rd
        self.funct3 = funct3
        self.rs = rs
        self.imm = imm


    def to_binary(self):
        imm_bin = "{:05b}".format(self.imm)
        return "{0}$rs{1}$rd{2}".format(
            imm_bin, self.funct3, self.opcode
        ).replace("$rs", "{:05b}".format(self.rs)
        ).replace("$rd", "{:05b}".format(self.rd))


    @staticmethod
    def parse(binary_code):
        imm = Instruction.imm_bin_to_int(binary_code[:12])
        rs = int(binary_code[12:17], 2)
        funct3 = binary_code[17:20]
        rd = int(binary_code[20:25], 2)
        opcode = binary_code[25:32]
        return IType_Instruction(opcode, rd, funct3, rs, imm)


    def execute(self, rs_value):
        code = self.execution_code
        code = code.replace('rs', str(rs_value))

        return eval(code)


    def is_load(self):
        return self.opcode in ["0000011", "0000111"]

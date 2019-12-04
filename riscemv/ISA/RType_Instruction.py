import os, json
from riscemv.ISA.Instruction import Instruction


class RType_Instruction(Instruction):
    rd_type = "int"
    rs1_type = "int"
    rs2_type = "int"


    def __init__(self, opcode, rd, funct3, rs1, rs2, funct7):
        self.opcode = opcode
        self.rd = rd
        self.funct3 = funct3
        self.rs1 = rs1
        self.rs2 = rs2
        self.funct7 = funct7


    def to_binary(self):
        return "{0}$rs2$rs1{1}$rd{2}".format(
            self.funct7, self.funct3, self.opcode
        ).replace("$rs2", "{:05b}".format(self.rs2)
        ).replace("$rs1", "{:05b}".format(self.rs1)
        ).replace("$rd", "{:05b}".format(self.rd))


    @staticmethod
    def parse(binary_code):
        funct7 = binary_code[:7]
        rs2 = int(binary_code[7:12], 2)
        rs1 = int(binary_code[12:17], 2)
        funct3 = binary_code[17:20]
        rd = int(binary_code[20:25], 2)
        opcode = binary_code[25:32]
        return RType_Instruction(opcode, rd, funct3, rs1, rs2, funct7)


    def execute(self, rs1_value, rs2_value):
        code = self.execution_code
        code = code.replace('rs', str(rs1_value))
        code = code.replace('rt', str(rs2_value))

        return eval(code)

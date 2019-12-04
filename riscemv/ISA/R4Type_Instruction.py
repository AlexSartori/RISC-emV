import os, json
from riscemv.ISA.Instruction import Instruction


class R4Type_Instruction(Instruction):
    rd_type = "int"
    rs1_type = "int"
    rs2_type = "int"
    rs3_type = "int"


    def __init__(self, opcode, rd, funct3, rs1, rs2, rs3, fmt):
        self.opcode = opcode
        self.rd = rd
        self.funct3 = funct3
        self.rs1 = rs1
        self.rs2 = rs2
        self.rs3 = rs3
        self.fmt = fmt


    def to_binary(self):
        return "$rs3{0}$rs2$rs1{1}$rd{2}".format(
            self.fmt, self.funct3, self.opcode
        ).replace("$rs3", "{:05b}".format(self.rs3)
        ).replace("$rs2", "{:05b}".format(self.rs2)
        ).replace("$rs1", "{:05b}".format(self.rs1)
        ).replace("$rd", "{:05b}".format(self.rd))


    @staticmethod
    def parse(binary_code):
        rs3 = int(binary_code[:5], 2)
        fmt = binary_code[5:7]
        rs2 = int(binary_code[7:12], 2)
        rs1 = int(binary_code[12:17], 2)
        funct3 = binary_code[17:20]
        rd = int(binary_code[20:25], 2)
        opcode = binary_code[25:32]
        return R4Type_Instruction(opcode, rd, funct3, rs1, rs2, rs3, fmt)


    def execute(self, rs1_value, rs2_value, rs3_value):
        code = self.execution_code
        code = code.replace('rs1', str(rs1_value))
        code = code.replace('rs2', str(rs2_value))
        code = code.replace('rs3', str(rs3_value))

        return eval(code)

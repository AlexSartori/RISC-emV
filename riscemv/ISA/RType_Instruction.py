import os, json
from riscemv.ISA.Instruction import Instruction


class RType_Instruction(Instruction):
    def __init__(self, opcode, rd, funct3, rs1, rs2, funct7):
        self.opcode = opcode
        self.rd = rd
        self.funct3 = funct3
        self.rs1 = rs1
        self.rs2 = rs2
        self.funct7 = funct7


    # def to_binary(self):
    #     return "{0}$rs2$rs1{1}$rd{2}".format(
    #         self.funct7, self.funct3, self.opcode
    #     )


    @staticmethod
    def parse(binary_code):
        funct7 = binary_code[:7]
        rs2 = binary_code[7:12]
        rs1 = binary_code[12:17]
        funct3 = binary_code[17:20]
        rd = binary_code[20:25]
        opcode = binary_code[25:32]
        return RType_Instruction(opcode, rd, funct3, rs1, rs2, funct7)


    def execute(self, rs1_value, rs2_value):
        code = self.execution_code
        code = code.replace('rs', '0b'+str(rs1_value))
        code = code.replace('rt', '0b'+str(rs2_value))

        fn = lambda: eval(code)
        return fn()

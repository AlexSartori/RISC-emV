import os, json
from riscemv.ISA.Instruction import Instruction


class BType_Instruction(Instruction):
    def __init__(self, opcode, imm, funct3, rs1, rs2):
        self.opcode = opcode
        self.imm = imm
        self.funct3 = funct3
        self.rs1 = rs1
        self.rs2 = rs2


    @staticmethod
    def parse(binary_code):
        imm12 = binary_code[0]
        imm10 = binary_code[1:7]
        rs2 = int(binary_code[7:12], 2)
        rs1 = int(binary_code[12:17], 2)
        funct3 = binary_code[17:20]
        imm4 = binary_code[20:24]
        imm11 = binary_code[24]
        opcode = binary_code[25:32]
        imm_bin = imm12 + imm11 + imm10 + imm4 + "0"
        imm = int(imm_bin, 2)
        return BType_Instruction(opcode, imm, funct3, rs1, rs2)


    def execute(self, rs1_value, rs2_value):
        code = self.execution_code
        code = code.replace('rs', str(rs1_value))
        code = code.replace('rt', str(rs2_value))

        return self.imm if eval(code) else 4

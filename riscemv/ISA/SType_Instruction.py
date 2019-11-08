import os, json
from riscemv.ISA.Instruction import Instruction


class SType_Instruction(Instruction):
    def __init__(self, opcode, imm, funct3, rs1, rs2):
        self.opcode = opcode
        self.imm = imm
        self.funct3 = funct3
        self.rs1 = rs1
        self.rs2 = rs2


    @staticmethod
    def parse(binary_code):
        imm11 = binary_code[:7]
        rs2 = binary_code[7:12]
        rs1 = binary_code[12:17]
        funct3 = binary_code[17:20]
        imm4 = binary_code[20:25]
        opcode = binary_code[25:32]
        imm = imm11 + imm4
        return SType_Instruction(opcode, imm, funct3, rs1, rs2)


    def execute(self):
        raise NotImplementedError()

import os, json
from riscemv.ISA.Instruction import Instruction


class IType_Instruction(Instruction):
    def __init__(self, opcode, rd, funct3, rs, imm):
        self.opcode = opcode
        self.rd = rd
        self.funct3 = funct3
        self.rs = rs
        self.imm = imm


    @staticmethod
    def parse(binary_code):
        imm = binary_code[:12]
        rs = binary_code[12:17]
        funct3 = binary_code[17:20]
        rd = binary_code[20:25]
        opcode = binary_code[25:32]
        return IType_Instruction(opcode, rd, funct3, rs, imm)


    def execute(self):
        raise NotImplementedError("The ISA configuration did not override this function")


    def is_load(self):
        return self.opcode == "0000011"

import os, json
from riscemv.ISA.Instruction import Instruction


class BType_Instruction(Instruction):
    rs1_type = "int"
    rs2_type = "int"


    def __init__(self, opcode, imm, funct3, rs1, rs2):
        self.opcode = opcode
        self.imm = imm
        self.funct3 = funct3
        self.rs1 = rs1
        self.rs2 = rs2


    def to_binary(self):
        imm_bin = "{:013b}".format(self.imm)
        imm12 = imm_bin[0]
        imm10 = imm_bin[2:8]
        imm4 = imm_bin[8:12]
        imm11 = imm_bin[1]
        return "{0}{1}$rs2$rs1{2}{3}{4}{5}".format(
            imm12, imm10, self.funct3, imm4, imm11, self.opcode
        ).replace("$rs1", "{:05b}".format(self.rs1)
        ).replace("$rs2", "{:05b}".format(self.rs2))


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

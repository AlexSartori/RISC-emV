import os, json
from riscemv.ISA.Instruction import Instruction


class SType_Instruction(Instruction):
    rs1_type = "int"
    rs2_type = "int"


    def __init__(self, opcode, imm, funct3, rs1, rs2):
        self.opcode = opcode
        self.imm = imm
        self.funct3 = funct3
        self.rs1 = rs1
        self.rs2 = rs2


    def to_binary(self):
        imm_bin = "{:012b}".format(self.imm)
        imm11 = imm_bin[:7]
        imm4 = imm_bin[7:]
        return "{0}$rs2$rs1{1}{2}{3}".format(
            imm11, self.funct3, imm4, self.opcode
        ).replace("$rs1", "{:05b}".format(self.rs1)
        ).replace("$rs2", "{:05b}".format(self.rs2))


    @staticmethod
    def parse(binary_code):
        imm11 = binary_code[:7]
        rs2 = int(binary_code[7:12], 2)
        rs1 = int(binary_code[12:17], 2)
        funct3 = binary_code[17:20]
        imm4 = binary_code[20:25]
        opcode = binary_code[25:32]
        imm = Instruction.imm_bin_to_int(imm11 + imm4)
        return SType_Instruction(opcode, imm, funct3, rs1, rs2)


    def execute(self, rs_value):
        code = self.execution_code
        code = code.replace('rs', str(rs_value))

        return eval(code)


    def __str__(self):
        return '{} {}, {}({})'.format(self.instr_name, self.__map_reg_name__(self.rs1, self.rs1_type),
                self.imm, self.__map_reg_name__(self.rs2, self.rs2_type))

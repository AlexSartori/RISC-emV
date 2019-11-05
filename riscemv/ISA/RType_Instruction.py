import os, json
from riscemv.instructions.Instruction import Instruction
from riscemv.ProgramLoader import ProgramLoader


class RType_Instruction(Instruction):
    def __init__(self, opcode, rd, funct3, rs1, rs2, funct7):
        self.opcode = opcode
        self.rd = rd
        self.funct3 = funct3
        self.rs1 = rs1
        self.rs2 = rs2
        self.funct7 = funct7

        binary_instr = "{0}$rs2$rs1{1}$rd{2}".format(funct7, funct3, opcode)
        #TODO: change to have dynamic XLEN
        pl = ProgramLoader(32)
        self.instruction_name = pl.binary_to_instr_name(binary_instr, "r-type")


    @staticmethod
    def parse(binary_code):
        funct7 = binary_code[:7]
        rs2 = binary_code[7:12]
        rs1 = binary_code[12:17]
        funct3 = binary_code[17:20]
        rd = binary_code[20:25]
        opcode = binary_code[25:32]
        return RInstruction(opcode, rd, funct3, rs1, rs2, funct7)


    def execute(self):
        return self.instruction_execution[self.instruction_name](self.rs1, self.rs2)


    instruction_execution = {
        "add": lambda rs1, rs2:
            "{:05b}".format(int(rs1, 2) + int(rs2, 2)),
        "sub": lambda rs1, rs2:
            "{:05b}".format(int(rs1, 2) - int(rs2, 2)),
        "xor": lambda rs1, rs2:
            "{:05b}".format(int(rs1, 2) ^ int(rs2, 2)),
        "or": lambda rs1, rs2:
            "{:05b}".format(int(rs1, 2) | int(rs2, 2)),
        "and": lambda rs1, rs2:
            "{:05b}".format(int(rs1, 2) & int(rs2, 2)),
        "sll": lambda rs1, rs2:
            "{:05b}".format(int(rs1, 2) << int(rs2, 2)),
        "srl": lambda rs1, rs2:
            "{:05b}".format(int(rs1, 2) >> int(rs2, 2)),
        "sra": lambda rs1, rs2:
            "{:05b}".format(int(rs1, 2) >> int(rs2, 2)),
        "slt": lambda rs1, rs2:
            "{:05b}".format(1 if (int(rs1, 2) < int(rs2, 2)) else 0),
        "sltu": lambda rs1, rs2:
            "{:05b}".format(1 if (int(rs1, 2) < int(rs2, 2)) else 0)
    }

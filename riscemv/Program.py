import json, os, re
from riscemv.ISA.ISA import ISA


class Program:
    def __init__(self):
        self.ISA = ISA()

        self.syntax_errors = []
        self.IM = [] # Instruction Memory


    def load_text(self, text):
        pc = 0
        for l_n, line in enumerate(text.split('\n')):
            line = line.split(';')[0]

            if line.strip() != '':
                try:
                    inst = self.ISA.instruction_from_str(line)
                    inst.program_counter = pc * 4
                    self.IM.append(inst)
                except:
                    self.syntax_errors.append((l_n, line))

                pc += 1


    def __iter__(self):
        return iter(self.IM)


    # def load_machine_code(self, filename):
    #     self.lines = []
    #
    #     i = 0
    #     with open(filename, 'rb') as f:
    #         binary_instruction = f.read(self.XLEN/8)
    #         bits_instruction = ("{:0" + str(self.XLEN) + "b}").format(binary_instruction)
    #         instr = self.ISA.instruction_from_bin(bits_instruction)
    #         instr.program_counter = i * 4
    #         self.lines.append((bits_instruction, instr))
    #         i += 1
    #
    #         # 6 types of instructions: R/I/S/SB/U/UJ
    #         #   - R-Format:  3 register inputs (add, xor, mul)
    #         #   - I-Format:  immediates or loads (addi, lw, jalr, ...)
    #         #   - S-Format:  store (sw, sb)
    #         #   - SB-Format: branch instructions (beq, bge)
    #         #   - U-Format:  upper immediates (?) (lui, auipc)
    #         #   - UJ-Format: jumps (jal)


    # def asm_to_binary(self, l):
    #     binary_instruction = ""
    #     line = l.lower().strip().split(' ')
    #
    #     if line[0] in self.ISA['r-type'].keys():
    #
    #         binary_instruction = self.rv32i['r-type'][line[0]]
    #         rd  = int(line[1][1:-1]) # Remove letter and comma
    #         rs1 = int(line[2][1:-1])
    #         rs2 = int(line[3][1:])
    #
    #         binary_instruction = binary_instruction.replace('$rd',  "{:05b}".format(rd)) # Remove comma
    #         binary_instruction = binary_instruction.replace('$rs1', "{:05b}".format(rs1)) # Remove comma
    #         binary_instruction = binary_instruction.replace('$rs2', "{:05b}".format(rs2))
    #         inst = RType_Instruction(tuple(line))
    #     else:
    #         raise SyntaxError("RISCemV: cannot process line \"" + l + "\"")
    #
    #     return binary_instruction

    #
    # def binary_to_instr_name(self, binary_instr, instr_type):
    #     for instr_name, instr_code in self.rv32i[instr_type].items():
    #         if binary_instr == instr_code:
    #             return instr_name
    #
    #     raise EnvironmentError("RISCemV: instruction not found! " + binary_instr)

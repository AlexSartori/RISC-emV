import re
from riscemv.ISA.ISA import ISA


class Program:
    def __init__(self, DM):
        self.DM = DM
        self.ISA = ISA()

        self.syntax_errors = []
        self.IM = []  # Instruction Memory
        self.sections = {'.text': 0}
        self.symbol_table = {}
        self.alignment = 4
        self.directives = {
            '.byte':  1,
            '.2byte': 2,
            '.4byte': 4,
            '.8byte': 8,
            '.half':  2,
            '.word':  4,
            '.dword': 8,
            # '.asciz': None,
            # '.string': None,
            # '.zero': None
        }


    def get_entry_point(self):
        if '_start' in self.symbol_table:
            return self.symbol_table['_start']
        else:
            return self.sections['.text']


    def load_text(self, text):
        pc = 0
        for l_n, line in enumerate(text.split('\n')):
            line = line.split(';')[0].strip()
            line = line.replace('\t', ' ')

            if line != '':
                if re.match('\.[a-zA-Z0-9]+', line):
                    # Directive
                    try:
                        pc = self.__parse_directive__(line, pc)
                    except SyntaxError as s:
                        self.syntax_errors.append((l_n, line, s))
                elif re.match('[a-zA-Z0-9]+:', line):
                    # Label
                    label = re.match('[a-zA-Z0-9]+:', line).group(0)
                    label = label[:-1]  # Remove colon
                    self.symbol_table[label] = pc
                else:
                    # Instruction
                    try:
                        inst = self.ISA.instruction_from_str(line, self.symbol_table, pc)
                        self.IM.append(inst)

                        # Load 32 bits into memory
                        for i in range(4):
                            self.DM.store(pc+i, int(inst.to_binary()[8*i:(8*i)+8], 2))
                    except NotImplementedError:
                        self.syntax_errors.append((l_n, line, "Instruction not yet implemented"))
                    except SyntaxError:
                        self.syntax_errors.append((l_n, line, "Unknown instruction"))

                    pc += 4


    def __parse_directive__(self, line, pc):
        line = line.split(' ')

        if line[0] in ['.text', '.data', '.rodata', '.bss']:
            self.sections[line[0]] = pc
        elif line[0] == '.align' or line[0] == '.p2align':
            self.alignment = 2**int(line[1])
        elif line[0] == '.balign':
            self.alignment = int(line[1])
        elif line[0] in self.directives:
            # TODO: store value byte per byte
            dir = self.directives[line[0]]
            val = line[1]

            for offset in range(self.alignment):
                self.DM.store(pc, val)
        elif line[0] == '.zero':
            addr = pc
            while addr < int(line[1]):
                self.DM.store(addr, 0)
                addr += 1
            pc += addr
        elif line[0] == '.string' or line[0] == '.asciz':
            s = line[1][1:-1]  # Remove quotes
            addr = pc

            for c in s:
                self.DM.store(addr, ord(c))
                addr += 1

            pc += addr
        else:
            raise SyntaxError("Unknown directive")

        return pc


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

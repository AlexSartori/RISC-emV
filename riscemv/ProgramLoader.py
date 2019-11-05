import json, os

class ProgramLoader:
    def __init__(self, XLEN):
        self.XLEN = XLEN
        self.lines = []

        # Load ISA // TODO: discover files automatically
        self.rv32i = json.load(open(os.path.join(os.path.dirname(__file__), "rv32i.json")))


    def load_machine_code(self, filename):
        self.lines = []

        with open(filename, 'rb') as f:
            binary_instruction = f.read(self.XLEN/8)
            bits_instruction = ("{:0" + str(self.XLEN) + "b}").format(binary_instruction)
            self.lines.append(bits_instruction)

            # 6 types of instructions: R/I/S/SB/U/UJ
            #   - R-Format:  3 register inputs (add, xor, mul)
            #   - I-Format:  immediates or loads (addi, lw, jalr, ...)
            #   - S-Format:  store (sw, sb)
            #   - SB-Format: branch instructions (beq, bge)
            #   - U-Format:  upper immediates (?) (lui, auipc)
            #   - UJ-Format: jumps (jal)


    def load_assembly_code(self, listing):
        self.lines = []

        for line in listing.split('\n'):
            if line.strip() == '':
                continue

            binary_instruction = self.asm_to_binary(line)
            self.lines.append(binary_instruction)
            print(binary_instruction)


    def asm_to_binary(self, l):
        binary_instruction = ""
        line = l.lower().strip().split(' ')
        print(line)

        if line[0] in self.rv32i['r-type']:
            binary_instruction = self.rv32i['r-type'][line[0]]
            rd  = int(line[1][1:-1]) # Remove letter and comma
            rs1 = int(line[2][1:-1])
            rs2 = int(line[3][1:])

            binary_instruction = binary_instruction.replace('$rd',  "{:05b}".format(rd)) # Remove comma
            binary_instruction = binary_instruction.replace('$rs1', "{:05b}".format(rs1)) # Remove comma
            binary_instruction = binary_instruction.replace('$rs2', "{:05b}".format(rs2))
        else:
            raise SyntaxError("RISCemV: cannot process line \"" + l + "\"")

        return binary_instruction


    def binary_to_instr_name(self, binary_instr, instr_type):
        for instr_name, instr_code in self.rv32i[instr_type].items():
            if binary_instr == instr_code:
                return instr_name
        
        raise EnvironmentError("RISCemV: instruction not found! " + binary_instr)

import os, json, re
from riscemv.ISA.RType_Instruction import RType_Instruction
from riscemv.ISA.IType_Instruction import IType_Instruction
from riscemv.ISA.SType_Instruction import SType_Instruction
from riscemv.ISA.BType_Instruction import BType_Instruction
from riscemv.ISA.UType_Instruction import UType_Instruction
from riscemv.ISA.UJType_Instruction import UJType_Instruction


class ISA:
    ISA_singleton = None

    def __init__(self):
        if ISA.ISA_singleton is None:
            self.ISA = {
                "r-type":  {},
                "i-type":  {},
                "s-type":  {},
                "b-type": {},
                "u-type":  {},
                "uj-type": {}
            }

            # Load ISA
            base_dir = os.path.join(os.path.dirname(__file__), "Extensions")
            for ext_file in os.listdir(base_dir):
                ext = json.load(open(os.path.join(base_dir, ext_file)))
                for type in ext.keys():
                    self.ISA[type].update(ext[type])

            ISA.ISA_singleton = self.ISA
        else:
            self.ISA = ISA.ISA_singleton


    def instruction_from_str(self, line, symbol_table, pc):
        line = [l.lower().strip() for l in line.split(' ')]
        inst = None

        if line[0] in self.ISA['r-type']:
            match = self.ISA['r-type'][line[0]]
            rd  = int(line[1][1:-1])  # Remove letter and comma
            rs1 = int(line[2][1:-1])
            rs2 = int(line[3][1:])

            inst = RType_Instruction(match["opcode"], rd, match['funct3'], rs1, rs2, match['funct7'])
            inst.string = ' '.join(line)
            inst.program_counter = pc
            inst.execution_code = match['exec']
            inst.functional_unit = match['funcUnit']
            inst.clock_needed = match['clockNeeded']
        elif line[0] in self.ISA['i-type']:
            match = self.ISA['i-type'][line[0]]
            rd = int(line[1][1:-1])  # Remove letter and comma

            if match['opcode'] == "0000011":  # Load instruction
                _rexp = re.search(r'([0-9]{1,2})\([x|fp]([0-9]{1,2})\)', line[2])
                imm = int(_rexp.group(1))
                rs  = int(_rexp.group(2))
            else:
                rs  = int(line[2][1:-1])
                imm = int(line[3])

            inst = IType_Instruction(match["opcode"], rd, match['funct3'], rs, imm)
            inst.string = ' '.join(line)
            inst.program_counter = pc
            inst.execution_code = match['exec'].replace('imm', str(imm))
            inst.functional_unit = match['funcUnit']
            inst.clock_needed = match['clockNeeded']

            if inst.is_load():
                inst.length = match['length']
        elif line[0] in self.ISA['s-type']:
            match = self.ISA['s-type'][line[0]]
            rs2 = int(line[1][1:-1])  # Remove letter and comma
            rs1_parts = line[2][:-1].split('(')
            rs1 = int(rs1_parts[1][1:])  # Remove letter
            imm = int(rs1_parts[0])

            inst = SType_Instruction(match["opcode"], imm, match['funct3'], rs1, rs2)
            inst.string = ' '.join(line)
            inst.program_counter = pc
            inst.execution_code = match['exec'].replace('imm', str(imm))
            inst.functional_unit = match['funcUnit']
            inst.clock_needed = match['clockNeeded']
            inst.length = match['length']
        elif line[0] in self.ISA['b-type']:
            match = self.ISA['b-type'][line[0]]
            rs2 = int(line[1][1:-1])  # Remove letter and comma
            rs1 = int(line[2][1:-1])  # Remove letter and comma

            if line[3].isdigit():
                imm = int(line[3])
            else:
                imm = symbol_table[line[3]] - pc

            inst = BType_Instruction(match["opcode"], imm, match['funct3'], rs1, rs2)
            inst.string = ' '.join(line)
            inst.program_counter = pc
            inst.execution_code = match['exec']
            inst.functional_unit = match['funcUnit']
            inst.clock_needed = match['clockNeeded']
        elif line[0] in self.ISA['u-type']:
            match = self.ISA['u-type'][line[0]]
            rd  = int(line[1][1:-1])
            imm = int(line[2])

            inst = UType_Instruction(match.opcode, rd, imm)
            inst.string = ' '.join(line)
            inst.program_counter = pc
            inst.execution_code = match['exec'].replace('imm', "{020b}".format(imm))
            inst.functional_unit = match['funcUnit']
            inst.clock_needed = match['clockNeeded']
        elif line[0] in self.ISA['uj-type']:
            match = self.ISA['uj-type'][line[0]]
            rd = int(line[1][1:-1])
            imm = int(line[2])

            inst = UJType_Instruction(match.opcode, rd, imm)
            inst.string = ' '.join(line)
            inst.program_counter = pc
            inst.execution_code = match['exec']
            inst.functional_unit = match['funcUnit']
            inst.clock_needed = match['clockNeeded']
        elif line[0] in ['nop', 'ecall']:
            raise NotImplementedError()
        else:
            raise SyntaxError()

        return inst


    def instruction_from_bin(self, binary_code, pc):
        opcode = binary_code[25:32]
        print("OPCODE:", opcode)

        for instr_type in self.ISA:
            for instr_code in self.ISA[instr_type]:
                instr_match = self.ISA[instr_type][instr_code]
                if instr_match["opcode"] == opcode:
                    if instr_type == "r-type":
                        inst = RType_Instruction.parse(binary_code)

                        if instr_match['funct7'] == inst.funct7 and instr_match['funct3'] == inst.funct3:
                            inst.execution_code = instr_match['exec']
                            inst.functional_unit = instr_match['funcUnit']
                            inst.clock_needed = instr_match['clockNeeded']
                            inst.program_counter = pc

                            return inst
                    elif instr_type == "i-type":
                        inst = IType_Instruction.parse(binary_code)

                        if instr_match['opcode'] == inst.opcode and instr_match['funct3'] == inst.funct3:
                            imm_bin = '{:032b}'.format(inst.imm)
                            if ('imm' in instr_match and imm_bin[:7] == instr_match['imm']) or 'imm' not in instr_match:
                                inst.execution_code = instr_match['exec'].replace('imm', '0b'+str(imm_bin))
                                inst.functional_unit = instr_match['funcUnit']
                                inst.clock_needed = instr_match['clockNeeded']
                                inst.program_counter = pc
                                if inst.is_load():
                                    inst.length = instr_match['length']

                            return inst
                    elif instr_type == "s-type":
                        inst = SType_Instruction.parse(binary_code)

                        if instr_match['funct3'] == inst.funct3:
                            inst.execution_code = instr_match['exec'].replace('imm', '0b'+str(inst.imm))
                            inst.functional_unit = instr_match['funcUnit']
                            inst.clock_needed = instr_match['clockNeeded']
                            inst.length = instr_match['length']
                            inst.program_counter = pc

                            return inst
                    elif instr_type == "b-type":
                        inst = BType_Instruction.parse(binary_code)

                        if instr_match['funct3'] == inst.funct3:
                            inst.execution_code = instr_match['exec']
                            inst.functional_unit = instr_match['funcUnit']
                            inst.clock_needed = instr_match['clockNeeded']
                            inst.program_counter = pc

                            return inst
                    elif instr_type == "u-type":
                        inst = UType_Instruction.parse(binary_code)

                        if instr_match['opcode'] == inst.opcode:
                            imm_bin = "{:020b}".format(inst.imm)
                            inst.execution_code = instr_match['exec'].replace('imm', '0b' + str(imm_bin))
                            inst.functional_unit = instr_match['funcUnit']
                            inst.clock_needed = instr_match['clockNeeded']
                            inst.program_counter = pc

                            return inst
                    elif instr_type == "uj-type":
                        inst = UJType_Instruction.parse(binary_code)

                        inst.execution_code = instr_match['exec']
                        inst.functional_unit = instr_match['funcUnit']
                        inst.clock_needed = instr_match['clockNeeded']
                        inst.program_counter = pc

                        return inst
                    else:
                        raise NotImplementedError()

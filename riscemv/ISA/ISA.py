import os, json, re
from riscemv.ISA.RType_Instruction import RType_Instruction
from riscemv.ISA.IType_Instruction import IType_Instruction
from riscemv.ISA.SType_Instruction import SType_Instruction
from riscemv.ISA.BType_Instruction import BType_Instruction
from riscemv.ISA.UType_Instruction import UType_Instruction
from riscemv.ISA.UJType_Instruction import UJType_Instruction
from riscemv.ISA.R4Type_Instruction import R4Type_Instruction
from riscemv.RegisterFile import RegisterFile


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
                "uj-type": {},
                "r4-type": {}
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


    def __map_register_name__(self, reg_name):
        rf = RegisterFile()
        for idx, reg in enumerate(rf.IntRegisters):
            if reg.symbolic_name == reg_name:
                return 'x' + str(idx)

        for idx, reg in enumerate(rf.FPRegisters):
            if reg.symbolic_name == reg_name:
                return 'f' + str(idx)
        return reg_name


    def __map_symbols__(self, imm, symbol_table):
        try:
            int(imm)
            return imm  # Not a symbol
        except ValueError:
            # Load from symbol table
            if re.match(r'%lo\((.+)\)', imm):
                label = re.match(r'%lo\((.+)\)', imm).group(1)
                sym = symbol_table[label]
                bins = ''.join(['{:08b}'.format(ord(char)) for char in sym['text']])
                return int(bins[:-12])
            elif re.match(r'%hi\((.+)\)', imm):
                label = re.match(r'%hi\((.+)\)', imm).group(1)
                sym = symbol_table[label]
                bins = ''.join(['{:08b}'.format(ord(char)) for char in sym['text']])
                return int(bins[:20])
            return None


    def instruction_from_str(self, line, symbol_table, pc):
        line = [l.lower().strip() for l in re.split(' |,', line)]
        line = list(filter(None, line))
        line = [self.__map_register_name__(reg_name) for reg_name in line]

        inst = None

        if line[0] in self.ISA['r-type']:
            match = self.ISA['r-type'][line[0]]
            rd  = int(line[1][1:])  # Remove letter
            rs1 = int(line[2][1:])
            rs2 = int(line[3][1:])

            funct3 = match['funct3'] if 'funct3' in match else '000'
            inst = RType_Instruction(match["opcode"], rd, funct3, rs1, rs2, match['funct7'])
            inst.instr_name = line[0]
            inst.program_counter = pc
            inst.execution_code = match['exec']
            inst.functional_unit = match['funcUnit']
            inst.clock_needed = match['clockNeeded']

            if 'rdType' in match:
                inst.rd_type = match['rdType']
            if 'rsType' in match:
                inst.rs1_type = match['rsType']
            if 'rtType' in match:
                inst.rs2_type = match['rtType']
        elif line[0] in self.ISA['i-type']:
            match = self.ISA['i-type'][line[0]]
            rd = int(line[1][1:])  # Remove letter

            if match['opcode'] in ["0000011", "0000111", "0100111"]:  # Load instructions and flw
                _rexp = re.search(r'(.+)\((.+)\)$', line[2])
                imm = _rexp.group(1)
                rs  = int(self.__map_register_name__(_rexp.group(2))[1:])
            else:
                rs  = int(self.__map_register_name__(line[2])[1:])
                imm = line[3]

            imm = int(self.__map_symbols__(imm, symbol_table))

            inst = IType_Instruction(match["opcode"], rd, match['funct3'], rs, imm)
            inst.instr_name = line[0]
            inst.program_counter = pc
            inst.execution_code = match['exec'].replace('imm', str(imm))
            inst.functional_unit = match['funcUnit']
            inst.clock_needed = match['clockNeeded']

            if 'rdType' in match:
                inst.rd_type = match['rdType']
            if 'rsType' in match:
                inst.rs_type = match['rsType']

            if inst.is_load():
                inst.length = match['length']
        elif line[0] in self.ISA['s-type']:
            match = self.ISA['s-type'][line[0]]
            rs2 = int(line[1][1:])  # Remove letter
            rs1_parts = line[2][:-1].split('(')

            rs1 = int(self.__map_register_name__(rs1_parts[1])[1:])  # Remove letter
            imm = int(self.__map_symbols__(rs1_parts[0], symbol_table))

            inst = SType_Instruction(match["opcode"], imm, match['funct3'], rs1, rs2)
            inst.instr_name = line[0]
            inst.program_counter = pc
            inst.execution_code = match['exec'].replace('imm', str(imm))
            inst.functional_unit = match['funcUnit']
            inst.clock_needed = match['clockNeeded']

            if 'rsType' in match:
                inst.rs1_type = match['rsType']
            if 'rtType' in match:
                inst.rs2_type = match['rtType']

            inst.length = match['length']
        elif line[0] in self.ISA['b-type']:
            match = self.ISA['b-type'][line[0]]
            rs2 = int(line[1][1:])  # Remove letter
            rs1 = int(line[2][1:])  # Remove letter

            if re.match(r'[-+]?\d+', line[3]):
                imm = int(line[3])
            else:
                imm = symbol_table[line[3]]['value'] - pc

            inst = BType_Instruction(match["opcode"], imm, match['funct3'], rs1, rs2)
            inst.instr_name = line[0]
            inst.program_counter = pc
            inst.execution_code = match['exec']
            inst.functional_unit = match['funcUnit']
            inst.clock_needed = match['clockNeeded']

            if 'rsType' in match:
                inst.rs1_type = match['rsType']
            if 'rtType' in match:
                inst.rs2_type = match['rtType']
        elif line[0] in self.ISA['u-type']:
            match = self.ISA['u-type'][line[0]]
            rd  = int(line[1][1:])
            imm = int(self.__map_symbols__(line[2], symbol_table))

            inst = UType_Instruction(match["opcode"], rd, imm)
            inst.instr_name = line[0]
            inst.program_counter = pc
            inst.execution_code = match['exec'].replace('imm', "{:020b}".format(imm))
            inst.functional_unit = match['funcUnit']
            inst.clock_needed = match['clockNeeded']

            if 'rdType' in match:
                inst.rd_type = match['rdType']
        elif line[0] in self.ISA['uj-type']:
            match = self.ISA['uj-type'][line[0]]
            rd = int(line[1][1:])
            imm = int(self.__map_symbols__(line[2], symbol_table))

            inst = UJType_Instruction(match["opcode"], rd, imm)
            inst.instr_name = line[0]
            inst.program_counter = pc
            inst.execution_code = match['exec']
            inst.functional_unit = match['funcUnit']
            inst.clock_needed = match['clockNeeded']

            if 'rdType' in match:
                inst.rd_type = match['rdType']
        elif line[0] in self.ISA['r4-type']:
            match = self.ISA['r4-type'][line[0]]
            rd  = int(line[1][1:])  # Remove letter
            rs1 = int(line[2][1:])
            rs2 = int(line[3][1:])
            rs3 = int(line[4][1:])

            fmt = match['fmt']
            inst = R4Type_Instruction(match["opcode"], rd, funct3, rs1, rs2, rs3, fmt)
            inst.instr_name = line[0]
            inst.program_counter = pc
            inst.execution_code = match['exec']
            inst.functional_unit = match['funcUnit']
            inst.clock_needed = match['clockNeeded']

            if 'rdType' in match:
                inst.rd_type = match['rdType']
            if 'rs1Type' in match:
                inst.rs1_type = match['rs1Type']
            if 'rs2Type' in match:
                inst.rs2_type = match['rs2Type']
            if 'rs3Type' in match:
                inst.rs3_type = match['rs3Type']
        elif line[0] in ['nop', 'ecall']:
            raise NotImplementedError()
        else:
            raise SyntaxError()

        return inst


    def instruction_from_bin(self, binary_code, pc):
        opcode = binary_code[25:32]

        for instr_type in self.ISA:
            for instr_code in self.ISA[instr_type]:
                instr_match = self.ISA[instr_type][instr_code]
                if instr_match["opcode"] == opcode:
                    if instr_type == "r-type":
                        inst = RType_Instruction.parse(binary_code)

                        if instr_match['funct7'] == inst.funct7:
                            if 'funct3' not in instr_match or instr_match['funct3'] == inst.funct3:
                                inst.execution_code = instr_match['exec']
                                inst.functional_unit = instr_match['funcUnit']
                                inst.clock_needed = instr_match['clockNeeded']
                                inst.program_counter = pc

                                if 'rdType' in instr_match:
                                    inst.rd_type = instr_match['rdType']
                                if 'rsType' in instr_match:
                                    inst.rs1_type = instr_match['rsType']
                                if 'rtType' in instr_match:
                                    inst.rs2_type = instr_match['rtType']


                                inst.instr_name = instr_code

                                return inst
                    elif instr_type == "i-type":
                        inst = IType_Instruction.parse(binary_code)

                        if instr_match['opcode'] == inst.opcode and instr_match['funct3'] == inst.funct3:
                            imm_bin = '{:032b}'.format(inst.imm)

                            if ('imm' in instr_match and imm_bin[:7] == instr_match['imm']) or 'imm' not in instr_match:
                                inst.execution_code = instr_match['exec'].replace('imm', str(inst.imm))
                                inst.functional_unit = instr_match['funcUnit']
                                inst.clock_needed = instr_match['clockNeeded']
                                inst.program_counter = pc

                                if 'rdType' in instr_match:
                                    inst.rd_type = instr_match['rdType']
                                if 'rsType' in instr_match:
                                    inst.rs_type = instr_match['rsType']

                                if inst.is_load():
                                    inst.length = instr_match['length']

                                inst.instr_name = instr_code

                                return inst
                    elif instr_type == "s-type":
                        inst = SType_Instruction.parse(binary_code)

                        if instr_match['funct3'] == inst.funct3:
                            inst.execution_code = instr_match['exec'].replace('imm', str(inst.imm))
                            inst.functional_unit = instr_match['funcUnit']
                            inst.clock_needed = instr_match['clockNeeded']
                            inst.length = instr_match['length']
                            inst.program_counter = pc

                            if 'rsType' in instr_match:
                                inst.rs1_type = instr_match['rsType']
                            if 'rtType' in instr_match:
                                inst.rs2_type = instr_match['rtType']

                            inst.instr_name = instr_code

                            return inst
                    elif instr_type == "b-type":
                        inst = BType_Instruction.parse(binary_code)

                        if instr_match['funct3'] == inst.funct3:
                            inst.execution_code = instr_match['exec']
                            inst.functional_unit = instr_match['funcUnit']
                            inst.clock_needed = instr_match['clockNeeded']
                            inst.program_counter = pc

                            if 'rsType' in instr_match:
                                inst.rs1_type = instr_match['rsType']
                            if 'rtType' in instr_match:
                                inst.rs2_type = instr_match['rtType']

                            inst.instr_name = instr_code

                            return inst
                    elif instr_type == "u-type":
                        inst = UType_Instruction.parse(binary_code)

                        if instr_match['opcode'] == inst.opcode:
                            imm_bin = "{:020b}".format(inst.imm)
                            inst.execution_code = instr_match['exec'].replace('imm', '0b' + str(imm_bin))
                            inst.functional_unit = instr_match['funcUnit']
                            inst.clock_needed = instr_match['clockNeeded']
                            inst.program_counter = pc

                            if 'rdType' in instr_match:
                                inst.rd_type = instr_match['rdType']

                            inst.instr_name = instr_code

                            return inst
                    elif instr_type == "uj-type":
                        inst = UJType_Instruction.parse(binary_code)

                        inst.execution_code = instr_match['exec']
                        inst.functional_unit = instr_match['funcUnit']
                        inst.clock_needed = instr_match['clockNeeded']
                        inst.program_counter = pc

                        if 'rdType' in instr_match:
                            inst.rd_type = instr_match['rdType']

                        inst.instr_name = instr_code

                        return inst
                    elif instr_type == "r4-type":
                        inst = R4Type_Instruction.parse(binary_code)

                        if instr_match['opcode'] == inst.opcode and instr_match['fmt'] == inst.fmt:
                            inst.execution_code = instr_match['exec']
                            inst.functional_unit = instr_match['funcUnit']
                            inst.clock_needed = instr_match['clockNeeded']
                            inst.program_counter = pc

                            if 'rdType' in instr_match:
                                inst.rd_type = instr_match['rdType']
                            if 'rs1Type' in instr_match:
                                inst.rs1_type = instr_match['rs1Type']
                            if 'rs2Type' in instr_match:
                                inst.rs2_type = instr_match['rs2Type']
                            if 'rs3Type' in instr_match:
                                inst.rs3_type = instr_match['rs3Type']

                            inst.instr_name = instr_code

                            return inst
                    else:
                        raise NotImplementedError()

        raise NotImplementedError("Unknown OPCODE")

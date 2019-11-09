import os, json
from riscemv.ISA.RType_Instruction import RType_Instruction
from riscemv.ISA.IType_Instruction import IType_Instruction
from riscemv.ISA.SType_Instruction import SType_Instruction


# TODO: make static so it loads instructions only once
class ISA:
    def __init__(self):
        self.ISA = {
            "r-type":  {},
            "i-type":  {},
            "s-type":  {},
            "sb-type": {},
            "u-type":  {},
            "uj-type": {}
        }

        # Load ISA
        base_dir = os.path.join(os.path.dirname(__file__), "Extensions")
        for ext_file in os.listdir(base_dir):
            ext = json.load(open(os.path.join(base_dir, ext_file)))
            for type in ext.keys():
                self.ISA[type].update(ext[type])


    def instruction_from_str(self, line):
        line = [l.lower().strip() for l in line.split(' ')]

        if line[0] in self.ISA['r-type']:
            match = self.ISA['r-type'][line[0]]
            rd  = int(line[1][1:-1]) # Remove letter and comma
            rs1 = int(line[2][1:-1])
            rs2 = int(line[3][1:])

            inst = RType_Instruction("?", rd, match['funct3'], rs1, rs2, match['funct7'])
            inst.execution_code = match['exec']
            inst.functional_unit = match['funcUnit']
            inst.clock_needed = match['clockNeeded']
            return inst
        elif line[0] in self.ISA['i-type']:
            match = self.ISA['i-type'][line[0]]
            rd  = int(line[1][1:-1]) # Remove letter and comma
            rs = int(line[2][1:-1])
            imm = int(line[3])

            inst = IType_Instruction(match["opcode"], rd, match['funct3'], rs, imm)
            inst.execution_code = match['exec'].replace('imm', str(imm))
            inst.functional_unit = match['funcUnit']
            inst.clock_needed = match['clockNeeded']
            return inst
        elif line[0] in self.ISA['s-type']:
            match = self.ISA['s-type'][line[0]]
            rs2  = int(line[1][1:-1]) # Remove letter and comma
            rs1_parts = line[2][1:-1].split('(')
            rs1 = int(rs1_parts[1])
            imm = int(rs1_parts[0])

            inst = SType_Instruction("0100011", imm, match['funct3'], rs1, rs2)
            inst.execution_code = match['exec'].replace('imm', str(imm))
            inst.functional_unit = match['funcUnit']
            inst.clock_needed = match['clockNeeded']
            return inst
        else:
            raise NotImplementedError()


    def instruction_from_bin(self, binary_code):
        opcode = binary_code[25:32]
        print("OPCODE:", opcode)

        if opcode == "0110011": # r-type
            inst = RType_Instruction.parse(binary_code)

            for i in self.ISA['r-type'].values():
                if i['funct7'] == inst.funct7 and i['funct3'] == inst.funct3:
                    inst.execution_code = i['exec']
                    inst.functional_unit = i['funcUnit']
                    inst.clock_needed = i['clockNeeded']

            return inst
        elif opcode in ["0010011", "0000011"]: # i-type
            inst = IType_Instruction.parse(binary_code)

            for i in self.ISA['i-type'].values():
                if i['opcode'] == inst.opcode and i['funct3'] == inst.funct3:
                    imm_bin = '{:032b}'.format(inst.imm)
                    if ('imm' in i and imm_bin[:7] == i['imm']) or 'imm' not in i:
                        inst.execution_code = i['exec'].replace('imm', '0b'+str(imm_bin))
                        inst.functional_unit = i['funcUnit']
                        inst.clock_needed = i['clockNeeded']

            return inst
        elif opcode == "0100011": # s-type
            inst = SType_Instruction.parse(binary_code)

            for i in self.ISA['s-type'].values():
                if i['funct3'] == inst.funct3:
                    inst.execution_code = i['exec'].replace('imm', '0b'+str(inst.imm))
                    inst.functional_unit = i['funcUnit']
                    inst.clock_needed = i['clockNeeded']

            return inst
        else:
            raise NotImplementedError("Only r-type, i-type and s-type")

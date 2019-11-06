import os, json
from riscemv.ISA.RType_Instruction import RType_Instruction
from riscemv.ISA.IType_Instruction import IType_Instruction


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
            inst.execute = lambda : eval(match['exec'].replace('rs', rs1).replace('rt', rs2))
            return inst
        elif line[0] in self.ISA['i-type']:
            match = self.ISA['i-type'][line[0]]
            rd  = int(line[1][1:-1]) # Remove letter and comma
            rs = int(line[2][1:-1])
            imm = int(line[3][1:])

            inst = IType_Instruction(match["opcode"], rd, match['funct3'], rs, imm)
            inst.execute = lambda : eval(match['exec'].replace('rs', rs).replace('imm', imm))
            return inst
        else:
            raise NotImplementedError()


    def instruction_from_bin(self, binary_code):
        opcode = binary_code[25:32]

        if opcode == "0110011": # r-type
            inst = RType_Instruction.parse(binary_code)

            for i in self.ISA['r-type'].values():
                if i['funct7'] == inst.funct7 and i['funct3'] == inst.funct3:
                    exec = i['exec'].replace('rs', '0b'+str(inst.rs1)).replace('rt', '0b'+str(inst.rs2))
                    inst.execute = lambda: eval(exec)

            return inst
        elif opcode in ["0010011", "0000011"]: # i-type
            inst = IType_Instruction.parse(binary_code)

            for i in self.ISA['i-type'].values():
                if i['opcode'] == inst.opcode and i['funct3'] == inst.funct3:
                    if 'imm' in i and inst.imm[:5] != i['imm']:
                        continue
                    exec = i['exec'].replace('rs', '0b'+str(inst.rs)).replace('imm', '0b'+str(inst.imm))
                    inst.execute = lambda: eval(exec)

            return inst
        else:
            raise NotImplementedError("Only r-type and i-type")

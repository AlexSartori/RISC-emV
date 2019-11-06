import os, json
from riscemv.ISA.RType_Instruction import RType_Instruction


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
        else:
            raise NotImplementedError()


    def instruction_from_bin(self, binary_code):
        opcode = binary_code[25:32]

        if opcode == "0110011": # r-type
            funct7 = binary_code[:7]
            rs2 = binary_code[7:12]
            rs1 = binary_code[12:17]
            funct3 = binary_code[17:20]
            rd = binary_code[20:25]

            inst = RType_Instruction(opcode, rd, funct3, rs1, rs2, funct7)

            for i in self.ISA['r-type'].values():
                if i['funct7'] == funct7 and i['funct3'] == funct3:
                    exec = i['exec'].replace('rs', '0b'+str(rs1)).replace('rt', '0b'+str(rs2))
                    inst.execute = lambda: eval(exec)

            return inst
        else:
            raise NotImplementedError("Only r-type")

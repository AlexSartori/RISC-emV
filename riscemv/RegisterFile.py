import json, os

class Register:
    def __init__(self, symbolic_name, value=None, read_only=False):
        self.symbolic_name = symbolic_name
        self.value = value
        self.read_only = read_only


    @staticmethod
    def parse(int_reg):
        value, read_only = None, False
        if 'value' in int_reg:
            value = int_reg['value']
            read_only = int_reg['read_only']

        return Register(int_reg['symbolic_name'], value, read_only)


    def get_value(self):
        return self.value


    def set_value(self, value):
        if self.read_only:
            raise PermissionError("RISCemV: cannot write to register: " + self.symbolic_name)

        self.value = value


class RegisterFile:
    def __init__(self):
        self.PC = Register('PC')
        self.IR = Register('IR')

        self.IntRegisters = []
        self.FPRegisters = []

        rf_config = json.load(open(os.path.join(os.path.dirname(__file__), "rf_config.json")))
        for int_reg in rf_config['IntRegisters']:
            self.IntRegisters.append(Register.parse(int_reg))

        for fp_reg in rf_config['FPRegisters']:
            self.FPRegisters.append(Register.parse(fp_reg))


    def readInt(self, reg_name):
        dec_name = int(reg_name, 2)
        return self.IntRegisters[dec_name].get_value()


    def writeInt(self, reg_name, value):
        dec_name = int(reg_name, 2)
        self.IntRegisters[dec_name].set_value(value)


    def readFP(self, reg_name):
        dec_name = int(reg_name, 2)
        return self.FPRegisters[dec_name].get_value()


    def writeFP(self, reg_name, value):
        dec_name = int(reg_name, 2)
        self.FPRegisters[dec_name].set_value(value)


    def __iter__(self):
        yield iter(self.IntRegisters)
        yield iter(self.FPRegisters)

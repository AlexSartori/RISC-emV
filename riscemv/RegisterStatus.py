
class RegisterStatus:
    def __init__(self):
        self.int_reg_status = [None] * 32
        self.fp_reg_status = [None] * 32


    def add_int_status(self, register, operation):
        self.int_reg_status[register] = operation


    def add_fp_status(self, register, operation):
        self.fp_reg_status[register] = operation


    def remove_int_status(self, register):
        # if 'register' not in '__reg_status' -> RD collision
        if self.int_reg_status is not None:
            self.int_reg_status[register] = None
        else:
            print("[RegStatus] ERROR: int RD collision")


    def remove_fp_status(self, register):
        # if 'register' not in '__reg_status' -> RD collision
        if self.fp_reg_status is not None:
            self.fp_reg_status[register] = None
        else:
            print("[RegStatus] ERROR: fp RD collision")


    def get_int_status(self, register):
        return self.int_reg_status[register]


    def get_fp_status(self, register):
        return self.fp_reg_status[register]


    def __iter__(self):
        return iter(self.int_reg_status + self.fp_reg_status)

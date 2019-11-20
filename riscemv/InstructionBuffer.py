
class IFQEntry:
    def __init__(self, inst, iss, ex, wr):
        self.instruction = inst
        self.issue = iss
        self.execute = ex
        self.write_result = wr


class InstructionBuffer():
    def __init__(self):
        self.code_lines = []


    def __pc_to_line_number__(self, pc):
        return int(pc / 4)


    def get(self, pc):
        line_number = self.__pc_to_line_number__(pc)
        return self.code_lines[line_number]


    def put(self, inst, iss=0, ex=0, wr=0):
        self.code_lines.append(IFQEntry(inst, iss, ex, wr))


    def set_instruction_issue(self, pc, steps):
        line_number = self.__pc_to_line_number__(pc)
        self.code_lines[line_number].issue = steps


    def set_instruction_execute(self, pc, steps):
        line_number = self.__pc_to_line_number__(pc)
        self.code_lines[line_number].execute = steps


    def set_instruction_write_result(self, pc, steps):
        line_number = self.__pc_to_line_number__(pc)
        self.code_lines[line_number].write_result = steps


    def empty(self, pc):
        line_number = self.__pc_to_line_number__(pc)
        return line_number == len(self.code_lines)


    def __iter__(self):
        return iter(self.code_lines)

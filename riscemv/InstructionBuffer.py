import queue


class IFQEntry:
    def __init__(self, inst, iss, ex, wr):
        self.instruction = inst
        self.issue = iss
        self.execute = ex
        self.write_result = wr


class InstructionBuffer(queue.Queue):
    def __init__(self):
        self.code_lines = []
        super(InstructionBuffer, self).__init__()


    def put(self, inst, iss=0, ex=0, wr=0):
        super(InstructionBuffer, self).put(IFQEntry(inst, iss, ex, wr))
        self.code_lines.append(IFQEntry(inst, iss, ex, wr))


    def set_instruction_issue(self, line_number, steps):
        self.code_lines[line_number].issue = steps


    def set_instruction_execute(self, line_number, steps):
        self.code_lines[line_number].execute = steps


    def set_instruction_write_result(self, line_number, steps):
        self.code_lines[line_number].write_result = steps


    def __iter__(self):
        return iter(self.code_lines)

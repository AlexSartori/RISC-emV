
class IFQEntry:
    def __init__(self, inst, iss, ex, wr):
        self.instruction = inst
        self.issue = iss
        self.execute = ex
        self.write_result = wr


class InstructionBuffer():
    def __init__(self):
        self.instructions = {}
        self.last_instruction = 0


    def get(self, pc):
        if pc in self.instructions:
            return self.instructions[pc]
        else:
            raise IndexError("No instruction at PC " + str(pc))


    def put(self, inst, iss=0, ex=0, wr=0):
        self.instructions[inst.program_counter] = IFQEntry(inst, iss, ex, wr)
        self.last_instruction = inst.program_counter


    def set_instruction_issue(self, pc, steps):
        self.instructions[pc].issue = steps


    def set_instruction_execute(self, pc, steps):
        self.instructions[pc].execute = steps


    def set_instruction_write_result(self, pc, steps):
        self.instructions[pc].write_result = steps


    def empty(self, pc):
        return pc == self.last_instruction

    def __iter__(self):
        return iter(self.instructions.values())


    def clear(self):
        self.instructions = {}

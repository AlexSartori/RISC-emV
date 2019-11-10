import queue


class IFQEntry:
    def __init__(self, inst, iss, ex, wr):
        self.instruction = inst
        self.issue = iss
        self.execute = ex
        self.write_result = wr


class InstructionBuffer(queue.Queue):
    def __init__(self):
        super(InstructionBuffer, self).__init__()


    def put(self, inst, iss=0, ex=0, wr=0):
        super(InstructionBuffer, self).put(IFQEntry(inst, iss, ex, wr))


    def __iter__(self):
        return iter(list(self.queue))

from riscemv.ReservationStations import ReservationStations
from riscemv.RegisterFile import RegisterFile
from riscemv.RegisterStatus import RegisterStatus
from riscemv.ProgramLoader import ProgramLoader
from riscemv.ISA.RType_Instruction import RType_Instruction
from riscemv.ISA.IType_Instruction import IType_Instruction
from riscemv.ISA.SType_Instruction import SType_Instruction
import queue

class Tomasulo:
    def __init__(self, code_text, XLEN, adders_number, multipliers_number, dividers_number):
        self.__steps = 0

        self.RS = ReservationStations(adders_number, multipliers_number, dividers_number)
        self.Regs = RegisterFile()
        self.RegisterStat = RegisterStatus()

        self.__load__(code_text, XLEN)

        self.issue_fu = self.exec_fu = self.exec_res = None

    
    def __load__(self, code_text, XLEN):
        self.IFQ = queue.Queue()

        pl = ProgramLoader(XLEN)
        pl.load_assembly_code(code_text)
        for instr_code, instr in pl.lines:
            self.IFQ.put(instr)
        

    def step(self):
        self.__steps += 1

        self.write(self.exec_fu, self.exec_res)
        self.exec_fu, self.exec_res = self.execute(self.issue_fu)
        self.issue_fu = self.issue()


    def issue(self):
        if self.IFQ.empty():
            return
        instruction = self.IFQ.get()
        is_load = isinstance(instruction, IType_Instruction) and instruction.is_load()
        is_store = isinstance(instruction, SType_Instruction)

        r = instruction.functional_unit
        
        if is_load or is_store:

            if is_load: # load
                raise NotImplementedError()
            else: # store
                raise NotImplementedError()                
        else:
            if not self.RS.check_if_busy(r):
                fu = self.RS.get_first_free(r)
                fu.instruction = instruction
                if isinstance(instruction, RType_Instruction):
                    if self.RegisterStat.get_status(instruction.rs1) != 0:
                        fu.Qj = self.RegisterStat.get_status(instruction.rs1)
                    else:
                        fu.Vj = self.Regs.readInt(instruction.rs1)
                        fu.Qj = 0
                    if self.RegisterStat.get_status(instruction.rs2) != 0:
                        fu.Qk = self.RegisterStat.get_status(instruction.rs2)
                    else:
                        fu.Vk = self.Regs.readInt(instruction.rs2)
                        fu.Qk = 0
                elif isinstance(instruction, IType_Instruction):
                    if self.RegisterStat.get_status(instruction.rs) != 0:
                        fu.Qj = self.RegisterStat.get_status(instruction.rs)
                    else:
                        fu.Vj = self.Regs.readInt(instruction.rs)
                        fu.Qj = 0
                    fu.Vk = instruction.imm # store the immediate value
                    fu.Qk = 0

                self.RegisterStat.add_status(instruction.rd, fu.name)
                return fu
        
        return None


    def execute(self, fu):
        if fu is not None:
            if fu.Qj == 0 and fu.Qk == 0:
                if isinstance(fu.instruction, RType_Instruction):
                    exec = fu.instruction.execute(fu.Vj, fu.Vk)
                elif isinstance(fu.instruction, IType_Instruction):
                    exec = fu.instruction.execute(fu.Vj)
                return fu, exec
        return None, None

    
    def write(self, fu, result):
        if fu is not None and result is not None:
            self.RegisterStat.remove_status(fu.instruction.rd)
            self.Regs.writeInt(fu.instruction.rd, result)

            self.RS.write_result(fu.name, result)

            fu.clear()

from riscemv.Tomasulo import Tomasulo
from riscemv.ProgramLoader import ProgramLoader
from riscemv.ISA.ISA import ISA


def test_tomasulo():
    xlen = 32
    n_adders = n_mult = n_div = n_ld = n_st = 1
    code_text = "addi x10, x9, 12"

    tomasulo = Tomasulo(xlen, n_adders, n_mult, n_div, n_ld, n_st)
    PL = ProgramLoader(xlen)
    PL.load_assembly_code(code_text)
    
    for l in PL.lines:
        tomasulo.IFQ.put(l[1])

    reg_addr = 9
    tomasulo.Regs.writeInt(reg_addr, 0)

    tomasulo.step()

    tomasulo.step()

    tomasulo.step()

    assert tomasulo.Regs.readInt(10) == 12

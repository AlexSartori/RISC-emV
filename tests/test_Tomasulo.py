from riscemv.Tomasulo import Tomasulo
from riscemv.ISA.ISA import ISA


def test_tomasulo():
    xlen = 32
    n_adders = n_mult = n_div = n_ld = n_st = 1
    code_text = "addi x10, x9, 12"

    tomasulo = Tomasulo(xlen, n_adders, n_mult, n_div, n_ld, n_st)
    tomasulo.IFQ.put(ISA().instruction_from_str(code_text))

    reg_addr = 9
    tomasulo.Regs.writeInt(reg_addr, 0)

    tomasulo.step()
    # assert tomasulo.issue_fu != None
    # assert tomasulo.exec_fu == tomasulo.exec_res == None

    tomasulo.step()
    # assert tomasulo.issue_fu == None
    # assert tomasulo.exec_fu != None
    # assert tomasulo.exec_res != None

    tomasulo.step()
    # assert tomasulo.issue_fu == None
    # assert tomasulo.exec_fu == tomasulo.exec_res == None

    assert tomasulo.Regs.readInt(10) == 12

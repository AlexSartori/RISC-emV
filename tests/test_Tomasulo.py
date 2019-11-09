from riscemv.Tomasulo import Tomasulo


def test_tomasulo():
    xlen = 32
    n_adders = n_mult = n_div = 1
    code_text = "addi x10, x9, 12"

    tomasulo = Tomasulo(code_text, xlen, n_adders, n_mult, n_div)
    reg_addr = 9
    tomasulo.Regs.writeInt(reg_addr, 0)

    tomasulo.step()
    assert tomasulo.issue_fu != None
    assert tomasulo.exec_fu == tomasulo.exec_res == None

    tomasulo.step()    
    assert tomasulo.issue_fu == None
    assert tomasulo.exec_fu != None
    assert tomasulo.exec_res != None

    tomasulo.step()
    assert tomasulo.issue_fu == None
    assert tomasulo.exec_fu == tomasulo.exec_res == None

    assert tomasulo.Regs.readInt(10) == 12

from riscemv.ISA.ISA import ISA


def test_lui():
    imm = "00000000000010101010"
    rd = "0" * 5
    instruction = "$imm$rd0110111"
    instruction = instruction.replace("$imm", imm)
    instruction = instruction.replace("$rd", rd)
    exp = "10101010000000000000"

    instr = ISA().instruction_from_bin(instruction)
    assert int(exp, 2) == instr.execute(None)


def test_auipc():
    imm = "00000000000010101010"
    rd = "0" * 5
    instruction = "$imm$rd0010111"
    instruction = instruction.replace("$imm", imm)
    instruction = instruction.replace("$rd", rd)
    exp_par = "10101010000000000000"
    PC = 24
    exp = int(exp_par, 2) + PC

    instr = ISA().instruction_from_bin(instruction)
    assert exp == instr.execute(PC)

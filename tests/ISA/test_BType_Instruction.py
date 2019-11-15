from riscemv.ISA.ISA import ISA


def test_beq():
    rd = "0" * 5
    instruction = "0000000$rs2$rs1000100001100011"
    instruction = instruction.replace("$rs1", rd)
    instruction = instruction.replace("$rs2", rd)
    rs1 = 0b00000000000000000000000000001101 # 13
    rs2 = 0b00000000000000000000000000001011 # 11
    exp = 16

    instr = ISA().instruction_from_bin(instruction)
    assert exp == instr.execute(rs1, rs1)

    assert 4 == instr.execute(rs1, rs2)

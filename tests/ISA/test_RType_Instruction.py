from riscemv.ISA.ISA import ISA


def test_add():
    rd = "0" * 5
    instruction = "0000000$rs2$rs1000$rd0110011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rd)
    instruction = instruction.replace("$rs2", rd)
    rs1 = 0b00000000000000000000000000001101 # 13
    rs2 = 0b00000000000000000000000000001011 # 11
    exp = 0b00000000000000000000000000011000 # 24

    instr = ISA().instruction_from_bin(instruction, 0)
    assert exp == instr.execute(rs1, rs2)


def test_sub():
    rd = "0" * 5
    instruction = "0100000$rs2$rs1000$rd0110011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rd)
    instruction = instruction.replace("$rs2", rd)
    rs1 = 0b00000000000000000000000000001101 # 13
    rs2 = 0b00000000000000000000000000001011 # 11
    exp = 0b00000000000000000000000000000010 # 2

    instr = ISA().instruction_from_bin(instruction, 0)
    assert exp == instr.execute(rs1, rs2)


def test_xor():
    rd = "0" * 5
    instruction = "0000000$rs2$rs1100$rd0110011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rd)
    instruction = instruction.replace("$rs2", rd)
    rs1 = 0b00000000000000000000000000001101 # 13
    rs2 = 0b00000000000000000000000000001011 # 11
    exp = 0b00000000000000000000000000000110

    instr = ISA().instruction_from_bin(instruction, 0)
    assert exp == instr.execute(rs1, rs2)


def test_or():
    rd = "0" * 5
    instruction = "0000000$rs2$rs1110$rd0110011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rd)
    instruction = instruction.replace("$rs2", rd)
    rs1 = 0b00000000000000000000000000001101 # 13
    rs2 = 0b00000000000000000000000000001011 # 11
    exp = 0b00000000000000000000000000001111

    instr = ISA().instruction_from_bin(instruction, 0)
    assert exp == instr.execute(rs1, rs2)


def test_and():
    rd = "0" * 5
    instruction = "0000000$rs2$rs1111$rd0110011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rd)
    instruction = instruction.replace("$rs2", rd)
    rs1 = 0b00000000000000000000000000001101 # 13
    rs2 = 0b00000000000000000000000000001011 # 11
    exp = 0b00000000000000000000000000001001

    instr = ISA().instruction_from_bin(instruction, 0)
    assert exp == instr.execute(rs1, rs2)


def test_sll():
    rd = "0" * 5
    instruction = "0000000$rs2$rs1001$rd0110011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rd)
    instruction = instruction.replace("$rs2", rd)
    rs1 = 0b00000000000000000000000000001101 # 13
    rs2 = 0b00000000000000000000000000000001 # 1
    exp = 0b00000000000000000000000000011010

    instr = ISA().instruction_from_bin(instruction, 0)
    assert exp == instr.execute(rs1, rs2)


def test_srl():
    rd = "0" * 5
    instruction = "0000000$rs2$rs1101$rd0110011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rd)
    instruction = instruction.replace("$rs2", rd)
    rs1 = 0b00000000000000000000000000001100 # 12
    rs2 = 0b00000000000000000000000000000001 # 1
    exp = 0b00000000000000000000000000000110

    instr = ISA().instruction_from_bin(instruction, 0)
    assert exp == instr.execute(rs1, rs2)


def test_sra():
    rd = "0" * 5
    instruction = "0100000$rs2$rs1101$rd0110011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rd)
    instruction = instruction.replace("$rs2", rd)
    rs1 = 0b00000000000000000000000000001100 # 12
    rs2 = 0b00000000000000000000000000000001 # 1
    exp = 0b00000000000000000000000000000110

    instr = ISA().instruction_from_bin(instruction, 0)
    assert exp == instr.execute(rs1, rs2)


def test_slt():
    rd = "0" * 5
    instruction = "0000000$rs2$rs1010$rd0110011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rd)
    instruction = instruction.replace("$rs2", rd)
    rs1 = 0b00000000000000000000000000001100 # 12
    rs2 = 0b00000000000000000000000000000001 # 1
    exp = 0b00000000000000000000000000000000

    instr = ISA().instruction_from_bin(instruction, 0)
    assert exp == instr.execute(rs1, rs2)


def test_sltu():
    rd = "0" * 5
    instruction = "0000000$rs2$rs1011$rd0110011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rd)
    instruction = instruction.replace("$rs2", rd)
    rs1 = 0b00000000000000000000000000001100 # 12
    rs2 = 0b00000000000000000000000000000001 # 1
    exp = 0b00000000000000000000000000000000

    instr = ISA().instruction_from_bin(instruction, 0)
    assert exp == instr.execute(rs1, rs2)

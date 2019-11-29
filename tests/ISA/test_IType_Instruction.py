from riscemv.ISA.ISA import ISA


def test_addi():
    rd = "0" * 5
    imm = "000000001011" # 11
    instruction = "$imm$rs1000$rd0010011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rd)
    instruction = instruction.replace("$imm", imm)
    rs1 = 0b00000000000000000000000000001101 # 13
    exp = 0b00000000000000000000000000011000 # 24

    instr = ISA().instruction_from_bin(instruction, 0)
    assert exp == instr.execute(rs1)


def test_xori():
    rd = "0" * 5
    imm = "000000001011" # 11
    instruction = "$imm$rs1100$rd0010011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rd)
    instruction = instruction.replace("$imm", imm)
    rs1 = 0b00000000000000000000000000001101 # 13
    exp = 0b00000000000000000000000000000110

    instr = ISA().instruction_from_bin(instruction, 0)
    assert exp == instr.execute(rs1)


def test_ori():
    rd = "0" * 5
    imm = "000000001011" # 11
    instruction = "$imm$rs1110$rd0010011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rd)
    instruction = instruction.replace("$imm", imm)
    rs1 = 0b00000000000000000000000000001101 # 13
    exp = 0b00000000000000000000000000001111

    instr = ISA().instruction_from_bin(instruction, 0)
    assert exp == instr.execute(rs1)


def test_andi():
    rd = "0" * 5
    imm = "000000001011" # 11
    instruction = "$imm$rs1111$rd0010011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rd)
    instruction = instruction.replace("$imm", imm)
    rs1 = 0b00000000000000000000000000001101 # 13
    exp = 0b00000000000000000000000000001001

    instr = ISA().instruction_from_bin(instruction, 0)
    assert exp == instr.execute(rs1)


def test_slli():
    rd = "0" * 5
    imm = "000000000001" # 11
    instruction = "$imm$rs1001$rd0010011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rd)
    instruction = instruction.replace("$imm", imm)
    rs1 = 0b00000000000000000000000000001101 # 13
    exp = 0b00000000000000000000000000011010

    instr = ISA().instruction_from_bin(instruction, 0)
    assert exp == instr.execute(rs1)


def test_srli():
    rd = "0" * 5
    imm = "000000000001" # 1
    instruction = "$imm$rs1101$rd0010011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rd)
    instruction = instruction.replace("$imm", imm)
    rs1 = 0b00000000000000000000000000001100 # 12
    exp = 0b00000000000000000000000000000110

    instr = ISA().instruction_from_bin(instruction, 0)
    assert exp == instr.execute(rs1)


def test_srai():
    rd = "0" * 5
    imm = "000000000001" # 1
    instruction = "$imm$rs1101$rd0010011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rd)
    instruction = instruction.replace("$imm", imm)
    rs1 = 0b00000000000000000000000000001100 # 12
    exp = 0b00000000000000000000000000000110

    instr = ISA().instruction_from_bin(instruction, 0)
    assert exp == instr.execute(rs1)


def test_slti():
    rd = "0" * 5
    imm = "000000000001" # 1
    instruction = "$imm$rs1010$rd0010011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rd)
    instruction = instruction.replace("$imm", imm)
    rs1 = 0b00000000000000000000000000001100 # 12
    exp = 0b00000000000000000000000000000000

    instr = ISA().instruction_from_bin(instruction, 0)
    assert exp == instr.execute(rs1)


def test_sltui():
    rd = "0" * 5
    imm = "000000000001" # 1
    instruction = "$imm$rs1011$rd0010011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rd)
    instruction = instruction.replace("$imm", imm)
    rs1 = 0b00000000000000000000000000001100 # 12
    exp = 0b00000000000000000000000000000000

    instr = ISA().instruction_from_bin(instruction, 0)
    assert exp == instr.execute(rs1)

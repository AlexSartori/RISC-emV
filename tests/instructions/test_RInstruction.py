from riscemv.instructions.RInstruction import RInstruction


def test_add():
    rd = "0" * 5
    rs1 = "01101" # 13
    rs2 = "01011" # 11
    instruction = "0000000$rs2$rs1000$rd0110011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rs1)
    instruction = instruction.replace("$rs2", rs2)
    exp = "11000" # 24

    instr = RInstruction.parse(instruction)
    assert exp == instr.execute()


def test_sub():
    rd = "0" * 5
    rs1 = "01101" # 13
    rs2 = "01011" # 11
    instruction = "0100000$rs2$rs1000$rd0110011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rs1)
    instruction = instruction.replace("$rs2", rs2)
    exp = "00010" # 2

    instr = RInstruction.parse(instruction)
    assert exp == instr.execute()


def test_xor():
    rd = "0" * 5
    rs1 = "01101" # 13
    rs2 = "01011" # 11
    instruction = "0000000$rs2$rs1100$rd0110011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rs1)
    instruction = instruction.replace("$rs2", rs2)
    exp = "00110"

    instr = RInstruction.parse(instruction)
    assert exp == instr.execute()


def test_or():
    rd = "0" * 5
    rs1 = "01101" # 13
    rs2 = "01011" # 11
    instruction = "0000000$rs2$rs1110$rd0110011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rs1)
    instruction = instruction.replace("$rs2", rs2)
    exp = "01111"

    instr = RInstruction.parse(instruction)
    assert exp == instr.execute()


def test_and():
    rd = "0" * 5
    rs1 = "01101" # 13
    rs2 = "01011" # 11
    instruction = "0000000$rs2$rs1111$rd0110011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rs1)
    instruction = instruction.replace("$rs2", rs2)
    exp = "01001"

    instr = RInstruction.parse(instruction)
    assert exp == instr.execute()


def test_sll():
    rd = "0" * 5
    rs1 = "01101" # 13
    rs2 = "00001" # 1
    instruction = "0000000$rs2$rs1001$rd0110011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rs1)
    instruction = instruction.replace("$rs2", rs2)
    exp = "11010"

    instr = RInstruction.parse(instruction)
    assert exp == instr.execute()


def test_srl():
    rd = "0" * 5
    rs1 = "01100" # 12
    rs2 = "00001" # 1
    instruction = "0000000$rs2$rs1101$rd0110011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rs1)
    instruction = instruction.replace("$rs2", rs2)
    exp = "00110"

    instr = RInstruction.parse(instruction)
    assert exp == instr.execute()


def test_sra():
    rd = "0" * 5
    rs1 = "01100" # 12
    rs2 = "00001" # 1
    instruction = "0100000$rs2$rs1101$rd0110011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rs1)
    instruction = instruction.replace("$rs2", rs2)
    exp = "00110"

    instr = RInstruction.parse(instruction)
    assert exp == instr.execute()


def test_slt():
    rd = "0" * 5
    rs1 = "01100" # 12
    rs2 = "00001" # 1
    instruction = "0000000$rs2$rs1010$rd0110011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rs1)
    instruction = instruction.replace("$rs2", rs2)
    exp = "00000"

    instr = RInstruction.parse(instruction)
    assert exp == instr.execute()


def test_sltu():
    rd = "0" * 5
    rs1 = "01100" # 12
    rs2 = "00001" # 1
    instruction = "0000000$rs2$rs1011$rd0110011"
    instruction = instruction.replace("$rd", rd)
    instruction = instruction.replace("$rs1", rs1)
    instruction = instruction.replace("$rs2", rs2)
    exp = "00000"

    instr = RInstruction.parse(instruction)
    assert exp == instr.execute()

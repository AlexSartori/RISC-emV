from riscemv.ISA.ISA import ISA
from riscemv.ISA.BType_Instruction import BType_Instruction


def test_beq():
    rd = "0" * 5
    instruction = "0000000$rs2$rs1000100001100011"
    instruction = instruction.replace("$rs1", rd)
    instruction = instruction.replace("$rs2", rd)
    rs1 = 0b00000000000000000000000000001101 # 13
    rs2 = 0b00000000000000000000000000001011 # 11
    exp = 16

    instr = ISA().instruction_from_bin(instruction, 0)
    assert exp == instr.execute(rs1, rs1)

    assert 4 == instr.execute(rs1, rs2)


def test_to_bin():
    inst = ISA().instruction_from_str('beq x5, x0, 4', None, 0)  # BType_Instruction(1100011, 5, '000', 1, 2)
    assert inst.to_binary() == '00000000010100000000010001100011'

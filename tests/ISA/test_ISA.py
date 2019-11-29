from riscemv.ISA.ISA import ISA


def test_r_instruction_from_string():
    instruction = "add r4, r3, r2"

    res = ISA().instruction_from_str(instruction, None, None)
    assert res.rd  == 4
    assert res.rs1 == 3
    assert res.rs2 == 2


def test_r_instruction_from_binary():
    instruction = "00000000001000011001001000110011"

    res = ISA().instruction_from_bin(instruction, 0)
    assert res.rd  == 4
    assert res.rs2 == 2
    assert res.rs1 == 3


def test_i_instruction_from_string():
    instruction = "addi r4, r3, 12"

    res = ISA().instruction_from_str(instruction, None, None)
    assert res.rd  == 4
    assert res.rs == 3
    assert res.imm == 12


def test_i_instruction_from_binary():
    instruction = "00000000110000011000001000010011"

    res = ISA().instruction_from_bin(instruction, 0)
    assert res.rd  == 4
    assert res.rs == 3
    assert res.imm == 12

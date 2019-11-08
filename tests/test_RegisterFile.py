import os
from riscemv.RegisterFile import RegisterFile


def test_PC():
    RF = RegisterFile()

    value = "01" * 16
    RF.PC.set_value(value)

    assert RF.PC.get_value() == value


def test_IR():
    RF = RegisterFile()

    value = "01" * 16
    RF.IR.set_value(value)

    assert RF.IR.get_value() == value


def test__int_registers():
    RF = RegisterFile()

    value = "01" * 16

    for reg_n in range(1, 32):
        bin_idx = "{:032b}".format(reg_n)
        RF.writeInt(bin_idx, value)

        assert RF.readInt(bin_idx) == value


def test__fp_registers():
    RF = RegisterFile()

    value = "01" * 16

    for reg_n in range(1, 32):
        bin_idx = "{:032b}".format(reg_n)
        RF.writeFP(bin_idx, value)

        assert RF.readFP(bin_idx) == value

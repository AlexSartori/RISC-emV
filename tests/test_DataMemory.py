import os
from riscemv.DataMemory import DataMemory


def test_DM():
    DM = DataMemory()

    address = "0"
    value = 16
    DM.store(address, value)

    assert DM.load(address) == value

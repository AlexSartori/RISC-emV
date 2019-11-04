import os
from riscemv.DataMemory import DataMemory


def test_PC():
    DM = DataMemory()

    address = "0"
    value = "01" * 16 
    DM.store(address, value)

    assert DM.load(address) == value

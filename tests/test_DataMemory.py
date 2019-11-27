import pytest
from riscemv.DataMemory import DataMemory


def test_DM_rw():
    DM = DataMemory(8)

    address = "0"
    value = 16
    DM.store(address, value)

    assert DM.load(address) == value


def test_DM_segfault():
    DM = DataMemory(8)

    with pytest.raises(MemoryError):
        DM.load(512)

    with pytest.raises(MemoryError):
        DM.store(512, 0x00)


def test_DM_empty():
    DM = DataMemory(8)

    for word in DM:
        assert word == 0x00

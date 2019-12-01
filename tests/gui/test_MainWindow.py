from PyQt5 import QtWidgets
from riscemv.gui.MainWindow import MainWindow


def test_MW_delay(qtbot):
    w = MainWindow()
    w.set_emulation_delay(123)
    assert w.emulation_delay == 123


def test_MW_emu_comp(qtbot):
    w = MainWindow()

    assert w.RF is not None, "RF is None"
    assert w.ResStations is not None, "ResStations is None"
    assert w.RegStatus is not None, "RegStatus is None"
    assert w.IFQ is not None, "IFQ is None"
    assert w.DM is not None, "DM is None"


def test_MW_step():
    w = MainWindow()

    s1 = w.emulator_instance.get_steps()
    w.emulator_step()

    assert w.emulator_instance.get_steps() > s1, "Emulator did not perform a step"

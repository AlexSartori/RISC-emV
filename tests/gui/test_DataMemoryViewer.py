from riscemv.DataMemory import DataMemory
from riscemv.gui.DataMemoryViewer import DataMemoryViewer


def test_DM_write(qtbot):
    DM = DataMemory(1024)
    dm_v = DataMemoryViewer(DM)
    qtbot.addWidget(dm_v)

    DM.store(12, 0x72)
    dm_v.load_contents()

    assert int(dm_v.hex_box.toPlainText().split(' ')[12], 16) == DM.load(12)
    assert dm_v.ascii_box.toPlainText()[12] == chr(DM.load(12))

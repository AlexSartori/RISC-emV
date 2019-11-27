from riscemv.RegisterStatus import RegisterStatus
from riscemv.gui.RegStatusViewer import RegStatusViewer


def test_add_status(qtbot):
    RS = RegisterStatus()
    reg_v = RegStatusViewer(RS)
    qtbot.addWidget(reg_v)

    RS.add_int_status(3, 'ADD0')
    RS.add_fp_status(7, 'DIV0')

    reg_v.load_contents()

    assert reg_v.rs_table.item(0, 3).text() == 'ADD0'
    assert reg_v.rs_table.item(0, 32 + 7).text() == 'DIV0'

    RS.remove_int_status(3)
    RS.remove_fp_status(7)

    reg_v.load_contents()

    assert reg_v.rs_table.item(0, 3).text() == ''
    assert reg_v.rs_table.item(0, 32 + 7).text() == ''

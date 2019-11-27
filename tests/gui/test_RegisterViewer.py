from riscemv.RegisterFile import RegisterFile
from riscemv.gui.RegisterViewer import RegisterViewer

def test_regRead(qtbot):
    RF = RegisterFile()
    reg_v = RegisterViewer(RF)
    qtbot.addWidget(reg_v)

    RF.PC.set_value(123)
    RF.IR.set_value(321)
    RF.IntRegisters[7].set_value(456)
    RF.FPRegisters[13].set_value(78.9)

    reg_v.load_contents()

    assert reg_v.rf_int_table.item(0, 0).text() == '1111011', \
        "Incorrect special register value (PC)"
    assert reg_v.rf_int_table.item(0, 1).text() == '101000001', \
        "Incorrect special register value (IR)"
    assert reg_v.rf_int_table.item(0, 7+2).text() == '111001000', \
        "Incorrect integer register value"
    assert reg_v.rf_fp_table.item(0, 13).text() == '1000010100111011100110011001101', \
        "Incorrect floating point register value"


def test_regWrite(qtbot):
    RF = RegisterFile()
    reg_v = RegisterViewer(RF)
    qtbot.addWidget(reg_v)

    reg_v.load_contents()

    reg_v.rf_int_table.item(0, 0).setText('0001')
    reg_v.rf_int_table.item(0, 1).setText('0010')
    reg_v.rf_int_table.item(0, 7+2).setText('0011')
    reg_v.rf_fp_table.item(0, 13).setText('111110110011001100110011001101')

    assert RF.PC.get_value() == 1, \
        "Incorrect special register value (PC)"
    assert RF.IR.get_value() == 2, \
        "Incorrect special register value (IR)"
    assert RF.IntRegisters[7].get_value() == 3, \
        "Incorrect integer register value"
    assert abs(RF.FPRegisters[13].get_value() - 0.4) < 0.01, \
        "Incorrect floating point register value"


def test_write_display_format(qtbot):
    RF = RegisterFile()
    reg_v = RegisterViewer(RF)
    qtbot.addWidget(reg_v)

    reg_v.load_contents()

    reg_v.format = 'BIN'
    reg_v.rf_int_table.item(0, 7+2).setText('11001001')
    assert RF.IntRegisters[7].get_value() == 201, "Binary format error"

    reg_v.format = 'DEC'
    reg_v.rf_int_table.item(0, 7+2).setText('342')
    assert RF.IntRegisters[7].get_value() == 342, "Decimal format error"

    reg_v.format = 'HEX'
    reg_v.rf_int_table.item(0, 7+2).setText('0xf')
    assert RF.IntRegisters[7].get_value() == 15, "Hex format error"


def test_read_display_format(qtbot):
    RF = RegisterFile()
    reg_v = RegisterViewer(RF)
    qtbot.addWidget(reg_v)

    reg_v.load_contents()

    reg_v.format = 'BIN'
    RF.IntRegisters[7].set_value(201)
    reg_v.load_contents()
    assert reg_v.rf_int_table.item(0, 7+2).text() == '11001001', \
        "Binary format error"

    reg_v.format = 'DEC'
    RF.IntRegisters[7].set_value(342)
    reg_v.load_contents()
    assert reg_v.rf_int_table.item(0, 7+2).text() == '342', \
        "Decimal format error"

    reg_v.format = 'HEX'
    RF.IntRegisters[7].set_value(15)
    reg_v.load_contents()
    assert reg_v.rf_int_table.item(0, 7+2).text() == '0xf', \
        "Hex format error"

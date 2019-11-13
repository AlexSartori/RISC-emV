from PyQt5 import QtWidgets, QtGui, QtCore
from riscemv.RegisterFile import RegisterFile
import struct


class RegisterViewer(QtWidgets.QFrame):
    def __init__(self, RF):
        super(RegisterViewer, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())

        self.RF = RF
        self.format = 'DEC'

        title = QtWidgets.QLabel()
        title.setText("Registers Viewer:")
        self.layout().addWidget(title)

        format_chooser = QtWidgets.QFrame()
        format_chooser.setLayout(QtWidgets.QHBoxLayout())

        fmt_label = QtWidgets.QLabel()
        fmt_label.setText("Display:")
        fmt_bin = QtWidgets.QPushButton()
        fmt_bin.setText("BIN")
        fmt_bin.setStyleSheet("QPushButton { padding: 1px 5px; }")
        fmt_bin.clicked.connect(self.change_format)
        fmt_dec = QtWidgets.QPushButton()
        fmt_dec.setText("DEC")
        fmt_dec.setDown(True)
        fmt_dec.setStyleSheet("QPushButton { padding: 1px 5px; }")
        fmt_dec.clicked.connect(self.change_format)
        fmt_hex = QtWidgets.QPushButton()
        fmt_hex.setText("HEX")
        fmt_hex.setStyleSheet("QPushButton { padding: 1px 5px; }")
        fmt_hex.clicked.connect(self.change_format)
        self.fmt_buttons = [fmt_bin, fmt_dec, fmt_hex]

        format_chooser.layout().addWidget(fmt_label)
        format_chooser.layout().addWidget(fmt_bin)
        format_chooser.layout().addWidget(fmt_dec)
        format_chooser.layout().addWidget(fmt_hex)
        format_chooser.layout().addStretch(1)

        self.rf_int_table = QtWidgets.QTableWidget()
        self.rf_int_table.setColumnCount(32 + 2)
        self.rf_int_table.setRowCount(1)
        self.rf_int_table.verticalHeader().setVisible(False)
        self.rf_int_table.setHorizontalHeaderLabels(['PC', 'IR'] + ["X" + str(r) for r in range(32)])
        self.rf_int_table.setFont(QtGui.QFont('monospace'))

        self.rf_fp_table = QtWidgets.QTableWidget()
        self.rf_fp_table.setColumnCount(32)
        self.rf_fp_table.setRowCount(1)
        self.rf_fp_table.verticalHeader().setVisible(False)
        self.rf_fp_table.setHorizontalHeaderLabels(["FP" + str(r) for r in range(32)])
        self.rf_fp_table.setFont(QtGui.QFont('monospace', 10))

        self.layout().addWidget(format_chooser)
        self.layout().addWidget(self.rf_int_table)
        self.layout().addWidget(self.rf_fp_table)

        self.rf_int_table.cellChanged.connect(self.int_reg_changed)
        self.rf_fp_table.cellChanged.connect(self.fp_reg_changed)
        self.load_contents()


    def int_reg_changed(self, row, col):
        new_val = self.rf_int_table.item(row, col).text()
        if new_val is None or new_val.strip() == '':
            return

        try:
            if self.format == 'BIN':
                new_val = int(new_val, 2)
            elif self.format == 'DEC':
                new_val = int(new_val, 10)
            else:
                new_val = int(new_val, 16)
        except ValueError:
            # TODO: Rollback edit
            raise ValueError("Invalid string for register " + str(new_val))

        if col == 0: # PC
            self.RF.PC.set_value(new_val)
        elif col == 1: # IR
            self.RF.IR.set_value(new_val)
        elif col == 2: # reg zero
            pass
        else:
            self.RF.writeInt(col - 2, new_val)


    def fp_reg_changed(self, row, col):
        new_val = self.rf_fp_table.item(row, col).text()
        if new_val is None or new_val.strip() == '':
            return

        # def float_to_bin(num): bin(struct.unpack('!I', struct.pack('!f', num))[0])[2:].zfill(32)

        try:
            if self.format == 'BIN':
                new_val = struct.unpack('!f', struct.pack('!I', int(new_val, 2)))[0]
            elif self.format == 'DEC':
                new_val = float(new_val)
            else:
                # bytes.fromhex(...) throws exceptions for some inputs (eg: "0" but not "00")
                new_val = struct.unpack('!f', bytes.fromhex(new_val[2:]))[0] # Remove '0x'
        except ValueError:
            # TODO: Rollback edit
            raise ValueError("Invalid string for register: " + new_val)

        self.RF.writeFP(col, new_val)


    def change_format(self):
        self.format = self.sender().text()

        for b in self.fmt_buttons:
            if b != self.sender():
                b.setDown(False)
            else:
                b.setDown(True)

        self.load_contents()


    def format_reg(self, r, fp=False):
        fmt_str_int = {
            'BIN': '{:b}',
            'DEC': '{:d}',
            'HEX': '0x{:x}'
        }

        if r.get_value() is None:
            return ''
        elif not fp:
            return fmt_str_int[self.format].format(r.get_value())
        else:
            if self.format == 'BIN':
                return '{:b}'.format(struct.unpack('!I', struct.pack('!f', r.get_value()))[0])
            elif self.format == 'DEC':
                return '{:f}'.format(r.get_value())
            else:
                return '0x{:x}'.format(struct.unpack('!I', struct.pack('!f', r.get_value()))[0])


    def load_contents(self):
        self.rf_int_table.setItem(0, 0,
            QtWidgets.QTableWidgetItem(self.format_reg(self.RF.PC))
        )
        self.rf_int_table.setItem(0, 1,
            QtWidgets.QTableWidgetItem(self.format_reg(self.RF.IR))
        )

        for i, r in enumerate(self.RF.IntRegisters):
            self.rf_int_table.setItem(0, i + 2,
                QtWidgets.QTableWidgetItem(self.format_reg(r))
            )

        for i, r in enumerate(self.RF.FPRegisters):
            self.rf_fp_table.setItem(0, i,
                QtWidgets.QTableWidgetItem(self.format_reg(r, fp=True))
            )

        self.rf_int_table.resizeRowsToContents()
        self.rf_int_table.setMaximumHeight(
            self.rf_int_table.horizontalHeader().height()
            + self.rf_int_table.rowHeight(0)
            + self.rf_int_table.horizontalScrollBar().height()
        )
        self.rf_int_table.verticalHeader().setStretchLastSection(True)

        self.rf_fp_table.resizeRowsToContents()
        self.rf_fp_table.setMaximumHeight(
            self.rf_fp_table.horizontalHeader().height()
            + self.rf_fp_table.rowHeight(0)
            + self.rf_fp_table.horizontalScrollBar().height()
        )
        self.rf_fp_table.verticalHeader().setStretchLastSection(True)

        self.rf_int_table.resizeColumnsToContents()
        self.rf_fp_table.resizeColumnsToContents()

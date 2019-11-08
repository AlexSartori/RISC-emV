from PyQt5 import QtWidgets, QtGui, QtCore
from riscemv.RegisterFile import RegisterFile


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
        self.rf_int_table.setFont(QtGui.QFont('monospace', 10))

        self.rf_fp_table = QtWidgets.QTableWidget()
        self.rf_fp_table.setColumnCount(32)
        self.rf_fp_table.setRowCount(1)
        self.rf_fp_table.verticalHeader().setVisible(False)
        self.rf_fp_table.setHorizontalHeaderLabels(["FP" + str(r) for r in range(32)])
        self.rf_fp_table.setFont(QtGui.QFont('monospace', 10))

        self.layout().addWidget(format_chooser)
        self.layout().addWidget(self.rf_int_table)
        self.layout().addWidget(self.rf_fp_table)

        self.load_contents()


    def change_format(self):
        self.format = self.sender().text()

        for b in self.fmt_buttons:
            if b != self.sender():
                b.setDown(False)
            else:
                b.setDown(True)

        self.load_contents()


    def load_contents(self):
        def format_reg(r):
            fmt_str = {
                'BIN': '{:b}',
                'DEC': '{:d}',
                'HEX': '0x{:x}'
            }
            return '-' if r.get_value() is None else fmt_str[self.format].format(r.get_value())

        self.rf_int_table.setItem(0, 0,
            QtWidgets.QTableWidgetItem(format_reg(self.RF.PC))
        )
        self.rf_int_table.setItem(0, 1,
            QtWidgets.QTableWidgetItem(format_reg(self.RF.IR))
        )

        for i, r in enumerate(self.RF.IntRegisters):
            self.rf_int_table.setItem(0, i + 2,
                QtWidgets.QTableWidgetItem(format_reg(r))
            )

        for i, r in enumerate(self.RF.FPRegisters):
            self.rf_fp_table.setItem(0, i,
                QtWidgets.QTableWidgetItem(format_reg(r))
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

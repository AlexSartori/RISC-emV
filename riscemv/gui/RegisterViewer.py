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

        self.rf_table = QtWidgets.QTableWidget()
        self.rf_table.setColumnCount(32)
        self.rf_table.setRowCount(1)
        self.rf_table.verticalHeader().setVisible(False)
        self.rf_table.setHorizontalHeaderLabels(["R" + str(r) for r in range(32)])
        self.rf_table.setFont(QtGui.QFont('monospace', 10))

        self.layout().addWidget(format_chooser)
        self.layout().addWidget(self.rf_table)

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
        for i, r in enumerate(self.RF.IntRegisters):
            v = r.get_value()

            if v is None:
                v = '-'
            elif self.format == "BIN":
                v = '{:b}'.format(v)
            elif self.format == "DEC":
                v = '{:d}'.format(v)
            else:
                v = '0x{:x}'.format(v)

            self.rf_table.setItem(0, i, QtWidgets.QTableWidgetItem(v))

        # TODO: somehow imprecise height
        self.rf_table.setMaximumHeight(
            self.rf_table.horizontalHeader().height()
            + self.rf_table.rowHeight(0)
            + self.rf_table.horizontalScrollBar().height()
        )

        self.rf_table.resizeColumnsToContents()

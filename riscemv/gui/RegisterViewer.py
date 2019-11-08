from PyQt5 import QtWidgets, QtGui, QtCore


class RegisterViewer(QtWidgets.QFrame):
    def __init__(self):
        super(RegisterViewer, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())

        title = QtWidgets.QLabel()
        title.setText("Registers Viewer:")
        self.layout().addWidget(title)

        format_chooser = QtWidgets.QFrame()
        format_chooser.setLayout(QtWidgets.QHBoxLayout())

        fmt_label = QtWidgets.QLabel()
        fmt_label.setText("Display:")
        fmt_binary = QtWidgets.QPushButton()
        fmt_binary.setText("BIN")
        fmt_binary.setStyleSheet("QPushButton { padding: 1px 5px; }")
        fmt_binary.setDown(True)
        fmt_decimal = QtWidgets.QPushButton()
        fmt_decimal.setText("DEC")
        fmt_decimal.setStyleSheet("QPushButton { padding: 1px 5px; }")
        fmt_hex = QtWidgets.QPushButton()
        fmt_hex.setText("HEX")
        fmt_hex.setStyleSheet("QPushButton { padding: 1px 5px; }")

        format_chooser.layout().addWidget(fmt_label)
        format_chooser.layout().addWidget(fmt_binary)
        format_chooser.layout().addWidget(fmt_decimal)
        format_chooser.layout().addWidget(fmt_hex)
        format_chooser.layout().addStretch(1)

        rf_table = QtWidgets.QTableWidget()
        rf_table.setColumnCount(32)
        rf_table.setRowCount(1)
        rf_table.verticalHeader().setVisible(False)
        rf_table.setHorizontalHeaderLabels(["R" + str(r) for r in range(32)])
        rf_table.setFont(QtGui.QFont('monospace', 10))

        for r in range(32):
            rf_table.setItem(0, r, QtWidgets.QTableWidgetItem("0101001010"))

        # TODO: somehow imprecise height
        rf_table.setMaximumHeight(
            rf_table.horizontalHeader().height()
            + rf_table.rowHeight(0)
            + rf_table.horizontalScrollBar().height()
        )

        rf_table.resizeColumnsToContents()

        self.layout().addWidget(format_chooser)
        self.layout().addWidget(rf_table)

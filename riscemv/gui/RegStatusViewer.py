from PyQt5 import QtWidgets, QtGui, QtCore


class RegStatusViewer(QtWidgets.QFrame):
    def __init__(self):
        super(RegStatusViewer, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())

        title = QtWidgets.QLabel()
        title.setText("Registers Status Viewer:")
        self.layout().addWidget(title)

        rs_table = QtWidgets.QTableWidget()
        rs_table.setColumnCount(32)
        rs_table.setRowCount(1)
        rs_table.verticalHeader().setVisible(False)
        rs_table.setHorizontalHeaderLabels(["R" + str(r) for r in range(32)])
        rs_table.setFont(QtGui.QFont('monospace', 10))

        for r in range(32):
            rs_table.setItem(0, r, QtWidgets.QTableWidgetItem("-"))

        rs_table.setMaximumHeight(
            rs_table.horizontalHeader().height()
            + rs_table.rowHeight(0)
            + rs_table.horizontalScrollBar().height()
        )

        # rs_table.resizeColumnsToContents()

        self.layout().addWidget(rs_table)

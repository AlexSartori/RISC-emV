from PyQt5 import QtWidgets, QtGui, QtCore


class RegStatusViewer(QtWidgets.QFrame):
    def __init__(self, RS):
        super(RegStatusViewer, self).__init__()
        self.RS = RS
        self.setLayout(QtWidgets.QVBoxLayout())

        title = QtWidgets.QLabel()
        title.setText("Registers Status Viewer:")
        self.layout().addWidget(title)

        self.rs_table = QtWidgets.QTableWidget()
        self.rs_table.setColumnCount(64)
        self.rs_table.setRowCount(1)
        self.rs_table.verticalHeader().setVisible(False)
        self.rs_table.setHorizontalHeaderLabels(["X" + str(r) for r in range(32)]+["FP" + str(r) for r in range(32)])
        self.rs_table.setFont(QtGui.QFont('monospace'))

        self.layout().addWidget(self.rs_table)

        self.load_contents()


    def load_contents(self):
        for i, r in enumerate(self.RS):
            self.rs_table.setItem(0, i, QtWidgets.QTableWidgetItem(r))

        self.rs_table.setMaximumHeight(
            self.rs_table.horizontalHeader().height()
            + self.rs_table.rowHeight(0)
            + self.rs_table.horizontalScrollBar().height()
        )

        # self.rs_table.resizeColumnsToContents()

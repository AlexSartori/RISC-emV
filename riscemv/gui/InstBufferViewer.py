from PyQt5 import QtWidgets, QtGui, QtCore


class InstBufferViewer(QtWidgets.QFrame):
    def __init__(self, IFQ):
        super(InstBufferViewer, self).__init__()
        self.IFQ = IFQ

        self.setLayout(QtWidgets.QVBoxLayout())

        title = QtWidgets.QLabel()
        title.setText("Instruction Buffer Inspector:")
        self.layout().addWidget(title)

        self.ib_table = QtWidgets.QTableWidget()
        self.ib_table.setMinimumSize(600, 150)
        self.ib_table.setColumnCount(4)
        self.ib_table.setHorizontalHeaderLabels(
            ['Instruction', 'Issue', 'Execute', 'Write Result']
        )
        self.ib_table.setRowCount(8)
        self.ib_table.setFont(QtGui.QFont('monospace'))
        self.layout().addWidget(self.ib_table)

        self.load_contents()


    def load_contents(self):
        for i, ifq_entry in enumerate(self.IFQ):
            self.ib_table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(ifq_entry.instruction)))
            self.ib_table.setItem(i, 1, QtWidgets.QTableWidgetItem(ifq_entry.issue))
            self.ib_table.setItem(i, 2, QtWidgets.QTableWidgetItem(ifq_entry.execute))
            self.ib_table.setItem(i, 3, QtWidgets.QTableWidgetItem(ifq_entry.write_result))

        self.ib_table.resizeColumnsToContents()

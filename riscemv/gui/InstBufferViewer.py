from PyQt5 import QtWidgets, QtGui, QtCore


class InstBufferViewer(QtWidgets.QFrame):
    def __init__(self):
        super(InstBufferViewer, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())

        title = QtWidgets.QLabel()
        title.setText("Instruction Buffer Inspector:")
        self.layout().addWidget(title)

        ib_table = QtWidgets.QTableWidget()
        ib_table.setMinimumSize(600, 150)
        ib_table.setColumnCount(4)
        ib_table.setHorizontalHeaderLabels(
            ['Instruction', 'Issue', 'Execute', 'Write Result']
        )
        ib_table.setRowCount(8)
        self.ib_table = ib_table

        print("WARN: Instruction buffer has hardcoded size at <InstBUfferViewer.__init__>")
        for r in range(8):
            ib_table.setItem(r, 0, QtWidgets.QTableWidgetItem("add r3, r4, r5"))
            ib_table.setItem(r, 1, QtWidgets.QTableWidgetItem("1"))
            ib_table.setItem(r, 2, QtWidgets.QTableWidgetItem("4"))
            ib_table.setItem(r, 3, QtWidgets.QTableWidgetItem("8"))

        ib_table.resizeColumnsToContents()
        # ib_table.horizontalHeader().setStretchLastSection(True)
        self.layout().addWidget(ib_table)

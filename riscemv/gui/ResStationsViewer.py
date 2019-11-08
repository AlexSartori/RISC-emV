from PyQt5 import QtWidgets, QtGui, QtCore


class ResStationsViewer(QtWidgets.QFrame):
    def __init__(self):
        super(ResStationsViewer, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())

        title = QtWidgets.QLabel()
        title.setText("Reservation Stations:")
        self.layout().addWidget(title)

        rs_table = QtWidgets.QTableWidget()
        rs_table.setColumnCount(8)
        rs_table.setRowCount(5)
        rs_table.verticalHeader().setVisible(False)
        rs_table.setHorizontalHeaderLabels(
            ['Tag', 'Busy', 'Op', 'Vj', 'Vk', 'Qj', 'Qk', 'A']
        )
        rs_table.horizontalHeader().setStretchLastSection(True) # setResizeMode(QtWidgets.QTableWidget.QHeaderView.Stretch)
        rs_table.setFont(QtGui.QFont('monospace', 10))

        print("WARN: Reservation Stations number has been hardcoded at <MainWindow.create_resstations_view>")
        for r in range(5):
            rs_table.setItem(r, 0, QtWidgets.QTableWidgetItem("-"))

        # rs_table.setMaximumHeight(
        #     rs_table.horizontalHeader().height()
        #     + rs_table.rowHeight(0)
        #     + rs_table.horizontalScrollBar().height()
        # )

        # rs_table.resizeColumnsToContents()

        self.layout().addWidget(rs_table)

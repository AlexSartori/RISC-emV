from PyQt5 import QtWidgets, QtGui, QtCore

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("RISC-emV")
        self.setMinimumSize(600, 300)

        self.initUI()
        self.statusBar().showMessage("Ready")


    def initUI(self):
        self.central_split = QtWidgets.QSplitter()
        self.setCentralWidget(self.central_split)

        self.welcome = QtWidgets.QLabel()
        self.welcome.setText("Welcome. Work is in progress.")
        self.welcome.setFont(QtGui.QFont('SansSerif', 20))

        self.register_view = self.create_register_view()
        self.central_split.addWidget(self.register_view)
        self.central_split.addWidget(self.welcome)
        # self.welcome.setAlignment(QtCore.Qt.AlignHCenter)
        # self.welcome.adjustSize()



    def create_register_view(self):
        frame = QtWidgets.QGroupBox()
        frame.setTitle("Registers")
        frame.setLayout(QtWidgets.QVBoxLayout())

        format_chooser = QtWidgets.QFrame()
        format_chooser.setLayout(QtWidgets.QHBoxLayout())

        fmt_binary = QtWidgets.QPushButton()
        fmt_binary.setText("BIN")
        fmt_decimal = QtWidgets.QPushButton()
        fmt_decimal.setText("DEC")
        fmt_hex = QtWidgets.QPushButton()
        fmt_hex.setText("HEX")

        format_chooser.layout().addWidget(fmt_binary)
        format_chooser.layout().addWidget(fmt_decimal)
        format_chooser.layout().addWidget(fmt_hex)

        rf_table = QtWidgets.QTableWidget()
        rf_table.setColumnCount(2)
        rf_table.setRowCount(32)

        for r in range(32):
            rf_table.setItem(r, 0, QtWidgets.QTableWidgetItem("R" + str(r)))
            rf_table.setItem(r, 1, QtWidgets.QTableWidgetItem("0101001010"))

        frame.layout().addWidget(format_chooser)
        frame.layout().addWidget(rf_table)

        return frame

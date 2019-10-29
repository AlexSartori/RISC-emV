from PyQt5 import QtWidgets, QtGui, QtCore

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        # QtWidgets.QWidget.__init__(self)
        self.initUI()


    def initUI(self):
        self.setWindowTitle("RISC-emV")

        self.welcome = QtWidgets.QLabel()
        self.welcome.setText("Welcome. Work is in progress.")
        self.welcome.setFont(QtGui.QFont('SansSerif', 20))
        # self.welcome.setAlignment(QtCore.Qt.AlignHCenter)
        # self.welcome.adjustSize()

        self.main_hbox = QtWidgets.QHBoxLayout()
        self.main_hbox.addStretch(1)
        self.main_hbox.addWidget(self.welcome)
        self.main_hbox.addStretch(1)

        self.setLayout(self.main_hbox)

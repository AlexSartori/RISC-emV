import sys
from PyQt5.QtWidgets import QApplication
from riscemv.gui.MainWindow import MainWindow


def launch():
    app = QApplication(sys.argv)

    win = MainWindow()
    win.showMaximized()

    sys.exit(app.exec_())

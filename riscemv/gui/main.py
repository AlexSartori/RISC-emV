import sys
from PyQt5.QtWidgets import QApplication
from riscemv.gui.MainWindow import MainWindow
from riscemv.RegisterFile import RegisterFile


def launch():
    app = QApplication(sys.argv)

    win = MainWindow(None, RegisterFile(), None, None)
    win.showMaximized()

    sys.exit(app.exec_())

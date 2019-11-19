import sys
from PyQt5.QtWidgets import QApplication
from riscemv.gui.MainWindow import MainWindow
from riscemv.Tomasulo import Tomasulo


def launch():
    app = QApplication(sys.argv)

    emu = Tomasulo(32, 2, 2, 2, 2)
    win = MainWindow(emu)
    win.showMaximized()

    sys.exit(app.exec_())

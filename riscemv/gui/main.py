from PyQt5.QtWidgets import QApplication
from riscemv.gui.MainWindow import MainWindow
import sys



def launch():
    app = QApplication(sys.argv)

    win = MainWindow()
    win.showMaximized()

    sys.exit(app.exec_())

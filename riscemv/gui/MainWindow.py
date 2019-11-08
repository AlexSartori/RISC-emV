from PyQt5 import QtWidgets, QtGui, QtCore
from riscemv.gui.CodeTextBox import CodeTextBox
from riscemv.gui.InstBufferViewer import InstBufferViewer
from riscemv.gui.RegisterViewer import RegisterViewer
from riscemv.gui.RegStatusViewer import RegStatusViewer
from riscemv.gui.ResStationsViewer import ResStationsViewer

# TODO: divide components into classes

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("RISC-emV")

        self.toolbar = self.create_toolbar()

        self.initUI()
        self.statusBar().showMessage("Ready")


    def initUI(self):
        self.central_split = QtWidgets.QSplitter()
        self.setCentralWidget(self.central_split)

        # Left pane (code view)
        self.text_edit = CodeTextBox()
        self.instbuffer_view = InstBufferViewer()
        self.code_pane = self.create_code_pane()

        # Right pane (registers, etc.)
        self.register_view = RegisterViewer()
        self.regstatus_view = RegStatusViewer()
        self.resstations_view = ResStationsViewer()
        self.status_pane = self.create_status_pane()

        # All together
        self.central_split.addWidget(self.code_pane)
        self.central_split.setStretchFactor(0, 1)
        self.central_split.addWidget(self.status_pane)
        self.central_split.setStretchFactor(1, 3)


    def create_toolbar(self):
        openAction  = QtWidgets.QAction(QtGui.QIcon.fromTheme('document-open'), 'Open', self)
        startAction = QtWidgets.QAction(QtGui.QIcon.fromTheme('media-playback-start'), 'Start', self)
        stepAction  = QtWidgets.QAction(QtGui.QIcon.fromTheme('go-next'), 'Step Forward', self)
        # startAction.setShortcut('Ctrl+R')
        # startAction.triggered.connect(qApp.quit)

        toolbar = self.addToolBar('HomeToolbar')
        toolbar.addAction(openAction)
        toolbar.addAction(startAction)
        toolbar.addAction(stepAction)

        return toolbar


    def create_code_pane(self):
        code_pane = QtWidgets.QSplitter()
        code_pane.setOrientation(QtCore.Qt.Vertical)
        code_pane.setMinimumWidth(250)
        code_pane.addWidget(self.text_edit)
        code_pane.addWidget(self.instbuffer_view)
        code_pane.setStretchFactor(0, 3)
        code_pane.setStretchFactor(1, 1)

        return code_pane


    def create_status_pane(self):
        status_pane = QtWidgets.QFrame()
        status_pane.setLayout(QtWidgets.QVBoxLayout())
        status_pane.layout().addWidget(self.register_view)
        status_pane.layout().addWidget(self.regstatus_view)
        status_pane.layout().addWidget(self.resstations_view)
        status_pane.layout().addStretch(1)

        return status_pane

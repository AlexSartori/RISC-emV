from time import sleep
from PyQt5 import QtWidgets, QtGui, QtCore

from riscemv.ProgramLoader import ProgramLoader

from riscemv.gui.CodeTextBox import CodeTextBox
from riscemv.gui.InstBufferViewer import InstBufferViewer
from riscemv.gui.RegisterViewer import RegisterViewer
from riscemv.gui.RegStatusViewer import RegStatusViewer
from riscemv.gui.ResStationsViewer import ResStationsViewer
from riscemv.gui.DataMemoryViewer import DataMemoryViewer

from riscemv.gui.ConfWindow import ConfWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, emulator_instance):
        super(MainWindow, self).__init__()
        self.setWindowTitle("RISC-emV")
        self.setMinimumSize(self.sizeHint())

        self.emulator_instance = emulator_instance
        self.emulation_delay = 500
        self.init_emulator_components(emulator_instance)
        self.initUI()
        self.statusBar().showMessage("Ready")


    def init_emulator_components(self, emu):
        self.PL = ProgramLoader(32)
        self.RF = emu.Regs
        self.ResStations = emu.RS
        self.RegStatus = emu.RegisterStat
        self.IFQ = emu.IFQ
        self.DM = emu.DM


    def initUI(self):
        openAction  = QtWidgets.QAction(QtGui.QIcon.fromTheme('document-open'), 'Open', self)
        openAction.triggered.connect(self.open_document)
        openAction.setShortcut('Ctrl+O')

        startAction = QtWidgets.QAction(QtGui.QIcon.fromTheme('media-playback-start'), 'Start', self)
        startAction.triggered.connect(self.emulator_run)
        startAction.setShortcut('Ctrl+R')

        delay_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        delay_slider.setFixedWidth(200)
        delay_slider.setMinimum(0)
        delay_slider.setMaximum(1000)
        delay_slider.setTickInterval(50)
        delay_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        delay_slider.setValue(self.emulation_delay)
        delay_slider.valueChanged.connect(self.set_emulation_delay)

        stepAction  = QtWidgets.QAction(QtGui.QIcon.fromTheme('go-next'), 'Step Forward', self)
        stepAction.triggered.connect(self.emulator_step)
        stepAction.setShortcut('Ctrl+Shift+R')

        confAction  = QtWidgets.QAction(QtGui.QIcon.fromTheme('preferences-system'), 'Configuration', self)
        confAction.triggered.connect(self.open_conf_win)
        confAction.setShortcut('Alt+C')

        self.toolbar = self.addToolBar('HomeToolbar')
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon) # ToolButtonFollowStyle)
        self.toolbar.addAction(openAction)
        self.toolbar.addAction(startAction)
        self.toolbar.addWidget(delay_slider)
        self.toolbar.addAction(stepAction)
        self.toolbar.addAction(confAction)


        self.central_split = QtWidgets.QSplitter()
        self.setCentralWidget(self.central_split)


        self.code_textbox = CodeTextBox()
        self.instbuffer_view = InstBufferViewer(self.IFQ)

        self.code_pane = QtWidgets.QSplitter()
        self.code_pane.setOrientation(QtCore.Qt.Vertical)
        self.code_pane.setMinimumWidth(250)
        self.code_pane.addWidget(self.code_textbox)
        self.code_pane.addWidget(self.instbuffer_view)
        self.code_pane.setStretchFactor(0, 3)
        self.code_pane.setStretchFactor(1, 1)


        self.register_view = RegisterViewer(self.RF)
        self.regstatus_view = RegStatusViewer(self.RegStatus)
        self.resstations_view = ResStationsViewer(self.ResStations)
        self.datamemory_view = DataMemoryViewer(self.DM)

        self.status_pane = QtWidgets.QFrame()
        self.status_pane.setLayout(QtWidgets.QVBoxLayout())
        self.status_pane.layout().addWidget(self.register_view)
        self.status_pane.layout().addWidget(self.regstatus_view)
        self.status_pane.layout().addWidget(self.resstations_view)
        self.status_pane.layout().addWidget(self.datamemory_view)
        self.status_pane.layout().addStretch(1)


        self.central_split.addWidget(self.code_pane)
        self.central_split.setStretchFactor(0, 1)
        self.central_split.addWidget(self.status_pane)
        self.central_split.setStretchFactor(1, 3)


    def open_document(self):
        # options = QtWidgets.QFileDialog.Options()
        # options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open file", "", "RISC-V source files (*.s)") # TODO: only .s or ELF
        if not filename: return
        self.PL.load_assembly_code(open(filename).read())

        self.code_textbox.setText(
            '\n'.join([i[0] for i in self.PL.lines])
        )

        for l in self.PL.lines:
            self.IFQ.put(l[1])
        self.instbuffer_view.load_contents()

        # Reset emulator
        self.RF.PC.set_value(0)

        self.statusBar().showMessage("Document loaded.")


    def emulator_step(self):
        # Highlight line
        self.code_textbox.highlight_line(self.RF.PC.get_value() // 4)

        s = self.emulator_instance.step()
        self.statusBar().showMessage("Performed step #" + str(s))

        self.register_view.load_contents()
        self.regstatus_view.load_contents()
        self.instbuffer_view.load_contents()
        self.resstations_view.load_contents()
        self.datamemory_view.load_contents()



    def emulator_run(self):
        self.emulator_step()
        if not self.emulator_instance.is_halted():
            QtCore.QTimer.singleShot(self.emulation_delay, self.emulator_run)


    def open_conf_win(self):
        ConfWindow(self).show()


    def set_emulation_delay(self, v):
        self.emulation_delay = v

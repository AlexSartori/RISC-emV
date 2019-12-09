from PyQt5 import QtWidgets, QtGui, QtCore

from riscemv.gui.TomasuloView import TomasuloView
from riscemv.gui.ConfWindow import ConfWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,):
        super(MainWindow, self).__init__()
        self.setWindowTitle("RISC-emV")
        self.setMinimumSize(self.sizeHint())

        self.emulators = []
        self.emulation_delay = 500
        self.initUI()
        self.add_program_tab()
        self.statusBar().showMessage("Ready")


    def init_emulator_components(self, emu):
        self.RF = emu.Regs
        self.ResStations = emu.RS
        self.RegStatus = emu.RegisterStat
        self.IFQ = emu.IFQ
        self.DM = emu.DM


    def initUI(self):
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

        stepAction = QtWidgets.QAction(QtGui.QIcon.fromTheme('go-next'), 'Step Forward', self)
        stepAction.triggered.connect(self.emulator_step)
        stepAction.setShortcut('Ctrl+Shift+R')

        confAction = QtWidgets.QAction(QtGui.QIcon.fromTheme('preferences-system'), 'Configuration', self)
        confAction.triggered.connect(self.open_conf_win)
        confAction.setShortcut('Alt+C')

        self.toolbar = self.addToolBar('HomeToolbar')
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolbar.addAction(startAction)
        self.toolbar.addWidget(delay_slider)
        self.toolbar.addAction(stepAction)
        self.toolbar.addAction(confAction)


        self.programs_tab = QtWidgets.QTabWidget()
        self.setCentralWidget(self.programs_tab)

    
    def add_program_tab(self):
        tab = TomasuloView()
        self.emulators.append(tab)
        self.programs_tab.addTab(tab, "Program #" + str(len(self.emulators)))


    def emulator_step(self):
        step = 0
        for emu in self.emulators:
            step = max(emu.emulator_step(), step)
        self.statusBar().showMessage("Performed step #" + str(step))


    def emulator_run(self):
        all_halted = True
        self.emulator_step()
        for emu in self.emulators:
            if not emu.emulator_instance.is_halted():
                all_halted = False
        
        if not all_halted:
            QtCore.QTimer.singleShot(self.emulation_delay, self.emulator_run)


    def open_conf_win(self):
        ConfWindow(self).show()


    def set_emulation_delay(self, v):
        self.emulation_delay = v

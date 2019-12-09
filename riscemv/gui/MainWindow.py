from PyQt5 import QtWidgets, QtGui, QtCore

from riscemv.gui.ResStationsViewer import ResStationsViewer
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
        self.init_emulator_components(self.emulators[0])
        self.statusBar().showMessage("Ready")


    def init_emulator_components(self, emu):
        self.ResStations = emu.ResStations


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

        addProgAction = QtWidgets.QAction(QtGui.QIcon.fromTheme('list-add'), 'Add program', self)
        addProgAction.triggered.connect(self.add_program_tab)
        addProgAction.setShortcut('Ctrl+N')

        self.toolbar = self.addToolBar('HomeToolbar')
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolbar.addAction(startAction)
        self.toolbar.addWidget(delay_slider)
        self.toolbar.addAction(stepAction)
        self.toolbar.addAction(confAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(addProgAction)


        self.programs_tab = QtWidgets.QTabWidget()
        self.programs_tab.setTabBar(TabBar(self.programs_tab))
        self.setCentralWidget(self.programs_tab)

    
    def add_program_tab(self):
        thread_id = len(self.emulators)
        tab = TomasuloView(thread_id)
        self.emulators.append(tab)
        self.programs_tab.addTab(tab, "Program #" + str(thread_id))


    def emulator_step(self):
        step = 0
        for emu in self.emulators:
            if not emu.emulator_instance.is_halted():
                step = max(emu.emulator_step(), step)

        for emu in self.emulators: # update all reservation stations
            emu.resstations_view.load_contents()

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


class TabBar(QtWidgets.QTabBar):
    def __init__(self, parent):
        QtWidgets.QTabBar.__init__(self, parent)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        for index in range(self.count()):
            option = QtWidgets.QStyleOptionTab()
            self.initStyleOption(option, index)
            palette = self.palette()
            palette.setColor(palette.Button, ResStationsViewer.get_color(index))
            option.palette = palette
            self.style().drawControl(QtWidgets.QStyle.CE_TabBarTab, option, qp, self)

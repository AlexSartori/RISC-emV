from PyQt5 import QtWidgets, QtGui, QtCore

from riscemv.Tomasulo import Tomasulo

from riscemv.gui.CodeEditor import CodeEditor
from riscemv.gui.InstBufferViewer import InstBufferViewer
from riscemv.gui.RegisterViewer import RegisterViewer
from riscemv.gui.RegStatusViewer import RegStatusViewer
from riscemv.gui.ResStationsViewer import ResStationsViewer
from riscemv.gui.DataMemoryViewer import DataMemoryViewer


class TomasuloView(QtWidgets.QSplitter):
    def __init__(self, thread_id):
        super(TomasuloView, self).__init__()
        self.thread_id = thread_id
        self.emulator_instance = Tomasulo(32, thread_id, 2, 2, 2, 2, 2, 2, 2, 2)
        self.init_emulator_components(self.emulator_instance)
        self.initUI()


    def init_emulator_components(self, emu):
        self.RF = emu.Regs
        self.ResStations = emu.RS
        self.RegStatus = emu.RegisterStat
        self.IFQ = emu.IFQ
        self.DM = emu.DM


    def initUI(self):
        self.code_textbox = CodeEditor(self.DM, self.load_program)
        self.instbuffer_view = InstBufferViewer(self.IFQ)

        self.code_pane = QtWidgets.QTabWidget()
        self.code_pane.setMinimumWidth(250)
        self.code_pane.addTab(self.code_textbox, "Code Editor")
        self.code_pane.addTab(self.instbuffer_view, "Instruction Memory")


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


        self.addWidget(self.code_pane)
        self.setStretchFactor(0, 1)
        self.addWidget(self.status_pane)
        self.setStretchFactor(1, 3)


    def load_program(self, prog):
        self.IFQ.clear()

        for inst in prog:
            self.IFQ.put(inst)
        self.instbuffer_view.load_contents()
        self.datamemory_view.load_contents()

        self.RF.PC.set_value(prog.get_entry_point())
        self.RF.SP.set_value(self.DM.size)
        self.emulator_instance.reset_steps()


    def emulator_step(self):
        s = self.emulator_instance.step()

        self.register_view.load_contents()
        self.regstatus_view.load_contents()
        self.instbuffer_view.load_contents()
        self.resstations_view.load_contents()
        self.datamemory_view.load_contents()

        return s

from PyQt5 import QtWidgets, QtGui, QtCore

from riscemv.ISA.ISA import ISA

from riscemv.gui.InstBufferViewer import InstBufferViewer
from riscemv.gui.RegisterViewer import RegisterViewer
from riscemv.gui.RegStatusViewer import RegStatusViewer
from riscemv.gui.ResStationsViewer import ResStationsViewer


class ConfWindow(QtWidgets.QDialog):
    def __init__(self, main_window):
        super(ConfWindow, self).__init__(main_window)
        self.setWindowTitle("Configure RISC-emV")
        self.setMinimumSize(400, 500)

        self.MW = main_window
        self.initUI()


    def initUI(self):
        self.setLayout(QtWidgets.QVBoxLayout())

        tabs = QtWidgets.QTabWidget()
        self.tab_rs = self.cretae_tab_rs()
        self.tab_isa = self.create_tab_isa()

        tabs.addTab(self.tab_rs, "Reservation Stations")
        tabs.addTab(self.tab_isa, "ISA")

        self.layout().addWidget(tabs)


    def cretae_tab_rs(self):
        frame = QtWidgets.QFrame()
        frame.setLayout(QtWidgets.QFormLayout())

        adders_num = QtWidgets.QSpinBox()
        adders_num.setMinimum(1)
        adders_num.setValue(self.MW.ResStations.adders_number)
        adders_num.valueChanged.connect(self.MW.ResStations.set_adders_number)
        frame.layout().addRow("Number of adders:", adders_num)

        multipliers_num = QtWidgets.QSpinBox()
        multipliers_num.setMinimum(1)
        multipliers_num.setValue(self.MW.ResStations.multipliers_number)
        multipliers_num.valueChanged.connect(self.MW.ResStations.set_multipliers_number)
        frame.layout().addRow("Number of multipliers:", multipliers_num)

        dividers_num = QtWidgets.QSpinBox()
        dividers_num.setMinimum(1)
        dividers_num.setValue(self.MW.ResStations.dividers_number)
        dividers_num.valueChanged.connect(self.MW.ResStations.set_dividers_number)
        frame.layout().addRow("Number of dividers:", dividers_num)

        loaders_num = QtWidgets.QSpinBox()
        loaders_num.setMinimum(1)
        loaders_num.setValue(self.MW.ResStations.loaders_number)
        loaders_num.valueChanged.connect(self.MW.ResStations.set_loaders_number)
        frame.layout().addRow("Number of loaders:", loaders_num)

        storers_num = QtWidgets.QSpinBox()
        storers_num.setMinimum(1)
        storers_num.setValue(self.MW.ResStations.storers_number)
        storers_num.valueChanged.connect(self.MW.ResStations.set_storers_number)
        frame.layout().addRow("Number of storers:", storers_num)

        return frame


    def create_tab_isa(self):
        isa = ISA().ISA
        toolbox = QtWidgets.QToolBox()


        # Lambdas do not preserve context when updating ISA from event signal
        def get_isa_updater(t, i, f):
            def _(v):
                print(t, i, f, v)
                isa[t][i][f] = v
            return _

        for type in isa.keys():
            for inst in isa[type]:
                f = QtWidgets.QFrame()
                f.setLayout(QtWidgets.QFormLayout())

                for inst in isa[type]:
                    f.layout().addRow(inst.upper(), None)

                    op_txt = QtWidgets.QLineEdit()
                    op_txt.setText(isa[type][inst]['exec'])
                    op_txt.textChanged.connect(get_isa_updater(type, inst, 'exec'))
                    f.layout().addRow("Expression:", op_txt)

                    cyc = QtWidgets.QSpinBox()
                    cyc.setMinimum(1)
                    cyc.setValue(isa[type][inst]['clockNeeded'])
                    cyc.valueChanged.connect(get_isa_updater(type, inst, 'clockNeeded'))
                    f.layout().addRow("Clock cycles:", cyc)

                    f.layout().addRow(" ", None)

                scroll = QtWidgets.QScrollArea()
                scroll.setWidgetResizable(True)
                scroll.setWidget(f)

            toolbox.addItem(f, type.upper())

        return toolbox

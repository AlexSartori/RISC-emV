from PyQt5 import QtWidgets, QtGui, QtCore


# TODO: divide components into classes

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("RISC-emV")
        self.setMinimumSize(self.sizeHint())

        openAction  = QtWidgets.QAction(QtGui.QIcon.fromTheme('document-open'), 'Open', self)
        startAction = QtWidgets.QAction(QtGui.QIcon.fromTheme('media-playback-start'), 'Start', self)
        stepAction  = QtWidgets.QAction(QtGui.QIcon.fromTheme('go-next'), 'Step Forward', self)
        # startAction.setShortcut('Ctrl+R')
        # startAction.triggered.connect(qApp.quit)

        self.toolbar = self.addToolBar('HomeToolbar')
        self.toolbar.addAction(openAction)
        self.toolbar.addAction(startAction)
        self.toolbar.addAction(stepAction)

        self.initUI()
        self.statusBar().showMessage("Ready")


    def initUI(self):
        self.central_split = QtWidgets.QSplitter()
        self.setCentralWidget(self.central_split)


        self.text_edit = self.create_code_textbox()
        self.instbuffer_view = self.create_instbuffer_view()

        self.code_pane = QtWidgets.QFrame()
        self.code_pane.setMinimumWidth(250)
        self.code_pane.setLayout(QtWidgets.QVBoxLayout())
        self.code_pane.layout().addWidget(self.text_edit, 3)
        self.code_pane.layout().addWidget(self.instbuffer_view, 1)


        self.register_view = self.create_register_view()
        self.regstatus_view = self.create_regstatus_view()
        self.resstations_view = self.create_resstations_view()

        self.status_pane = QtWidgets.QFrame()
        self.status_pane.setLayout(QtWidgets.QVBoxLayout())
        self.status_pane.layout().addWidget(self.register_view)
        self.status_pane.layout().addWidget(self.regstatus_view)
        self.status_pane.layout().addWidget(self.resstations_view)
        self.status_pane.layout().addStretch(1)


        self.central_split.addWidget(self.code_pane)
        self.central_split.setStretchFactor(0, 1)
        self.central_split.addWidget(self.status_pane)
        self.central_split.setStretchFactor(1, 3)
        # self.welcome.setAlignment(QtCore.Qt.AlignHCenter)
        # self.welcome.adjustSize()


    def create_code_textbox(self):
        frame = QtWidgets.QGroupBox()
        frame.setTitle("Code Viewer")
        frame.setLayout(QtWidgets.QVBoxLayout())

        text_edit = QtWidgets.QTextEdit()
        text_edit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        text_edit.setFont(QtGui.QFont('Monospace', 14))
        text_edit.setText("ADD r4, r3, r5 ; RV32I addition\nSUB r5, r4 r12\nbla bla")

        frame.layout().addWidget(text_edit)
        return frame


    def create_instbuffer_view(self):
        frame = QtWidgets.QGroupBox()
        frame.setTitle("Instruction Buffer Inspector")
        frame.setLayout(QtWidgets.QVBoxLayout())
        # frame.setContentsMargins(0, 20, 0, 0)

        ib_table = QtWidgets.QTableWidget()
        ib_table.setMinimumSize(600, 150)
        ib_table.setColumnCount(4)
        ib_table.setRowCount(8)
        print("WARN: Instruction buffer has hardcoded size at <MainWindow.create_instbuffer_view>")

        ib_table.setHorizontalHeaderLabels(['Instruction', 'Issue', 'Execute', 'Write Result'])

        for r in range(8):
            ib_table.setItem(r, 0, QtWidgets.QTableWidgetItem("add r3, r4, r5"))
            ib_table.setItem(r, 1, QtWidgets.QTableWidgetItem("1"))
            ib_table.setItem(r, 2, QtWidgets.QTableWidgetItem("4"))
            ib_table.setItem(r, 3, QtWidgets.QTableWidgetItem("8"))

        ib_table.resizeColumnsToContents()
        # ib_table.horizontalHeader().setStretchLastSection(True)
        frame.layout().addWidget(ib_table)

        return frame


    def create_register_view(self):
        frame = QtWidgets.QGroupBox()
        frame.setTitle("Registers Inspector")
        frame.setLayout(QtWidgets.QVBoxLayout())

        format_chooser = QtWidgets.QFrame()
        format_chooser.setLayout(QtWidgets.QHBoxLayout())

        fmt_label = QtWidgets.QLabel()
        fmt_label.setText("Display:")
        fmt_binary = QtWidgets.QPushButton()
        fmt_binary.setText("BIN")
        fmt_decimal = QtWidgets.QPushButton()
        fmt_decimal.setText("DEC")
        fmt_hex = QtWidgets.QPushButton()
        fmt_hex.setText("HEX")

        format_chooser.layout().addWidget(fmt_label)
        format_chooser.layout().addWidget(fmt_binary)
        format_chooser.layout().addWidget(fmt_decimal)
        format_chooser.layout().addWidget(fmt_hex)
        format_chooser.layout().addStretch(1)

        rf_table = QtWidgets.QTableWidget()
        rf_table.setColumnCount(32)
        rf_table.setRowCount(1)
        rf_table.verticalHeader().setVisible(False)
        rf_table.setHorizontalHeaderLabels(["R" + str(r) for r in range(32)])

        for r in range(32):
            rf_table.setItem(0, r, QtWidgets.QTableWidgetItem("0101001010"))

        rf_table.setMaximumHeight(
            rf_table.horizontalHeader().height()
            + rf_table.rowHeight(0)
            + rf_table.horizontalScrollBar().height()
        )

        rf_table.resizeColumnsToContents()

        frame.layout().addWidget(format_chooser)
        frame.layout().addWidget(rf_table)

        return frame


    def create_regstatus_view(self):
        frame = QtWidgets.QGroupBox()
        frame.setTitle("Registers Status")
        frame.setLayout(QtWidgets.QVBoxLayout())

        rs_table = QtWidgets.QTableWidget()
        rs_table.setColumnCount(32)
        rs_table.setRowCount(1)
        rs_table.verticalHeader().setVisible(False)
        rs_table.setHorizontalHeaderLabels(["R" + str(r) for r in range(32)])

        for r in range(32):
            rs_table.setItem(0, r, QtWidgets.QTableWidgetItem("-"))

        rs_table.setMaximumHeight(
            rs_table.horizontalHeader().height()
            + rs_table.rowHeight(0)
            + rs_table.horizontalScrollBar().height()
        )

        # rs_table.resizeColumnsToContents()

        frame.layout().addWidget(rs_table)

        return frame


    def create_resstations_view(self):
        frame = QtWidgets.QGroupBox()
        frame.setTitle("Reservation Stations")
        frame.setLayout(QtWidgets.QVBoxLayout())

        rs_table = QtWidgets.QTableWidget()
        rs_table.setColumnCount(8)
        rs_table.setRowCount(5)
        rs_table.verticalHeader().setVisible(False)
        rs_table.setHorizontalHeaderLabels(['Tag', 'Busy', 'Op', 'Vj', 'Vk', 'Qj', 'Qk', 'A'])
        rs_table.horizontalHeader().setStretchLastSection(True) # setResizeMode(QtWidgets.QTableWidget.QHeaderView.Stretch)
        print("WARN: Reservation Stations number has been hardcoded at <MainWindow.create_resstations_view>")

        for r in range(5):
            rs_table.setItem(r, 0, QtWidgets.QTableWidgetItem("-"))

        # rs_table.setMaximumHeight(
        #     rs_table.horizontalHeader().height()
        #     + rs_table.rowHeight(0)
        #     + rs_table.horizontalScrollBar().height()
        # )

        # rs_table.resizeColumnsToContents()

        frame.layout().addWidget(rs_table)

        return frame

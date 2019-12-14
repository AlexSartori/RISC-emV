from riscemv.Program import Program
from riscemv.ELF import ELF
from PyQt5 import QtWidgets, QtGui, QtCore
import os


class CodeEditor(QtWidgets.QFrame):
    def __init__(self, DM, prog_loaded_callback=None):
        self.DM = DM
        self.prog_loaded_callback = prog_loaded_callback

        super(CodeEditor, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())

        title = QtWidgets.QLabel()
        title.setText("Code Viewer:")
        self.layout().addWidget(title)

        self.toolbar = self.create_toolbar()
        self.layout().addWidget(self.toolbar)

        self.text_edit = QtWidgets.QTextEdit()
        self.text_edit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.text_edit.setFont(QtGui.QFont('Monospace'))

        self.layout().addWidget(self.text_edit)


    def setText(self, txt):
        self.text_edit.setText(txt)


    def highlight_line(self, line_num):
        fmt = QtGui.QTextCharFormat()
        fmt.setForeground(QtGui.QBrush(QtGui.QColor(220, 0, 0, 255)))

        block = self.text_edit.document().findBlockByLineNumber(line_num)
        blockPos = block.position()

        cursor = QtGui.QTextCursor(self.text_edit.document())
        cursor.setPosition(blockPos)
        cursor.select(QtGui.QTextCursor.LineUnderCursor)
        cursor.setCharFormat(fmt)


    def create_toolbar(self):
        pane = QtWidgets.QFrame()
        pane.setLayout(QtWidgets.QHBoxLayout())

        btn_open = QtWidgets.QPushButton()
        btn_open.setText('Open')
        btn_open.setIcon(QtGui.QIcon.fromTheme('document-open'))
        btn_open.clicked.connect(self.open_document)
        btn_open.setShortcut('Ctrl+O')
        pane.layout().addWidget(btn_open)

        btn_load = QtWidgets.QPushButton()
        btn_load.setText('Load')
        btn_load.setIcon(QtGui.QIcon.fromTheme('go-next'))
        btn_load.clicked.connect(self.load_program)
        pane.layout().addWidget(btn_load)

        return pane


    def open_document(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open file", "", "RISC-V source files (*.s);; ELF file (*.o)")

        if filename:
            ext = os.path.splitext(filename)[1]
            if ext == '.s':
                self.setText(open(filename, 'r').read())
            else:  # ELF file
                p = Program(self.DM)
                elf = ELF(filename)
                elf.load_program(p)
                code = elf.generate_code_text(p)
                
                self.setText(code)


    def load_program(self):
        p = Program(self.DM)
        p.load_text(self.text_edit.toPlainText())

        if len(p.syntax_errors) > 0:
            for e in p.syntax_errors:
                self.highlight_line(e[0])

            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("One or more syntax errors or unsupported instructions were encountered:")
            msg.setInformativeText(
                '\n'.join(
                    ["\"{}\" at line {}: {}".format(s[1], s[0]+1, s[2]) for s in p.syntax_errors]
                )
            )
            msg.setWindowTitle("Error")
            msg.exec_()

        self.prog_loaded_callback(p)

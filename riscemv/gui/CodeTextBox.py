from PyQt5 import QtWidgets, QtGui, QtCore


class CodeTextBox(QtWidgets.QFrame):
    def __init__(self):
        super(CodeTextBox, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())

        title = QtWidgets.QLabel()
        title.setText("Code Viewer:")
        self.layout().addWidget(title)

        self.text_edit = QtWidgets.QTextEdit()
        self.text_edit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.text_edit.setFont(QtGui.QFont('Monospace'))

        self.layout().addWidget(self.text_edit)


    def setText(self, txt):
        self.text_edit.setText(txt)

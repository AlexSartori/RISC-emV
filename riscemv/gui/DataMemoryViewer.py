from PyQt5 import QtWidgets, QtGui, QtCore


class DataMemoryViewer(QtWidgets.QFrame):
    def __init__(self, DM):
        super(DataMemoryViewer, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.DM = DM

        title = QtWidgets.QLabel()
        title.setText("Data Memory Viewer:")
        self.layout().addWidget(title)

        sub_frame = QtWidgets.QFrame()
        sub_frame.setLayout(QtWidgets.QHBoxLayout())
        sub_frame.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(sub_frame)

        self.hex_box = QtWidgets.QPlainTextEdit()
        self.hex_box.setFont(QtGui.QFont('monospace'))
        self.hex_box.setOverwriteMode(True)
        self.hex_box.setMinimumWidth(210)

        self.ascii_box = QtWidgets.QPlainTextEdit()
        self.ascii_box.setFont(QtGui.QFont('monospace'))
        self.ascii_box.setOverwriteMode(True)
        self.ascii_box.setMinimumWidth(70)

        # Hex.width() = 3*ASCII.width()    :   '00 ' -> 'c'
        sub_frame.layout().addWidget(self.hex_box, 3)
        sub_frame.layout().addWidget(self.ascii_box, 1)

        self.hex_box.verticalScrollBar().valueChanged.connect(
            lambda v: self.ascii_box.verticalScrollBar().setValue(v)
        )
        self.ascii_box.verticalScrollBar().valueChanged.connect(
            lambda v: self.hex_box.verticalScrollBar().setValue(v)
        )

        # self.hex_box.connect(None)
        # self.ascii_box.connect(None)
        self.load_contents()


    def load_contents(self):
        hex_data, ascii_data = [], []

        for val in self.DM:
            hex_data.append('{:02x}'.format(val))
            try:
                c = chr(val)
                if c.isprintable() and c not in ['\n', '\r', '\t', '\v']:
                    ascii_data.append(c)
                else:
                    ascii_data.append('.')
            except ValueError:
                ascii_data.append('.')

        self.hex_box.setPlainText(' '.join(hex_data))
        self.ascii_box.setPlainText(''.join(ascii_data))

import sys
try:
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
except ImportError:
    sys.exit('pyside is required!')

try:
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
except ImportError:
    sys.exit('pyside is required!')
try:
    import matplotlib
except ImportError:
    sys.exit('matplotlib is required!')

matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.pylab import axes, pie


class MatplotlibWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)

        #create figure
        figwidth = 5.0    # inches
        figheight = 3.5   # inches

        self.figure = Figure(figsize=(figwidth, figheight))
        self.canvas = FigureCanvas(self.figure)
        self.axis = self.figure.add_subplot(111)
        self.axis.clear()
        self.layoutVertical = QtGui.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.canvas)

        savePlotBtn = QtGui.QPushButton("Save")

        self.time_lbl = QtGui.QLabel('', )
        self.avg_per_round = QtGui.QLabel('', )
        self.layoutVertical.addWidget(self.time_lbl)
        self.layoutVertical.addWidget(self.avg_per_round)
        self.layoutVertical.addWidget(savePlotBtn)
        savePlotBtn.clicked.connect(self.onSave)

    def add_data(self, values, labels, duration=None, avg=None):
        self.time_lbl.clear()
        self.avg_per_round.clear()
        if duration:
            self.time_lbl.setText('Duration: %g seconds' % duration)
            self.time_lbl.repaint()
        if avg:
            self.avg_per_round.setText('Avg per round: %g' % avg)
            self.avg_per_round.repaint()
        self.axis.clear()
        self.axis.pie(values, labels=labels, explode=None,
                        autopct='%1.1f%%', shadow=True, startangle=90)

    def onSave(self):
        file = QtGui.QFileDialog.getSaveFileName(self, 'Save file', '',)
        fname, _ = file
        self.figure.savefig(fname)


class TicTacToeButton(QtGui.QPushButton):
    """ widget is taken from github user https://github.com/niklasf"""

    def __init__(self):
        QtGui.QPushButton.__init__(self)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                       QtGui.QSizePolicy.Preferred)
        sizePolicy.setHeightForWidth(True)
        self.setSizePolicy(sizePolicy)

        font = self.font()
        font.setPixelSize(50)
        self.setFont(font)

    def heightForWidth(self, width):
        return width

    def sizeHint(self):
        return QtCore.QSize(100, 100)

    def setText(self, text):
        palette = self.palette()
        if text == "X":
            palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.red)
            self.setStyleSheet("color: red;")
        elif text == "O":
            palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.blue)
            self.setStyleSheet("color: blue;")
        self.setPalette(palette)
        super(TicTacToeButton, self).setText(text)



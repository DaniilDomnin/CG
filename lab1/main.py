import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QColorDialog, QLineEdit, QFormLayout, QSlider, \
    QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon, QPainter, QPen, QBrush
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QColor
from PyQt5.uic.properties import QtGui

sys.setrecursionlimit(2000)
class App(QWidget):

    def __init__(self):
        super().__init__()
        self.color = None
        self.type = None
        self.title = 'Color chooser'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 200
        self.setFixedSize(400, 300)
        self.initUI()

    def textchanged(self):
        print(self.rgb_in.text())

    def initUI(self):
        self.go = False
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.rgb_in = QLineEdit()
        self.rgb_in.returnPressed.connect(self.FromRGB)

        self.CMYK_in = QLineEdit()
        self.CMYK_in.returnPressed.connect(self.FromCMYK)

        self.HLS_in = QLineEdit()
        self.HLS_in.returnPressed.connect(self.FromHLS)

        flo = QVBoxLayout()
        rgb_l = QHBoxLayout()
        cmyk_l = QHBoxLayout()
        hls_l = QHBoxLayout()
        flo.addLayout(rgb_l)
        flo.addLayout(cmyk_l)
        flo.addLayout(hls_l)

        flo_1 = QVBoxLayout()
        rgb_l.addLayout(flo_1)
        self.r_s = QSlider(Qt.Orientation.Horizontal)
        self.g_s = QSlider(Qt.Orientation.Horizontal)
        self.b_s = QSlider(Qt.Orientation.Horizontal)
        self.r_s.setRange(0, 256)
        self.g_s.setRange(0, 255)
        self.b_s.setRange(0, 255)
        self.r_s.valueChanged.connect(self.r_update)
        self.g_s.valueChanged.connect(self.g_update)
        self.b_s.valueChanged.connect(self.b_update)
        flo_1.addWidget(self.r_s)
        flo_1.addWidget(self.g_s)
        flo_1.addWidget(self.b_s)

        flo_2 = QVBoxLayout()
        cmyk_l.addLayout(flo_2)
        self.c_s = QSlider(Qt.Orientation.Horizontal)
        self.m_s = QSlider(Qt.Orientation.Horizontal)
        self.y_s = QSlider(Qt.Orientation.Horizontal)
        self.k_s = QSlider(Qt.Orientation.Horizontal)
        self.c_s.setRange(0, 255)
        self.m_s.setRange(0, 255)
        self.y_s.setRange(0, 255)
        self.k_s.setRange(0, 255)

        self.c_s.valueChanged.connect(self.c_update)
        self.m_s.valueChanged.connect(self.m_update)
        self.y_s.valueChanged.connect(self.y_update)
        self.k_s.valueChanged.connect(self.k_update)

        flo_2.addWidget(self.c_s)
        flo_2.addWidget(self.m_s)
        flo_2.addWidget(self.y_s)
        flo_2.addWidget(self.k_s)

        flo_3 = QVBoxLayout()
        hls_l.addLayout(flo_3)
        self.h_s = QSlider(Qt.Orientation.Horizontal)
        self.s_s = QSlider(Qt.Orientation.Horizontal)
        self.l_s = QSlider(Qt.Orientation.Horizontal)
        self.h_s.valueChanged.connect(self.h_update)
        self.s_s.valueChanged.connect(self.s_update)
        self.l_s.valueChanged.connect(self.l_update)

        self.h_s.setRange(0, 356)
        self.s_s.setRange(0, 100)
        self.l_s.setRange(0, 100)

        flo_3.addWidget(self.h_s)
        flo_3.addWidget(self.s_s)
        flo_3.addWidget(self.l_s)

        rgb_l.addWidget(self.rgb_in)
        cmyk_l.addWidget(self.CMYK_in)
        hls_l.addWidget(self.HLS_in)

        button = QPushButton('Open color dialog', self)
        button.setToolTip('Opens color dialog')
        button.move(10, 10)
        button.clicked.connect(self.on_click)

        flo.addWidget(button)
        self.setLayout(flo)
        self.show()
        self.SetValue(QColor.fromRgb(0,0,0))
    @pyqtSlot()
    def on_click(self):
        if not self.go:
            self.openColorDialog()

    def r_update(self, value):
        if not self.go:
            self.SetValue(QColor.fromRgb(value, self.g_s.value(), self.b_s.value()))

    def g_update(self, value):
        if not self.go:
            self.SetValue(QColor.fromRgb(self.r_s.value(), value, self.b_s.value()))

    def b_update(self, value):
        if not self.go:
            self.SetValue(QColor.fromRgb(self.r_s.value(), self.g_s.value(), value))

    def c_update(self, value):
        if not self.go:
            self.SetValue(QColor.fromCmyk(value, self.m_s.value(), self.y_s.value(), self.k_s.value()))

    def m_update(self, value):
        if not self.go:
            self.SetValue(QColor.fromCmyk(self.c_s.value(), value, self.y_s.value(), self.k_s.value()))

    def y_update(self, value):
        if not self.go:
            self.SetValue(QColor.fromCmyk(self.c_s.value(), self.m_s.value(), value, self.k_s.value()))

    def k_update(self, value):
        if not self.go:
            self.SetValue(QColor.fromCmyk(self.c_s.value(), self.m_s.value(), self.y_s.value(), value))

    def h_update(self, value):
        if not self.go:
            b = int(self.s_s.value() * 255 / 100)
            c = int(self.l_s.value() * 255 / 100)
            self.SetValue(QColor.fromHsl(value, b, c))

    def s_update(self, value):
        if not self.go:
            c = int(self.l_s.value() * 255 / 100)
            self.SetValue(QColor.fromHsl(self.h_s.value(), int(value * 255 / 100), c))

    def l_update(self, value):
        if not self.go:
            b = int(self.s_s.value() * 255 / 100)
            self.SetValue(QColor.fromHsl(self.h_s.value(), b, int(value * 255 / 100)))


    def FromRGB(self):
        value = [int(word) for word in self.rgb_in.text().split(" ")]
        self.SetValue(QColor.fromRgb(*value))

    def FromCMYK(self):
        value = [int(word) for word in self.CMYK_in.text().split(" ")]
        self.SetValue(QColor.fromCmyk(*value))

    def FromHLS(self):
        value = [int(word) for word in self.HLS_in.text().split(" ")]
        value[1] *= 255
        value[2] *= 255
        self.SetValue(QColor.fromHsl(*value))

    def openColorDialog(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.color = color
            self.SetValue(color)

    def SetValue(self, color: QColor):
        self.go = True
        self.color = color
        self.rgb_in.setText(str(color.red()) + " " + str(color.green()) + " " + str(color.blue()))
        self.r_s.setValue(color.red())
        self.g_s.setValue(color.green())
        self.b_s.setValue(color.blue())
        tp = color.getCmyk()
        str_tp = str(tp[0]) + " " + str(tp[1]) + " " + str(tp[2]) + " " + str(tp[3])
        self.c_s.setValue(tp[0])
        self.m_s.setValue(tp[1])
        self.y_s.setValue(tp[2])
        self.k_s.setValue(tp[3])
        tp_2 = color.getHsl()
        str_tp_2 = str(tp_2[0]) + " " + "{0:.3f}".format(tp_2[1] / 255) + " " + "{0:.3f}".format(tp_2[2] / 255)
        self.h_s.setValue(tp_2[0])
        self.s_s.setValue(int(tp_2[1] / 255 * 100))
        self.l_s.setValue(int(tp_2[2] / 255 * 100))
        self.CMYK_in.setText(str_tp)
        self.HLS_in.setText(str_tp_2)
        self.go = False
        self.update()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        brush = QBrush(Qt.SolidPattern)
        try:
            brush.setColor(self.color)
        except:
            brush.setColor(QColor.fromRgb(0, 0, 0))

        qp.setBrush(brush)
        qp.drawRect(10, 130, 300, 60)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

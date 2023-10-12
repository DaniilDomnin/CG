import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QColorDialog, QLineEdit, QFormLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QColor


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
        self.initUI()

    def textchanged(self):
        print(self.rgb_in.text())

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.rgb_in = QLineEdit()
        self.rgb_in.returnPressed.connect(self.FromRGB)

        self.CMYK_in = QLineEdit()
        self.CMYK_in.returnPressed.connect(self.FromCMYK)

        self.HLS_in = QLineEdit()
        self.HLS_in.returnPressed.connect(self.FromHLS)

        flo = QFormLayout()
        flo.addRow("RGB", self.rgb_in)
        flo.addRow("CMYK", self.CMYK_in)
        flo.addRow("HLS", self.HLS_in)

        button = QPushButton('Open color dialog', self)
        button.setToolTip('Opens color dialog')
        button.move(10, 10)
        button.clicked.connect(self.on_click)

        self.draw_label = QLabel()
        self.draw_label.setText("Current Color")

        flo.addRow(button)
        flo.addRow(self.draw_label)
        self.setLayout(flo)
        self.show()

    @pyqtSlot()
    def on_click(self):
        self.openColorDialog()

    def FromRGB(self):
        value = [int(word) for word in self.rgb_in.text().split(" ")]
        self.SetValue(QColor.fromRgb(*value))

    def FromCMYK(self):
        value = [int(word) for word in self.CMYK_in.text().split(" ")]
        self.SetValue(QColor.fromCmyk(*value))

    def FromHLS(self):
        value = [int(word) for word in self.HLS_in.text().split(" ")]
        self.SetValue(QColor.fromHsl(*value))

    def openColorDialog(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.color = color
            self.SetValue(color)

    def SetValue(self, color: QColor):
        self.rgb_in.setText(str(color.red()) + " " + str(color.green()) + " " + str(color.blue()))
        tp = color.getCmyk()
        str_tp = str(tp[0]) + " " + str(tp[1]) + " " + str(tp[2]) + " " + str(tp[3])
        tp_2 = color.getHsl()
        str_tp_2 = str(tp_2[0]) + " " + str(tp_2[1]) + " " + str(tp_2[2])
        self.CMYK_in.setText(str_tp)
        self.HLS_in.setText(str_tp_2)
        self.draw_label.setStyleSheet(('* { color: ' + color.name() + ' }'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
import os
import sys
import requests
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('part_4.ui', self)
        self.comboBox.addItems(['Схема', 'Спутник', 'Гибрид'])
        self.search_btn.clicked.connect(self.getImage)

    def getImage(self):
        type = ''
        if self.comboBox.currentText() == 'Схема':
            type = 'map'
        elif self.comboBox.currentText() == 'Спутник':
            type = 'sat'
        else:
            type = 'sat,skl'
        params = {
            'll': ','.join([self.lineEdit.text(), self.lineEdit_2.text()]),
            'z': self.lineEdit_3.text(),
            'l': type
        }
        server = "http://static-maps.yandex.ru/1.x"
        response = requests.get(server, params=params)

        if response:
            self.map_file = "map.png"
            with open(self.map_file, "wb") as file:
                file.write(response.content)
            pixmap = QPixmap(self.map_file)
            self.image.setPixmap(pixmap)

    def keyPressEvent(self, event):
        self.lineEdit.clearFocus()
        self.lineEdit_2.clearFocus()
        self.lineEdit_3.clearFocus()
        long = float(self.lineEdit.text())
        lat = float(self.lineEdit_2.text())
        scale = int(self.lineEdit_3.text())
        if event.key() == Qt.Key_PageUp and scale < 17:
            scale += 1
            self.lineEdit_3.setText(str(scale))
        elif event.key() == Qt.Key_PageDown and scale > 0:
            scale -= 1
            self.lineEdit_3.setText(str(scale))
        elif event.key() == Qt.Key_Right and long < 179:
            long += 1
            self.lineEdit.setText(str(long))
        elif event.key() == Qt.Key_Left and long > -180:
            long -= 1
            self.lineEdit.setText(str(long))
        elif event.key() == Qt.Key_Up and lat < 90:
            lat += 1
            self.lineEdit_2.setText(str(lat))
        elif event.key() == Qt.Key_Down and lat > -90:
            lat -= 1
            self.lineEdit_2.setText(str(lat))
        self.getImage()

    def closeEvent(self, event):
        os.remove(self.map_file)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())

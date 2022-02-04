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
        uic.loadUi('part_2.ui', self)
        self.pushButton.clicked.connect(self.getImage)

    def getImage(self):
        params = {
            'll': ','.join([self.lineEdit.text(), self.lineEdit_2.text()]),
            'z': self.lineEdit_3.text(),
            'l': 'map'
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
        scale = int(self.lineEdit_3.text())
        if event.key() == Qt.Key_PageUp and scale < 17:
            scale += 1
            self.lineEdit_3.setText(str(scale))
            self.getImage()
        elif event.key() == Qt.Key_PageDown and scale > 0:
            scale -= 1
            self.lineEdit_3.setText(str(scale))
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

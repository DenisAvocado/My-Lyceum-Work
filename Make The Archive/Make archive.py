import os
import shutil
import datetime as dt

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('make_arc.ui', self)
        self.chose1.clicked.connect(self.chose)
        self.chose2.clicked.connect(self.chose)
        self.but_go.clicked.connect(self.go)

    def chose(self):
        if self.sender().objectName()[-1] == '1':
            fname = QFileDialog.getExistingDirectory(self, 'Выбрать директорию', '')
            self.lab_way1.setText(fname)
        elif self.sender().objectName()[-1] == '2':
            dname = QFileDialog.getExistingDirectory(self, 'Выбрать директорию', '')
            self.lab_way2.setText(dname)

    def go(self):
        if self.lab_way1.text() and self.lab_way2.text():
            make_reverse_arc(self.lab_way1.text(), self.lab_way2.text())
            self.statusBar().showMessage('Успешно!')
        else:
            self.statusBar().showMessage('Не все поля заполены!')


def make_reverse_arc(source, dest):
    name = dt.datetime.now().strftime('%c').replace(':', '-')
    shutil.make_archive(name, 'zip', root_dir=source)
    shutil.move(f'{os.path.curdir}/{name}.zip', dest)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
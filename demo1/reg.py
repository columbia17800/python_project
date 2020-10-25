# This Python file uses the following encoding: utf-8
import sys
import os


from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

class Reg:

    def __init__(self):
        self.ui = QUiLoader().load("C:/Users/Zeheng/Desktop/project/python-project/demo1/reg.ui")

        self.ui.pushButton.clicked.connect(self.sign)
        self.ui.lineEdit.returnPressed.connect(self.sign)
        self.ui.lineEdit_2.returnPressed.connect(self.sign)

    def sign(self):
        id = self.ui.lineEdit.text()
        pin = self.ui.lineEdit_2.text()
        print(id, pin, "send id and pin to server")



# This Python file uses the following encoding: utf-8
import sys
import os

from reg import Reg
from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader

class Login:

    def __init__(self):
        qfile_login = QFile("C:/Users/Zeheng/Desktop/project/python-project/demo1/login.ui")
        qfile_login.open(QFile.ReadOnly)
        self.ui = QUiLoader().load(qfile_login)
        qfile_login.close()


        self.ui.pushButton.clicked.connect(self.log)
        self.ui.lineEdit.returnPressed.connect(self.log)
        self.ui.lineEdit_2.returnPressed.connect(self.log)

        self.ui.pushButton_2.clicked.connect(self.exit)

        self.ui.commandLinkButton.clicked.connect(self.regist)

    def log(self):
        id = self.ui.lineEdit.text()
        pin = self.ui.lineEdit_2.text()
        print(id, pin, "send id and pin to server")

    def exit(self):
        app.exit()

    def regist(self):
        print("this guy want to sign up!")
        self.reg = Reg()
        self.reg.ui.show()


app = QApplication([])
login = Login()
login.ui.show()
app.exec_()

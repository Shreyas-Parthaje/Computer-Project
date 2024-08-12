
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5 import uic
import sys

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


# Code for login window
class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()

        #Loading .ui file
        uic.loadUi('login.ui', self)

        #declaring(identifying) widgets from .ui file
        self.loginButton=0
        self.registerWindowButton=self.findChild(QPushButton, "pushButton_2")

        #Button click checking code
        self.registerWindowButton.clicked.connect(self.openRegisterWindow)

    #This function will be excecuted when registerWindowButton is clicked
    def openRegisterWindow(self, checked):
        #Window initialisation
        self.w=RegisterWindow()
        #Execution of window
        self.w.show()

#Code for register window
class RegisterWindow(QMainWindow):
    def __init__(self):
        super(RegisterWindow, self).__init__()

        #Loading .ui file
        uic.loadUi('register.ui', self)

        #declaring(identifying) widgets from .ui file
        self.loginWindowButton=self.findChild(QPushButton, "pushButton_2")

        #Button click checking code
        self.loginWindowButton.clicked.connect(self.openLoginWindow)

    #This function will be excecuted when loginWindowButton is clicked
    def openLoginWindow(self, checked):
        #Window initialisation
        self.w=LoginWindow()
        #Execution of window
        self.w.show()


#App initialisation
app=QApplication(sys.argv)
#Window initialisation
Mainwindow=LoginWindow()
#Execution of window
Mainwindow.show()
#Execution of app
app.exec_()
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QCalendarWidget, QTextEdit, QLabel, QFrame, QPushButton, QLineEdit, QMessageBox, QGraphicsBlurEffect, QGraphicsDropShadowEffect
from PyQt5 import uic
import sys
import backgroundimg
import background_addEarningAndExpenseWindow
from dbFunctions import *

#QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
#QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

uid=0
calenderWindowSource=0
# Code for login window
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Loading .ui file
        uic.loadUi('UI/loginwindow.ui', self)

        # Get the database connection
        self.connection = DatabaseConnection().get_connection()

        #declaring(identifying) widgets from .ui file
        self.loginButton=self.findChild(QPushButton, 'pushButton')
        self.registerWindowButton=self.findChild(QPushButton, "pushButton_4")
        self.emailField=self.findChild(QLineEdit, 'lineEdit_3')
        self.passwordField=self.findChild(QLineEdit, 'lineEdit_2')

        #Button click checking code
        self.registerWindowButton.clicked.connect(self.openRegisterWindow)

        self.loginButton.clicked.connect(self.login)

    def login(self):
        email = self.emailField.text()
        password = self.passwordField.text()
        
        if login_user(self.connection, email, password):
            global uid
            uid=login_user(self.connection, email, password)[0]
            self.w=MainWindow()
            self.w.show()
        else:
            msg=QMessageBox()
            msg.setWindowTitle("Something went wrong.")
            msg.setText("Invalid email or password.")
            msg.exec_()


    #This function will be excecuted when registerWindowButton is clicked
    def openRegisterWindow(self, checked):
        #Window initialisation
        self.w=RegisterWindow()
        #Execution of window
        self.w.show()
        self.close()

#Code for register window
class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Loading .ui file
        uic.loadUi('UI/registerwindow.ui', self)

        # Get the database connection
        self.connection = DatabaseConnection().get_connection()

        #declaring(identifying) widgets from .ui file
        self.loginWindowButton=self.findChild(QPushButton, "pushButton_3")
        self.emailField=self.findChild(QLineEdit, 'lineEdit')
        self.passwordField=self.findChild(QLineEdit, 'lineEdit_2')
        self.registerWindowButton=self.findChild(QPushButton, 'pushButton')
        

        #Button click checking code
        self.loginWindowButton.clicked.connect(self.openLoginWindow)
        self.registerWindowButton.clicked.connect(self.register)

    #This function will be excecuted when loginWindowButton is clicked
    def openLoginWindow(self, checked):
        #Window initialisation
        self.w=LoginWindow()
        #Execution of window
        self.w.show()
        self.close()

    def register(self):
        email = self.emailField.text()
        password = self.passwordField.text()
        
        try:
            if email and password:  
                register_user(self.connection, email, password)
                self.w=MainWindow()
                self.w.show()
            else:
                msg=QMessageBox()
                msg.setWindowTitle("Something went wrong.")
                msg.setText("Please enter both email and password.")
                msg.exec_()

        except:
            msg=QMessageBox()
            msg.setWindowTitle("Something went wrong.")
            msg.setText("User already exists.")
            msg.exec_()

class deleteRecordWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('UI/deleteRecordWindow.ui', self)

        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global uid

        self.connection = DatabaseConnection().get_connection()

        #Loading .ui file
        uic.loadUi('UI/mainwindow.ui', self)

        self.addEarningButton=self.findChild(QPushButton, "pushButton")
        self.lightThemeCheckBox=self.findChild(QPushButton, "pushButton_3")
        self.totalSpendingValue=self.findChild(QLabel, "label_7")
        self.totalEarningValue=self.findChild(QLabel, "label_5")
        self.searchButton=self.findChild(QPushButton, "pushButton_4")
        self.deleteRecordButton=self.findChild(QPushButton, "pushButton_5")


        self.addEarningButton.clicked.connect(self.openAddEarningWindow)
        self.lightThemeCheckBox.clicked.connect(self.switchToLightTheme)
        self.searchButton.clicked.connect(self.openSearchResults)
        self.deleteRecordButton.clicked.connect(self.openDeleteRecordPopup)
        
        self.recordResult=view_recent_records(self.connection, uid)
        
        self.totalEarningValue.setText(str(self.recordResult[0]))
        self.totalSpendingValue.setText(str(self.recordResult[1]))

    def openDeleteRecordPopup(self):
        self.w=deleteRecordWindow()
        self.w.show()


    def openAddEarningWindow(self):
        self.w=addEarningWindow()
        self.w.show()

    def openSearchResults(self):
        self.w=searchResult()
        self.w.show()

    def switchToLightTheme(self):
        if self.lightThemeCheckBox.isChecked():
            self.lightThemeCheckBox.setStyleSheet('QPushButton{background-color:white;border:2px solid;border-radius:7px;border-color:rgb(62, 58, 83);}')
        
        else:
            self.lightThemeCheckBox.setStyleSheet('QPushButton{background-color:rgb(61, 40, 224);border:2px solid;border-radius:7px;border-color:rgb(62, 58, 83);}')

class searchResult(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('UI/searchResult.ui', self)

        


class calenderWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        global date
        uic.loadUi('UI/calenderWidget.ui', self)

        self.calender=self.findChild(QCalendarWidget, 'calendarWidget')
        self.setDateButton=self.findChild(QPushButton, 'pushButton')

        self.setDateButton.clicked.connect(self.setDate)

    def setDate(self):
        global calenderWindowSource
        self.selectedDate=self.calender.selectedDate().toString()

        if calenderWindowSource=='addEarningWindow':
            self.addEarningWindow=addEarningWindow()
            self.addEarningWindow.dateButton.setText(self.selectedDate)
            self.addEarningWindow.show()
        else:
            self.addExpenseWindow=addExpenseWindow()
            self.addExpenseWindow.dateButton.setText(self.selectedDate)
            self.addExpenseWindow.show()

class addExpenseWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("UI/addExpenseWindow.ui", self)

        self.connection = DatabaseConnection().get_connection()

        self.openEarningWindowButton=self.findChild(QPushButton, "pushButton_3")
        self.recurringExpenseCheckBox=self.findChild(QPushButton, "pushButton_5")
        self.addExpenseButton=self.findChild(QPushButton, "pushButton")

        self.amountField=self.findChild(QLineEdit, "lineEdit_2")
        self.expenseNameField=self.findChild(QLineEdit, "lineEdit_3")
        self.dateButton=self.findChild(QPushButton, "pushButton_2")
        self.descriptionField=self.findChild(QTextEdit, "textEdit")

        self.openEarningWindowButton.clicked.connect(self.openEarningWindow)
        self.recurringExpenseCheckBox.clicked.connect(self.changeState)
        self.addExpenseButton.clicked.connect(self.addExpense)
        self.dateButton.clicked.connect(self.openCalenderWindow)

        #This code has to be improved.
        self.dateText=self.dateButton.text().split('/')
        self.sqlDateText=''

        for i in self.dateText[::-1]:
            self.sqlDateText+=i+'-'
        self.sqlDateText=self.sqlDateText[0:-1]

    def openCalenderWindow(self):
        global calenderWindowSource

        calenderWindowSource='addExpenseWindow'
        self.close()
        self.w=calenderWidget()
        self.w.show()
        
    def openEarningWindow(self):
        self.w=addEarningWindow()
        self.w.show()
        self.close()

    def changeState(self):
        if self.recurringExpenseCheckBox.isChecked():
            self.recurringExpenseCheckBox.setStyleSheet('QPushButton{background-color:rgb(61, 40, 224);border:2px solid;border-radius:7px;border-color:rgb(71, 71, 71);}')
            self.recurringExpenseCheckBox.setChecked(True)
        else:
            self.recurringExpenseCheckBox.setStyleSheet('QPushButton{background-color:rgba(217, 217, 217,0);border:2px solid;border-radius:7px;border-color:rgb(71, 71, 71);}')
            self.recurringExpenseCheckBox.setChecked(False)


    def addExpense(self):
        global uid
        add_expense(self.connection,  self.expenseNameField.text(), self.amountField.text(), self.sqlDateText, self.descriptionField.toPlainText(), uid, self.recurringExpenseCheckBox.isChecked())
        msg=QMessageBox()
        msg.setWindowTitle("Successfull.")
        msg.setText("Record added successfully.")
        msg.exec_()


class addEarningWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("UI/addEarningWindow.ui", self)

        self.connection = DatabaseConnection().get_connection()


        self.openExpenseWindowButton=self.findChild(QPushButton, "pushButton_4")
        self.recurringEarningCheckBox=self.findChild(QPushButton, "pushButton_5")
        self.addEarningButton=self.findChild(QPushButton, "pushButton")

        self.earningNameField=self.findChild(QLineEdit,"lineEdit_3")
        self.amountField=self.findChild(QLineEdit,"lineEdit_2")
        self.dateButton=self.findChild(QPushButton, "pushButton_2")
        self.descriptionField=self.findChild(QTextEdit, "textEdit")

        self.openExpenseWindowButton.clicked.connect(self.openExpenseWindow)
        self.recurringEarningCheckBox.clicked.connect(self.changeState)
        self.addEarningButton.clicked.connect(self.addEarning)
        self.dateButton.clicked.connect(self.openCalenderWindow)

        #This code has to be improved
        self.dateText=self.dateButton.text().split('/')
        self.sqlDateText=''

        for i in self.dateText[::-1]:
            self.sqlDateText+=i+'-'
        self.sqlDateText=self.sqlDateText[0:-1]

    def openCalenderWindow(self):
        global calenderWindowSource

        calenderWindowSource='addEarningWindow'
        self.close()
        self.w=calenderWidget()
        self.w.show()


    def addEarning(self):
        global uid
        add_income(self.connection, self.earningNameField.text(), self.amountField.text(), self.sqlDateText, self.descriptionField.toPlainText(), uid, self.recurringEarningCheckBox.isChecked())
        msg=QMessageBox()
        msg.setWindowTitle("Successfull.")
        msg.setText("Record added successfully.")
        msg.exec_()
        
    def openExpenseWindow(self):
        self.w=addExpenseWindow()
        self.w.show()
        self.close()

    def changeState(self):
        if self.recurringEarningCheckBox.isChecked():
            self.recurringEarningCheckBox.setStyleSheet('QPushButton{background-color:rgb(61, 40, 224);border:2px solid;border-radius:7px;border-color:rgb(71, 71, 71);}')
            self.recurringEarningCheckBox.setChecked(True)
        else:
            self.recurringEarningCheckBox.setStyleSheet('QPushButton{background-color:rgba(217, 217, 217,0);border:2px solid;border-radius:7px;border-color:rgb(71, 71, 71);}')
            self.recurringEarningCheckBox.setChecked(False)
            
#App initialisation
app=QApplication(sys.argv)

# Initialize the database connection
DatabaseConnection()

#Window initialisation
Mainwindow=LoginWindow()

#Execution of window
Mainwindow.show()

#Execution of app
app.exec_()

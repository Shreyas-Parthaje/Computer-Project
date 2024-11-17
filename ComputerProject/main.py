from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QCalendarWidget,QComboBox, QTextEdit, QLabel, QFrame, QPushButton, QLineEdit, QMessageBox, QGraphicsBlurEffect, QGraphicsDropShadowEffect
from PyQt5 import uic
import sys
import backgroundimg
import background_addEarningAndExpenseWindow
from dbFunctions import *

#QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
#QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

uid=0
calenderWindowSource=0
searchFieldvalue=0

db=DatabaseConnection()

# Code for login window
class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Loading .ui file
        uic.loadUi('UI/loginwindow.ui', self)

        # Get the database connection
        global db
        self.connection=db.get_connection()

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
            uid = login_user(self.connection, email, password)[0]
            self.w = MainWindow()
            self.w.show()
            self.close()  # Close the login window after successful login
        else:
            msg = QMessageBox()
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
        global db
        self.connection = db.get_connection()

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
        global db
        global uid
        self.connection = db.get_connection()
        self.uid = uid
        
        try:
            uic.loadUi('UI/deleteRecordWindow.ui', self)
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText(f"Error loading UI file: {e}")
            msg.exec_()
            return

        self.deleteRecordButton = self.findChild(QPushButton, "pushButton")
        self.recordTypeComboBox = self.findChild(QtWidgets.QComboBox, "comboBox")
        self.idField = self.findChild(QLineEdit, "lineEdit")

        if not all([self.deleteRecordButton, self.recordTypeComboBox, self.idField]):
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Required UI elements not found!")
            msg.exec_()
            return

        self.deleteRecordButton.clicked.connect(self.deleteRecord)

    def deleteRecord(self):
        try:
            record_id = self.idField.text().strip()
            if not record_id:
                self.show_error("Please enter a record ID.")
                return
                
            if not record_id.isdigit():
                self.show_error("ID must be a number.")
                return

            record_id = int(record_id)
            record_type = self.recordTypeComboBox.currentText()

            if not self.connection:
                self.show_error("Database connection lost.")
                return

            success = False
            if record_type == "Income":
                success = delete_income(self.connection, record_id, self.uid)
            elif record_type == "Expense":
                success = delete_expense(self.connection, record_id, self.uid)
            
            # Update the main window to refresh the totals
            if success:
                self.show_success()
                # Find and refresh the main window if it exists
                main_window = self.findMainWindow()
                if main_window:
                    main_window.reload_window()
            else:
                self.show_error(f"No {record_type.lower()} record found with ID {record_id}")

        except Exception as e:
            logging.error(f"Error in deleteRecord: {str(e)}")
            self.show_error(f"An error occurred: {str(e)}")

    def findMainWindow(self):
        """Find the main window instance to refresh it after deletion"""
        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, MainWindow):
                return widget
        return None

    def show_error(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)  # Changed to Warning instead of Critical
        msg.setWindowTitle("Notice")
        msg.setText(message)
        msg.exec_()

    def show_success(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Success")
        msg.setText("Record deleted successfully!")
        msg.exec_()
        self.close()
from PyQt5.QtCore import QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global uid
        global db
        self.connection = db.get_connection()

        # Loading .ui file
        uic.loadUi('UI/mainwindow.ui', self)

        self.searchField = self.findChild(QLineEdit, 'lineEdit')
        self.addEarningButton = self.findChild(QPushButton, "pushButton")
        self.totalSpendingValue = self.findChild(QLabel, "label_7")
        self.totalEarningValue = self.findChild(QLabel, "label_5")
        self.searchButton = self.findChild(QPushButton, "pushButton_4")
        self.deleteRecordButton = self.findChild(QPushButton, "pushButton_5")
        self.analytics = self.findChild(QPushButton, "pushButton_2")

        self.addEarningButton.clicked.connect(self.openAddEarningWindow)
        self.searchButton.clicked.connect(self.openSearchResults)
        self.deleteRecordButton.clicked.connect(self.openDeleteRecordPopup)
        self.analytics.clicked.connect(self.analyticsf)
        # Set up the timer to reload the window every 10 seconds (10000 ms)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.reload_window)  # Connect the timer's timeout signal to a function
        self.timer.start(5000)  # 10 seconds interval

        # Initial data load for the main window
        self.recordResult = view_recent_records(self.connection, uid)
        self.totalEarningValue.setText("₹"+str(self.recordResult[0]))
        self.totalSpendingValue.setText("₹"+str(self.recordResult[1]))

    def reload_window(self):
        """Reload the content or refresh the main window every 10 seconds."""
        # Here you can re-fetch the data and update the window
        self.recordResult = view_recent_records(self.connection, uid)
        self.totalEarningValue.setText("₹"+str(self.recordResult[0]))
        self.totalSpendingValue.setText("₹"+str(self.recordResult[1]))
        # You can also refresh or update other parts of the window if needed.

    def openDeleteRecordPopup(self):
        self.w = deleteRecordWindow()
        self.w.show()

    def analyticsf(self):
        analytics(self.connection, uid)

    def openAddEarningWindow(self):
        self.w = addEarningWindow()
        self.w.show()

    def openSearchResults(self):
        global searchFieldvalue
        searchFieldvalue = self.searchField.text()
        self.w = searchResult()
        self.w.show()


from PyQt5.QtGui import QFont

class searchResult(QMainWindow):
    def __init__(self):
        super().__init__()

        global uid
        global searchFieldvalue

        print(searchFieldvalue)

        uic.loadUi('UI/searchResult.ui', self)
        global db
        self.connection = db.get_connection()

        s = view_records(self.connection, uid, searchFieldvalue)
        # index 1 and 2 correspond to name and amount
        expenseLabel = self.findChild(QLabel, "label_3")
        incomeLabel = self.findChild(QLabel, "label_4")

        incometext = ""
        for i in s['INCOME_RECORDS']:
            incometext += f'ID:{i[0]} | {i[1]} | {i[2]}₹\n\n'

        expensetext = ""
        for i in s['EXPENSE_RECORDS']:
            expensetext += f'ID:{i[0]} | {i[1]} | {i[2]}₹\n\n'
        # Set bold and large font size
        font = QFont()
        font.setBold(True)
        font.setPointSize(14)  # Adjust the font size as needed

        expenseLabel.setText(expensetext)
        incomeLabel.setText(incometext)

        # Apply the font to the labels
        expenseLabel.setFont(font)
        incomeLabel.setFont(font)

from PyQt5.QtWidgets import QMainWindow, QCalendarWidget, QPushButton

class calenderWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load UI file
        uic.loadUi('UI/calenderWidget.ui', self)

        # Initialize UI elements
        self.calender = self.findChild(QCalendarWidget, 'calendarWidget')
        self.setDateButton = self.findChild(QPushButton, 'pushButton')

        # Connect the setDateButton to the setDate method
        self.setDateButton.clicked.connect(self.setDate)

    def setDate(self):
        global calenderWindowSource
        # Get the selected date
        self.selectedDate = self.calender.selectedDate().toString()

        # Sanitize the date
        sanitizedDate = self.dateSanitizer(self.selectedDate)

        if calenderWindowSource == 'addEarningWindow':
            self.addEarningWindow = addEarningWindow()
            self.addEarningWindow.dateButton.setText(sanitizedDate)
            self.addEarningWindow.show()
        else:
            self.addExpenseWindow = addExpenseWindow()
            self.addExpenseWindow.dateButton.setText(sanitizedDate)
            self.addExpenseWindow.show()

        self.close()  # Close the calendar widget after setting the date

    def dateSanitizer(self, dateText):
        """Sanitize date format from 'Day Month Date Year' to 'YYYY-MM-DD'"""
        months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
        dateList = dateText.split()  # Split the date into parts (e.g., Mon, Nov, 11, 2024)

        month = months[dateList[1]]  # Map month name to number
        day = int(dateList[2])  # Extract the day
        year = int(dateList[3])  # Extract the year

        # Format the date as 'YYYY-MM-DD'
        return f"{year}-{month:02d}-{day:02d}"


def dateSanitizer(self, dateText):
    """Sanitize date format from 'Day Month Date Year' to 'YYYY-MM-DD'"""
    months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    dateList = dateText.split()  # Split the date into parts (e.g., Mon, Nov, 11, 2024)

    month = months[dateList[1]]  # Map month name to number
    day = int(dateList[2])  # Extract the day
    year = int(dateList[3])  # Extract the year

    # Format the date as 'YYYY-MM-DD'
    return f"{year}-{month:02d}-{day:02d}"


def setDate(self):
    global calenderWindowSource
    # Day Month Date Year: Mon Nov 11 2024
    self.selectedDate = self.calender.selectedDate().toString()

    sanitizedDate = self.dateSanitizer(self.selectedDate)

    if calenderWindowSource == 'addEarningWindow':
        self.addEarningWindow = addEarningWindow()
        self.addEarningWindow.dateButton.setText(sanitizedDate)
        self.addEarningWindow.show()
    else:
        self.addExpenseWindow = addExpenseWindow()
        self.addExpenseWindow.dateButton.setText(sanitizedDate)
        self.addExpenseWindow.show()

    self.close()  # Close the calendar widget after setting the date


class addExpenseWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("UI/addExpenseWindow.ui", self)
        global db
        self.connection = db.get_connection()

        self.openEarningWindowButton = self.findChild(QPushButton, "pushButton_3")
        self.recurringExpenseCheckBox = self.findChild(QPushButton, "pushButton_5")
        self.addExpenseButton = self.findChild(QPushButton, "pushButton")

        self.amountField = self.findChild(QLineEdit, "lineEdit_2")
        self.expenseNameField = self.findChild(QLineEdit, "lineEdit_3")
        self.dateButton = self.findChild(QPushButton, "pushButton_2")
        self.descriptionField = self.findChild(QTextEdit, "textEdit")

        self.openEarningWindowButton.clicked.connect(self.openEarningWindow)
        self.recurringExpenseCheckBox.clicked.connect(self.changeState)
        self.addExpenseButton.clicked.connect(self.addExpense)
        self.dateButton.clicked.connect(self.openCalenderWindow)

    def openCalenderWindow(self):
        global calenderWindowSource

        calenderWindowSource = 'addExpenseWindow'
        self.close()  # Close the current window
        self.w = calenderWidget()  # Open the calendar window
        self.w.show()

    def openEarningWindow(self):
        self.close()  # Close current window before opening the new one
        self.w = addEarningWindow()
        self.w.show()

    def changeState(self):
        if self.recurringExpenseCheckBox.isChecked():
            self.recurringExpenseCheckBox.setStyleSheet(
                'QPushButton{background-color:rgb(61, 40, 224);border:2px solid;border-radius:7px;border-color:rgb(71, 71, 71);}')
            self.recurringExpenseCheckBox.setChecked(True)
        else:
            self.recurringExpenseCheckBox.setStyleSheet(
                'QPushButton{background-color:rgba(217, 217, 217,0);border:2px solid;border-radius:7px;border-color:rgb(71, 71, 71);}')
            self.recurringExpenseCheckBox.setChecked(False)

    def addExpense(self):
    # Retrieve user inputs
        expense_name = self.expenseNameField.text()
        amount = self.amountField.text()
        date = self.dateButton.text()
        description = self.descriptionField.toPlainText()

    # Check if all required fields are filled
        if not expense_name or not amount or not date:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Input Error")
            msg.setText("Please fill in all the required fields!")
            msg.exec_()
            return  # Exit the method if there is missing input

    # Proceed to add the expense if all fields are filled
        global uid
        add_expense(self.connection, expense_name, amount, date, description, uid, self.recurringExpenseCheckBox.isChecked())

        msg = QMessageBox()
        msg.setWindowTitle("Successful")
        msg.setText("Record added successfully.")
        msg.exec_()



class addEarningWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("UI/addEarningWindow.ui", self)
        global db
        self.connection = db.get_connection()

        self.openExpenseWindowButton = self.findChild(QPushButton, "pushButton_4")
        self.recurringEarningCheckBox = self.findChild(QPushButton, "pushButton_5")
        self.addEarningButton = self.findChild(QPushButton, "pushButton")

        self.earningNameField = self.findChild(QLineEdit, "lineEdit_3")
        self.amountField = self.findChild(QLineEdit, "lineEdit_2")
        self.dateButton = self.findChild(QPushButton, "pushButton_2")
        self.descriptionField = self.findChild(QTextEdit, "textEdit")

        self.openExpenseWindowButton.clicked.connect(self.openExpenseWindow)
        self.recurringEarningCheckBox.clicked.connect(self.changeState)
        self.addEarningButton.clicked.connect(self.addEarning)
        self.dateButton.clicked.connect(self.openCalenderWindow)

    def openCalenderWindow(self):
        global calenderWindowSource

        calenderWindowSource = 'addEarningWindow'
        self.close()  # Close the current window
        self.w = calenderWidget()  # Open the calendar window
        self.w.show()

    def addEarning(self):
    # Retrieve user inputs
        earning_name = self.earningNameField.text()
        amount = self.amountField.text()
        date = self.dateButton.text()
        description = self.descriptionField.toPlainText()

    # Check if all required fields are filled
        if not earning_name or not amount or not date:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Input Error")
            msg.setText("Please fill in all the required fields!")
            msg.exec_()
            return  # Exit the method if there is missing input

    # Proceed to add the earning if all fields are filled
        global uid
        add_income(self.connection, earning_name, amount, date, description, uid, self.recurringEarningCheckBox.isChecked())

        msg = QMessageBox()
        msg.setWindowTitle("Successful")
        msg.setText("Record added successfully.")
        msg.exec_()
    

    def openExpenseWindow(self):
        self.close()  # Close the current window before opening the expense window
        self.w = addExpenseWindow()
        self.w.show()

    def changeState(self):
        if self.recurringEarningCheckBox.isChecked():
            self.recurringEarningCheckBox.setStyleSheet(
                'QPushButton{background-color:rgb(61, 40, 224);border:2px solid;border-radius:7px;border-color:rgb(71, 71, 71);}')
            self.recurringEarningCheckBox.setChecked(True)
        else:
            self.recurringEarningCheckBox.setStyleSheet(
                'QPushButton{background-color:rgba(217, 217, 217,0);border:2px solid;border-radius:7px;border-color:rgb(71, 71, 71);}')
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

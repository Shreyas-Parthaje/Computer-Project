import sys
import backgroundimg
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit
from database_functions import login_user, register_user, DatabaseConnection

#QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
#QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

# Code for login window
class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()

        # Load .ui file
        uic.loadUi('loginwindow.ui', self)

        #declaring(identifying) widgets from .ui file
        self.loginButton = self.findChild(QPushButton, 'pushButton')
        self.registerWindowButton = self.findChild(QPushButton, "pushButton_4")
        self.emailField = self.findChild(QLineEdit, 'lineEdit_3')
        self.passwordField = self.findChild(QLineEdit, 'lineEdit_2')

        # Get the database connection
        self.connection = DatabaseConnection().get_connection()

        #Button click checking code
        self.registerWindowButton.clicked.connect(self.openRegisterWindow)
        self.loginButton.clicked.connect(self.login)

    def login(self):
        email = self.emailField.text()
        password = self.passwordField.text()
        
        if login_user(self.connection, email, password):
            print("Login successful!")
            # Redirect to another window or perform some action
        else:
            print("Login failed. Invalid username or password.")

#This function will be excecuted when registerWindowButton is clicked
    def openRegisterWindow(self):
        self.w = RegisterWindow()  # Pass the existing connection
        self.w.show()
        self.close()  # Close the login window

# Code for register window
class RegisterWindow(QMainWindow):
    def __init__(self):
        super(RegisterWindow, self).__init__()

        # Load .ui file
        uic.loadUi('registerwindow.ui', self)

        #declaring(identifying) widgets from .ui file
        self.registerButton = self.findChild(QPushButton, 'pushButton')
        self.loginWindowButton = self.findChild(QPushButton, "pushButton_3")
        self.emailField = self.findChild(QLineEdit, 'lineEdit')
        self.passwordField = self.findChild(QLineEdit, 'lineEdit_2')

        # Get the database connection
        self.connection = DatabaseConnection().get_connection()

        #Button click checking code
        self.registerButton.clicked.connect(self.register)
        self.loginWindowButton.clicked.connect(self.openLoginWindow)

    def register(self):
        email = self.emailField.text()
        password = self.passwordField.text()
        
        if email and password:  
            register_user(self.connection, email, password)
            print("Registration successful!")
        else:
            print("Please enter both email and password.")

    def openLoginWindow(self):
        self.w = LoginWindow()
        self.w.show()
        self.close()  # Close the register window

# App initialization
app = QApplication(sys.argv)

# Initialize the database connection
DatabaseConnection()

#Window initialisation
mainwindow = LoginWindow()

#Execution of window
mainwindow.show()

#Execution of app
app.exec_()

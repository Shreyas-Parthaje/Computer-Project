import mysql.connector

class DatabaseConnection:
    def __init__(self):
        self.connection = mysql.connector.connect(
            user= 'i7771355_e1zq1',
            password= '3u0NFC]{p~^#',
            host= '184.168.102.202',
            database= 'csproj',
        )

    def get_connection(self):
        return self.connection

'''
class DatabaseConnection:
    def __init__(self):
        self.connection = mysql.connector.connect(
            user= 'root',
            password= 'mysql',
            host= 'localhost',
            database= 'csproj',
        )

    def get_connection(self):
        return self.connection
'''


# Function to execute a query
def execute_query(connection, query, values=None):
    cursor = connection.cursor()
    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)
    connection.commit()
    print("Query executed successfully")

# Function to fetch results from a SELECT query
def fetch_results(connection, query, values=None):
    cursor = connection.cursor()
    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)
    return cursor.fetchall()

def register_user(connection, username, password):
    query = f"INSERT INTO Users (username, password) VALUES ('{username}', '{password}')"
    execute_query(connection, query)

def login_user(connection, username, password):
    query = f"SELECT * FROM Users WHERE username = '{username}' AND password = '{password}'"
    user = fetch_results(connection, query)
    return user[0] if user else None

# Expense-related functions
def add_expense(connection, expense_name, amount, expense_date, description, user_id, is_recurring):
    query = f"INSERT INTO Expenses (expense_name, amount, expense_date, description, user_id, is_recurring) VALUES ('{expense_name}', '{amount}', '{expense_date}', '{description}', {user_id}, {is_recurring})"
    execute_query(connection, query)


def delete_expense(connection, expense_id):
    query = f"DELETE FROM Expenses WHERE id = {expense_id}"
    execute_query(connection, query)


# Income-related functions
def add_income(connection, source, amount, income_date, description, user_id, is_recurring):
    query = f"INSERT INTO Income (source, amount, income_date, description, user_id, is_recurring) VALUES ('{source}', {amount}, '{income_date}', '{description}', {user_id}, {is_recurring})"
    execute_query(connection, query)


def delete_income(connection, income_id):
    query = f"DELETE FROM Income WHERE id = {income_id}"
    execute_query(connection, query)


# Record-related functions
def view_records(connection, user_id, date):
    query = f"SELECT * FROM Income WHERE user_id = {user_id} AND income_date = '{date}'"
    income_list = fetch_results(connection, query)
    query = f"SELECT * FROM Expenses WHERE user_id = {user_id} AND expense_date = '{date}'"
    expense_list = fetch_results(connection, query)
    return {'INCOME_RECORDS':income_list, 'EXPENSE_RECORDS':expense_list}


def view_recent_records(connection, user_id):
    query = f"SELECT SUM(amount) FROM Income WHERE user_id = {user_id} AND YEAR(income_date) = YEAR(CURDATE()) AND MONTH(income_date) = MONTH(CURDATE())"
    recent_income = fetch_results(connection, query)[0][0]
    query = f"SELECT SUM(amount) FROM Expenses WHERE user_id = {user_id} AND YEAR(expense_date) = YEAR(CURDATE()) AND MONTH(expense_date) = MONTH(CURDATE())"
    recent_expenses = fetch_results(connection, query)[0][0]
    recent_income = float(recent_income) if recent_income else 0.00
    recent_expenses = float(recent_expenses) if recent_expenses else 0.00
    return (recent_income, recent_expenses)


def delete_income(connection, user_id, date):
    query = f"DELETE FROM Income WHERE user_id = {user_id} AND income_date = '{date}'"
    execute_query(connection, query)
    query = f"DELETE FROM Expenses WHERE user_id = {user_id} AND expense_date = '{date}'"
    execute_query(connection, query)
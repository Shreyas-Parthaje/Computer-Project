import mysql.connector
# Function to connect to the MySQL database
def create_connection(host_name, user_name, user_password, db_name):
    connection = mysql.connector.connect(
        host=host_name,
        user=user_name,
        passwd=user_password,
        database=db_name
    )
    print("Connected to MySQL Database")
    return connection
import mysql.connector

class DatabaseConnection:
    def __init__(self):
        # Initialize the database connection
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="Csproj"
        )

    def get_connection(self):
        return self.connection

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

# Category-related functions
def create_category(connection, category_name, user_id):
    query = "INSERT INTO Categories (category_name, user_id) VALUES (%s, %s)"
    execute_query(connection, query, (category_name, user_id))

def get_categories(connection, user_id):
    query = "SELECT * FROM Categories WHERE user_id = %s"
    return fetch_results(connection, query, (user_id,))

# Expense-related functions
def add_expense(connection, category_id, amount, date, description, user_id):
    query = "INSERT INTO Expenses (category_id, amount, date, description, user_id) VALUES (%s, %s, %s, %s, %s)"
    execute_query(connection, query, (category_id, amount, date, description, user_id))

def view_expenses(connection, user_id):
    query = "SELECT * FROM Expenses WHERE user_id = %s"
    expenses = fetch_results(connection, query, (user_id,))
    for expense in expenses:
        print(f"ID: {expense[0]}, Category ID: {expense[1]}, Amount: {expense[2]}, Date: {expense[3]}, Description: {expense[4]}")

def delete_expense(connection, expense_id):
    query = "DELETE FROM Expenses WHERE id = %s"
    execute_query(connection, query, (expense_id,))

# Income-related functions
def add_income(connection, source, amount, date, description, user_id, is_recurring):
    query = "INSERT INTO Income (source, amount, date, description, user_id, is_recurring) VALUES (%s, %s, %s, %s, %s, %s)"
    execute_query(connection, query, (source, amount, date, description, user_id, is_recurring))

def view_income(connection, user_id):
    query = "SELECT * FROM Income WHERE user_id = %s"
    income_list = fetch_results(connection, query, (user_id,))
    for income in income_list:
        recurring_status = "Yes" if income[6] else "No"
        print(f"ID: {income[0]}, Source: {income[1]}, Amount: {income[2]}, Date: {income[3]}, Recurring: {recurring_status}")

def delete_income(connection, income_id):
    query = "DELETE FROM Income WHERE id = %s"
    execute_query(connection, query, (income_id,))

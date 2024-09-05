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
'''
# Category-related functions
def create_category(connection, category_name, user_id):
    query = f"INSERT INTO Categories (category_name, user_id) VALUES ('{category_name}', {user_id})"
    execute_query(connection, query)
    
def get_categories(connection, user_id):
    query = f"SELECT * FROM Categories WHERE user_id = {user_id}"
    return fetch_results(connection, query)'''

# Expense-related functions
def add_expense(connection, category_id, amount, expense_date, description, user_id):
    query = f"INSERT INTO Expenses (category_id, amount, expense_date, description, user_id) VALUES ({category_id}, {amount}, '{expense_date}', '{description}', {user_id})"
    execute_query(connection, query)

def view_expenses(connection, user_id):
    query = f"SELECT * FROM Expenses WHERE user_id = {user_id}"
    expenses = fetch_results(connection, query)
    for expense in expenses:
        print(f"ID: {expense[0]}, Category ID: {expense[1]}, Amount: {expense[2]}, Date: {expense[3]}, Description: {expense[4]}")

def view_recent_expenses(connection,user_id):
    query=f"SELECT * FROM Expense WHERE user_id = {user_id} ORDER BY Expense_date DESC"
    expense_list = fetch_results(connection, query)
    for expense in expense_list[:3]:
        print(f"ID: {expense[0]}, Source: {expense[1]}, Amount: {expense[2]}, Date: {expense[3]}, Recurring: {recurring_status}")

def delete_expense(connection, expense_id):
    query = f"DELETE FROM Expenses WHERE id = {expense_id}"
    execute_query(connection, query)


# Income-related functions
def add_income(connection, source, amount, income_date, description, user_id, is_recurring):
    query = f"INSERT INTO Income (source, amount, income_date, description, user_id, is_recurring) VALUES ('{source}', {amount}, '{income_date}', '{description}', {user_id}, {is_recurring})"
    execute_query(connection, query)

def view_income(connection, user_id):
    query = f"SELECT * FROM Income WHERE user_id = {user_id}"
    income_list = fetch_results(connection, query)
    for income in income_list:
        recurring_status = "Yes" if income[6] else "No"
        print(f"ID: {income[0]}, Source: {income[1]}, Amount: {income[2]}, Date: {income[3]}, Recurring: {recurring_status}")

def view_recent_income(connection,user_id):
    query=f"SELECT * FROM Income WHERE user_id = {user_id} ORDER BY Income_date DESC"
    income_list = fetch_results(connection, query)
    for income in income_list[:3]:
        print(f"ID: {income[0]}, Source: {income[1]}, Amount: {income[2]}, Date: {income[3]}, Recurring: {recurring_status}")

def delete_income(connection, income_id):
    query = f"DELETE FROM Income WHERE id = {income_id}"
    execute_query(connection, query)

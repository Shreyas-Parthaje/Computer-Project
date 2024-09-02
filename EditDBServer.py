import mysql.connector
from mysql.connector import errorcode

config = {
    'user': 'i7771355_e1zq1',
    'password': '3u0NFC]{p~^#',
    'host': '184.168.102.202',
    'database': 'csproj',
    'raise_on_warnings': True
}

table_creation_queries = [
    """
    CREATE TABLE Users (
        user_id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    );
    """,
    """
    CREATE TABLE Categories (
        category_id INT PRIMARY KEY AUTO_INCREMENT,
        category_name VARCHAR(255) NOT NULL,
        user_id INT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    );
    """,
    """
    CREATE TABLE Expenses (
        expense_id INT PRIMARY KEY AUTO_INCREMENT,
        category_id INT,
        amount DECIMAL(10, 2) NOT NULL,
        expense_date DATE NOT NULL,
        description VARCHAR(255),
        user_id INT,
        FOREIGN KEY (category_id) REFERENCES Categories(category_id),
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    );
    """,
    """
    CREATE TABLE Income (
        income_id INT PRIMARY KEY AUTO_INCREMENT,
        source VARCHAR(255) NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        income_date DATE NOT NULL,
        description VARCHAR(255),
        user_id INT,
        is_recurring BOOLEAN,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    );
    """
]

try:
    # Connect to the MySQL database
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Execute each SQL command to create tables
    for query in table_creation_queries:
        cursor.execute(query)
        print(f"Table created successfully: {query.split()[2]}")

    # Commit changes
    connection.commit()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
finally:
    # Close the cursor and connection
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()

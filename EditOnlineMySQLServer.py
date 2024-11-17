import mysql.connector
from mysql.connector import errorcode

# Database configuration
config = {
    'user': 'i7771355_e1zq1',
    'password': '3u0NFC]{p~^#',
    'host': '184.168.102.202',
    'database': 'csproj',
    'raise_on_warnings': True
}

def execute_sql_command(command):
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Execute the given SQL command
        cursor.execute(command)

        # If it's a SELECT or DESCRIBE type of query, fetch and print the results
        if command.strip().upper().startswith(('SELECT', 'DESCRIBE', 'SHOW')):
            result = cursor.fetchall()
            for row in result:
                print(row)
        else:
            # For other queries like CREATE, DROP, ALTER, etc., just commit the changes
            connection.commit()
            print(f"Query executed successfully: {command}")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print("MySQL error:", err)
    finally:
        # Ensure the result is fully processed before closing the cursor
        if 'cursor' in locals():
            cursor.fetchall()  # Ensure all results are read if necessary
            cursor.close()
        if 'connection' in locals():
            connection.close()

def main():
    while True:
        try:
            print("\nEnter your SQL command (e.g., SELECT, DESCRIBE, CREATE, etc.) or type 'exit' to quit:")
            user_command = input()  # Get user input
            
            if user_command.lower() == 'exit':  # Check for exit command
                print("Exiting...")
                break  # Exit the loop if 'exit' is typed
            
            # Try to execute the SQL command
            execute_sql_command(user_command)  # Execute the SQL command
        except Exception as e:
            print(f"An error occurred: {e}. Please try again.")

if __name__ == "__main__":
    main()

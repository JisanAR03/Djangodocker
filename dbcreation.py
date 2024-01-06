import mysql.connector
from mysql.connector import Error

def create_database(db_name):
    try:
        # Connect to the MySQL Server (add your connection parameters)
        connection = mysql.connector.connect(
            host='localhost', 
            user='root', 
            password=''
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print(f"Database '{db_name}' created successfully.")
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

# Name of the database you want to create
database_name = "artixcorejango"
create_database(database_name)

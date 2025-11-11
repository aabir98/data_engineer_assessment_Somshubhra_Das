import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "db_user",
    "password": "6equj5_db_user",
    "database": "home_db"
}

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        print(f"connected to db: {db_name[0]}")
        cursor.execute("SELECT VERSION();")
        version = cursor.fetchone()
        print(f"MySQL Version: {version[0]}")
        cursor.close()
        conn.close()
        print("connection closed successfully.")
except Error as e:
    print(f"Error: {e}")

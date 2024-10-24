import sqlite3

class DatabaseManager:
    def __init__(self):
        self.db_name = "database.db"


    # Connects to Database
    def connect(self):
        try:
            connection = sqlite3.connect(self.db_name)
            return connection
        except sqlite3.Error as e:
            raise Exception(f"Failed to connect to Database: {e}")
        
    
    # Gets All Data from Database
    def fetch_data(self):
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM accounts")
                return cursor.fetchall()
        except sqlite3.Error as e:
            raise Exception(f"Failed to Fetch Data: {e}")


    # Inserts New Account into Database
    def insert_account(self, data):
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS accounts (
                        id INTEGER PRIMARY KEY, 
                        email TEXT, username TEXT, 
                        password TEXT, 
                        application TEXT, 
                        opt_in INTEGER)
                """)
                cursor.execute("INSERT INTO accounts(id, email, username, password, application, opt_in) VALUES (?, ?, ?, ?, ?, ?)",
                            (None, *data))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Failed to Insert Account Into Database: {e}")


    # Updates Account Data in Database
    def update_account(self, account_id, data):
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                set_clause = ", ".join([f"{col} = ?" for col in ["email", "username", "password", "application"]])
                query = f"UPDATE accounts SET {set_clause}, opt_in = ? WHERE id = ?"
                cursor.execute(query, data + [account_id])
        except sqlite3.Error as e:
            raise Exception(f"Failed to Update Account: {e}")


    # Deletes Account from Database
    def delete_account(self, account_id):
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Failed to Delete Account From Database: {e}")


    # Deletes All Accounts 
    def delete_all(self):
        try:
            with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute("DROP TABLE IF EXISTS accounts")
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"Failed to Delete Database Table: {e}")
    
    
    # Checks for Data in Database
    def check_db_for_data(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('PRAGMA table_info(accounts)')
            data = cursor.fetchone()
            return data
import sqlite3

class DatabaseManager:
    """
    Handles all SQL interactions for the secured vault.
    Uses SQLite for a real SQL implementation that is portable and server-ready.
    """
    def __init__(self, db_name="vault.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """Creates the tables for storing Part A and User Credentials."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Table for the encrypted data
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS secured_vault (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    phone TEXT,
                    uid TEXT
                )
            ''')
            # Table for user authentication
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password_hash TEXT
                )
            ''')
            conn.commit()

    def store_record(self, name, phone, uid):
        """Inserts the transformed Part A sequences into the SQL database."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO secured_vault (name, phone, uid) VALUES (?, ?, ?)",
                (name, phone, uid)
            )
            conn.commit()

    def get_all_records(self):
        """Retrieves all encrypted sequences from the SQL database."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, phone, uid FROM secured_vault")
            return cursor.fetchall()

    def create_user(self, username, password_hash):
        """Creates a new user in the system."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, password_hash)
                )
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False # Username already exists

    def verify_user(self, username, password_hash):
        """Checks if the username and password hash match."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT password_hash FROM users WHERE username = ?",
                (username,)
            )
            result = cursor.fetchone()
            if result and result[0] == password_hash:
                return True
        return False

    def clear_vault(self):
        """Wipes the database for a fresh demo."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM secured_vault")
            cursor.execute("DELETE FROM users")
            conn.commit()

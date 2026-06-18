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
        """Creates the table for storing Part A (the weird sequences)."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS secured_vault (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    phone TEXT,
                    uid TEXT
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

    def clear_vault(self):
        """Wipes the database for a fresh demo."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM secured_vault")
            conn.commit()

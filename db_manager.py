import sqlite3

class DBManager:
    """
    Singleton-style Database Manager handling all SQL interactions.
    """
    def __init__(self, db_name="college_app.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Users Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT UNIQUE,
                password TEXT,
                role TEXT
            )
        ''')
        
        # Marketplace Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                price REAL,
                type TEXT,
                owner_id INTEGER,
                status TEXT
            )
        ''')

        # Projects Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                project_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                prof_id INTEGER
            )
        ''')
        
        # Applications Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                app_id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                student_id INTEGER,
                student_name TEXT,
                status TEXT
            )
        ''')
        
        self.conn.commit()

    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_all(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
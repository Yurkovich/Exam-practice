
import os
import sqlite3

class Database:
    def __init__(self, db_name='tasks.db'):
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', db_name)

    def create_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        create_table_query = '''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            datetime DATETIME NOT NULL,
            completed INTEGER NOT NULL
        );
        '''

        cursor.execute(create_table_query)

        conn.commit()
        conn.close()
        
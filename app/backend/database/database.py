
import os
import sqlite3

class Database:
    def __init__(self, db_name='tasks.db'):
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', db_name)

    def create_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Создание таблицы для задач
        create_task_table_query = '''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            datetime DATETIME NOT NULL,
            completed INTEGER NOT NULL
        );
        '''
        cursor.execute(create_task_table_query)


        create_user_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY
        );
        '''
        cursor.execute(create_user_table_query)

        conn.commit()
        conn.close()

    def add_user_chat_id(self, chat_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (chat_id) VALUES (?)", (chat_id,))
        conn.commit()
        conn.close()

    def get_all_user_chat_ids(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT chat_id FROM users")
        users = cursor.fetchall()
        conn.close()
        return [user[0] for user in users]
        
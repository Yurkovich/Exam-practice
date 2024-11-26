
from abc import ABC, abstractmethod
import sqlite3
from typing import Any, List

from database.database import Database
from model.task import TaskCreate, TaskRead, TaskUpdate


class Model(ABC):
    @staticmethod
    @abstractmethod
    async def all() -> List[Any]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def add(data: Any) -> None:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def update(data: Any) -> None:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def delete(entity_id: int) -> bool:
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    async def get_by_id(id: int) -> List[Any]:
        raise NotImplementedError
    

class Task(Model):
    def __init__(self, db: Database):
        self.db = db

    async def all(self) -> List[TaskRead]:
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()

        select_query = '''
        SELECT id, name, description, datetime, completed
        FROM tasks
        '''

        cursor.execute(select_query)
        rows = cursor.fetchall()
        conn.close()

        return [TaskRead(id=row[0], name=row[1], description=row[2], datetime=row[3], completed=row[4]) for row in rows]

    async def add(self, data: TaskCreate) -> TaskRead:
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()

        insert_query = '''
        INSERT INTO tasks (name, description, datetime, completed)
        VALUES (?, ?, ?, ?)
        '''

        cursor.execute(insert_query, (data.name, data.description, data.datetime, data.completed))
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()

        return TaskRead(id=task_id, name=data.name, description=data.description, datetime=data.datetime, completed=data.completed)

    async def update(self, data: TaskUpdate) -> TaskRead:
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()

        update_query = '''
        UPDATE tasks
        SET name = ?, description = ?, datetime = ?, completed = ?
        WHERE id = ?
        '''
        cursor.execute(update_query, (data.name, data.description, data.datetime, data.completed, data.id))
        conn.commit()
        if cursor.rowcount == 0:
            conn.close()
            return None
        conn.close()

        return TaskRead(id=data.id, name=data.name, description=data.description, datetime=data.datetime, completed=data.completed)

    async def delete(self, entity_id: int) -> bool:
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()

        delete_query = '''
        DELETE FROM tasks
        WHERE id = ?
        '''

        cursor.execute(delete_query, (entity_id,))
        conn.commit()
        conn.close()

        return True

    async def get_by_id(self, entity_id: int) -> TaskRead:
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()

        select_query = '''
        SELECT id, name, description, datetime, completed
        FROM tasks
        WHERE id = ?
        '''

        cursor.execute(select_query, (entity_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return TaskRead(id=row[0], name=row[1], description=row[2], datetime=row[3], completed=row[4])
        return None
    
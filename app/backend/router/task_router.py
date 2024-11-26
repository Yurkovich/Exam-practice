
from fastapi import HTTPException, APIRouter
from typing import List
from database.database import Database
from model.task import TaskCreate, TaskRead, TaskUpdate
from model.model import Task
import logging

from bot.start_bot import notify_new_task, notify_task_deleted, notify_task_update

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

db_manager = Database()
task = Task(db_manager)

task_router = APIRouter(tags=['Tasks'])


@task_router.post("/api/task", response_model=TaskRead)
async def create_task(task_data: TaskCreate):
    try:
        created_task = await task.add(task_data)
        if created_task is None:
            raise ValueError("Создание задачи - None")
        
        notify_new_task({
            "id": created_task.id,
            "name": created_task.name,
            "datetime": created_task.datetime,
            "description": created_task.description,
        })
        
        return created_task
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@task_router.get("/api/task", response_model=List[TaskRead])
async def get_tasks():
    try:
        tasks = await task.all()
        if tasks is None:
            raise ValueError("Список задач - None")
        return tasks
    except Exception as e:
        logger.error(f"Error getting tasks: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@task_router.get("/api/task/{task_id}", response_model=TaskRead)
async def get_task_by_id(task_id: int):
    try:
        task_data = await task.get_by_id(task_id)
        if task_data is None:
            raise HTTPException(status_code=404, detail="Задача не найдена!")
        return task_data
    except Exception as e:
        logger.error(f"Ошибка при получении задачи по ID: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@task_router.put("/api/task/{task_id}", response_model=TaskRead)
async def update_task(task_id: int, task_data: TaskUpdate):
    try:
        existing_task = await task.get_by_id(task_id)
        if not existing_task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        changes = []
        if task_data.name and task_data.name != existing_task.name:
            changes.append("name")
            existing_task.name = task_data.name
        if task_data.description and task_data.description != existing_task.description:
            changes.append("description")
            existing_task.description = task_data.description
        if task_data.datetime and task_data.datetime != existing_task.datetime:
            changes.append("datetime")
            existing_task.datetime = task_data.datetime
        if task_data.completed is not None and task_data.completed != existing_task.completed:
            changes.append("completed")
            existing_task.completed = task_data.completed

        updated_task = await task.update(existing_task)
        
        if "completed" in changes and updated_task.completed:
            notify_task_update({"id": updated_task.id, "name": updated_task.name}, "completed")
        elif changes:
            notify_task_update({
                "id": updated_task.id,
                "name": updated_task.name,
                "datetime": updated_task.datetime,
                "description": updated_task.description,
            })
        
        return updated_task
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@task_router.delete("/api/task/{task_id}", response_model=dict)
async def delete_task(task_id: int):
    try:
        result = await task.delete(task_id)
        
        if result:
            notify_task_deleted(task_id)
            return {"message": "Задача успешно удалена!"}
        else:
            raise HTTPException(status_code=404, detail="Задача не найдена")
    except Exception as e:
        logger.error(f"Error deleting task: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
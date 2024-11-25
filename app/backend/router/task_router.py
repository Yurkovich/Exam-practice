
from fastapi import HTTPException, APIRouter
from typing import List
from database.database import Database
from model.task import TaskCreate, TaskRead, TaskUpdate
from model.model import Task
import logging

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
        task_data.id = task_id
        updated_task = await task.update(task_data)
        if updated_task is None:
            raise ValueError("Обновляемая задача - None")
        return updated_task
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@task_router.delete("/api/task/{task_id}", response_model=dict)
async def delete_task(task_id: int):
    try:
        result = await task.delete(task_id)
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Задача успешно удалена!"}
    except Exception as e:
        logger.error(f"Error deleting task: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
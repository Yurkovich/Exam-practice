
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from database.database import Database
from url.url import url_router
from router.task_router import task_router


templates = Jinja2Templates(directory="frontend/templates")
app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.include_router(url_router)
app.include_router(task_router)


if __name__ == '__main__':
    db_manager = Database()
    db_manager.create_database()
    uvicorn.run('main:app', reload=True, port=8000)
    
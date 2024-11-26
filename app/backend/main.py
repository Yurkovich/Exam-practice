
import threading
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from bot.start_bot import bot, check_deadlines
from database.database import Database
from url.url import url_router
from router.task_router import task_router


templates = Jinja2Templates(directory="frontend/templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.include_router(url_router)
app.include_router(task_router)


def start_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    db_manager = Database()
    db_manager.create_database()

    bot_thread = threading.Thread(target=start_bot)
    bot_thread.start()

    deadline_thread = threading.Thread(target=check_deadlines)
    deadline_thread.daemon = True
    deadline_thread.start()

    uvicorn.run('main:app', reload=True, port=8000)
    
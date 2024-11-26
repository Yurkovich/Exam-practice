
from datetime import datetime, timedelta
import time
import telebot
from dotenv import load_dotenv
import os
from database.database import Database


dotenv_path = os.path.join(os.path.dirname(__file__), '../token.env')
load_dotenv(dotenv_path=dotenv_path)


API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)
db = Database()
notified_task_ids = set()


def parse_datetime(datetime_str):
    if isinstance(datetime_str, datetime):
        return datetime_str
    
    try:
        return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            raise ValueError(f"Невозможно распарсить дату: {datetime_str}")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    db.add_user_chat_id(chat_id)
    
    welcome_text = (
        "👋 Привет! Я бот проекта управления задачами.\n\n"
        "📌 Проект: Веб-приложение для управления задачами.\n"
        "🔧 Возможности:\n"
        "- Добавление, изменение и выполнение задач.\n"
        "- Удобный интерфейс для управления.\n"
        "- Уведомления о новых и измененных задачах прямо здесь!\n\n"
        "Я буду уведомлять вас о важных событиях. 😊"
    )
    
    bot.send_message(chat_id, welcome_text, parse_mode='Markdown')


def notify_all_users(message_text):
    user_chat_ids = db.get_all_user_chat_ids()
    for chat_id in user_chat_ids:
        try:
            bot.send_message(chat_id, message_text)
        except Exception as e:
            print(f"Error sending message to {chat_id}: {e}")


def notify_new_task(task):
    task_deadline = parse_datetime(task['datetime'])
    now = datetime.now()

    time_left = task_deadline - now

    if time_left.days > 0:
        time_left_str = f"{time_left.days} дней {time_left.seconds // 3600} часов"
    elif time_left.seconds > 3600:
        time_left_str = f"{time_left.seconds // 3600} часов { (time_left.seconds // 60) % 60 } минут"
    else:
        time_left_str = f"{(time_left.seconds // 60)} минут"

    message = (
        f"✨ ** Новая задача добавлена! **\n"
        f"🆔 [ ID ] : {task['id']}\n"
        f"📌 [ Название ] : {task['name']}\n"
        f"🕒 [ Дедлайн ] : {task['datetime']}\n"
        f"⏳ [ Осталось времени до дедлайна ] : {time_left_str}\n"
        f"📝 [ Описание ] : {task['description']}\n"
    )
    notify_all_users(message)


def notify_task_update(task, update_type="updated"):
    if update_type == "completed":
        message = (
            f"✅ ** Задача выполнена! **\n"
            f"🆔 [ ID ] : {task['id']}\n"
            f"📌 [ Название ] : {task['name']}\n"
            f"\n"
            f"Отличная работа! 🎉\n"
            f"Вы успешно завершили задачу! 🥳\n"
            f"Потрясающе! Продолжайте в том же духе! 💪\n\n"
            f"Не забывайте добавлять новые задачи, чтобы поддерживать свой прогресс! 🚀"
        )
    else:
        message = (
            f"✏️ ** Задача обновлена! **\n"
            f"🆔 [ ID ] : {task['id']}\n"
            f"📌 [ Название ] : {task['name']}\n"
            f"🕒 [ Новый дедлайн ] : {task['datetime']}\n"
            f"📝 [ Новое описание ] : {task['description']}\n"
        )
    notify_all_users(message)


def notify_task_deleted(task_id):
    message = (
        f"❌ ** Задача удалена! **\n"
        f"🆔 [ ID ]: {task_id}\n"
    )
    notify_all_users(message)


def send_deadline_notification(task):
    message = (
        f"⏳ ** Через 5 минут истечет дедлайн задачи! **\n"
        f"🆔 [ ID ]: {task['id']}\n"
        f"📌 [ Название ]: {task['name']}\n"
        f"🕒 [ Дедлайн ]: {task['datetime']}\n"
        f"📝 [ Описание ]: {task['description']}\n"
        f"⚠️ Не забудьте выполнить задачу вовремя!"
    )
    notify_all_users(message)

def check_deadlines():
    while True:
        now = datetime.now()
        time_to_check = now + timedelta(minutes=5)
        tasks = db.get_tasks_from_db()

        for task in tasks:
            task_deadline = parse_datetime(task['datetime'])
            
            if task['id'] in notified_task_ids:
                continue

            if task_deadline <= time_to_check and task_deadline > now and not task['completed']:
                send_deadline_notification(task)
                notified_task_ids.add(task['id'])

        time.sleep(60)

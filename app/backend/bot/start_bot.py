
import telebot

from database.database import Database

API_TOKEN = "7654705071:AAFQfZTVd6P0NXL_kOMLvk_Ll_a9q9FfkwM"
NOTIFY_CHAT_ID = "819237494"

bot = telebot.TeleBot(API_TOKEN)
db = Database()


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
    message = (
        f"✨ ** Новая задача добавлена! **\n"
        f"🆔 [ ID ] : {task['id']}\n"
        f"📌 [ Название ] : {task['name']}\n"
        f"🕒 [ Дедлайн ] : {task['datetime']}\n"
        f"📝 [ Описание ] : {task['description']}\n"
    )
    notify_all_users(message)

def notify_task_update(task, update_type="updated"):
    if update_type == "completed":
        message = (
            f"✅ ** Задача выполнена! **\n"
            f"🆔 [ ID ] : {task['id']}\n"
            f"📌 [ Название ] : {task['name']}\n"
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

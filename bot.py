import telebot
from config import *
from telebot.types import Message

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# Команда /start
@bot.message_handler(commands=["start"])
def send_welcome(message: Message):
    bot.send_message(
        message.chat.id,
        "👋 Привет! Я эхо-бот.\nОтправь мне любое сообщение — и я его повторю.\nПопробуй /info или /help"
    )

# Команда /info
@bot.message_handler(commands=["info"])
def send_info(message: Message):
    user = message.from_user
    chat = message.chat
    bot.send_message(
        chat.id,
        f"ℹ️ <b>Информация о пользователе:</b>\n"
        f"👤 Имя: {user.first_name} {user.last_name or ''}\n"
        f"🆔 ID: {user.id}\n"
        f"💬 Тип чата: {chat.type}\n"
    )

# Команда /help
@bot.message_handler(commands=["help"])
def send_help(message: Message):
    bot.send_message(
        message.chat.id,
        "🛠 <b>Доступные команды:</b>\n"
        "/start — запуск бота\n"
        "/info — информация о тебе\n"
        "/help — список команд\n"
        "Или просто напиши что-нибудь, я повторю!"
    )

# Ответ на стикеры
@bot.message_handler(content_types=["sticker"])
def handle_sticker(message: Message):
    bot.send_sticker(message.chat.id, message.sticker.file_id)
    bot.send_message(message.chat.id, "🥸 Стикер принят. И возвращён!")

# Приветствие новых участников
@bot.message_handler(content_types=["new_chat_members"])
def greet_new_user(message: Message):
    for new_user in message.new_chat_members:
        bot.send_message(
            message.chat.id,
            f"👋 Добро пожаловать, {new_user.first_name}!\nРады видеть тебя здесь."
        )
        try:
            bot.approve_chat_join_request(message.chat.id, new_user.id)
        except Exception as e:
            print(f"Не удалось одобрить запрос на вступление: {e}")

# Эхо-сообщения
@bot.message_handler(func=lambda message: True)
def copy_message(message: Message):
    if message.from_user.id == bot.get_me().id:
        return
    bot.copy_message(
        chat_id=message.chat.id,
        from_chat_id=message.chat.id,
        message_id=message.message_id
    )

bot.infinity_polling()

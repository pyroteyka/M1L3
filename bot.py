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

# Ответ на стикеры (почему бы и нет?)
@bot.message_handler(content_types=["sticker"])
def handle_sticker(message: Message):
    bot.send_sticker(message.chat.id, message.sticker.file_id)
    bot.send_message(message.chat.id, "🥸 Стикер принят. И возвращён!")

# Эхо-сообщения (игнорируем сообщения самого бота)
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

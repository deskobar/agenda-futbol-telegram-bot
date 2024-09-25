from functools import wraps
from telebot.types import Message
from bot import bot
from bot.answers import WAKING_UP


def db_waking_up(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            message: Message = args[0]
            chat_id = message.chat.id
            message = await bot.reply_to(message, WAKING_UP)
            result = await func(*args, **kwargs)
            await bot.delete_message(chat_id, message.message_id)
            return result
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    return wrapper
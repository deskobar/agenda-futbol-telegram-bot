from functools import wraps
from telebot.types import Message
from bot import bot
from bot.answers import WAKING_UP

# Async decorator
def db_waking_up(func):
    @wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        try:
            chat_id = message.chat.id
            message = await bot.reply_to(message, WAKING_UP)
            result = await func(message, *args, **kwargs)
            bot.delete_message(chat_id, message.message_id)
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            print("After the function call")

    return wrapper

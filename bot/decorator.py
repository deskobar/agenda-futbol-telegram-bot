from functools import wraps
from telebot.types import Message
from bot import bot
from bot.answers import SOMETHING_HAPPENED, WAKING_UP


def waking_up(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        chat_id = None
        try:
            message: Message = args[0]
            chat_id = message.chat.id
            message = await bot.reply_to(message, WAKING_UP)
            await bot.send_chat_action(chat_id, "typing", timeout=30)
            result = await func(*args, **kwargs)
            await bot.delete_message(chat_id, message.message_id)
            return result
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            message = await bot.send_message(chat_id, SOMETHING_HAPPENED)

    return wrapper

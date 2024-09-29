from functools import wraps
from telebot.types import Message
from bot import bot
from bot.answers import SOMETHING_HAPPENED, WAKING_UP
import logging


def waking_up(func):
    @wraps(func)
    async def wrapper(incoming_message: Message, *args, **kwargs):
        chat_id = None
        try:
            chat_id = incoming_message.chat.id
            message = await bot.reply_to(incoming_message, WAKING_UP)
            await bot.send_chat_action(chat_id, "typing", timeout=30)
            result = await func(incoming_message, *args, **kwargs)
            await bot.delete_message(chat_id, message.message_id)
            return result
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            await bot.send_message(chat_id, SOMETHING_HAPPENED)

    return wrapper

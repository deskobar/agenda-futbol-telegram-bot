import logging

from telebot.async_telebot import AsyncTeleBot

from settings import TELEGRAM_TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

bot = AsyncTeleBot(TELEGRAM_TOKEN, allow_sending_without_reply=True)

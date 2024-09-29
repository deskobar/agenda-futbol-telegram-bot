import pandas as pd
from telebot.types import Message, InputFile
from bot import bot

import io
import dataframe_image as dfi

from bot.answers import GENERATING_IMAGE, SENDING_IMAGE


def df_to_image(df: pd.DataFrame) -> io.BytesIO:
    """Converts a DataFrame into an image and returns it as a BytesIO stream."""
    tmp = io.BytesIO()
    dfi.export(df, tmp, max_rows=-1)
    tmp.seek(0)
    return tmp


async def send_img_or_msg_if_no_content(
        message: Message, df: pd.DataFrame, msg: str, value: str
) -> Message:
    chat_id = message.chat.id
    if df.empty is True:
        message_sent: Message = await bot.reply_to(message, msg.format(value))
    else:
        generating_msg = await bot.send_message(chat_id, GENERATING_IMAGE)
        img = df_to_image(df)
        await bot.delete_message(chat_id, generating_msg.message_id)
        sending_img = await bot.send_message(chat_id, SENDING_IMAGE)
        message_sent: Message = await bot.send_photo(chat_id, InputFile(img))
        await bot.delete_message(chat_id, sending_img.message_id)
    return message_sent

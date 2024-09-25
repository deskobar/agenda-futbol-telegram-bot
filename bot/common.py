import io

import dataframe_image as dfi
import pandas as pd
from telebot.types import Message

async def send_img_or_msg_if_no_content(message: Message, df: pd.DataFrame, msg: str, value: str) -> Message:
    from bot import bot
    chat_id = message.chat.id
    if df.empty is True:
        message_sent: Message = await bot.reply_to(message, msg.format(value))
    else:
        with io.BytesIO() as tmp:
            dfi.export(df, tmp, table_conversion=None, max_rows=-1)
            tmp.seek(0)
            message_sent: Message = await bot.send_photo(chat_id, tmp)
    return message_sent

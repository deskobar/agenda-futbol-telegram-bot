import dataframe_image as dfi
import io
import base64
from PIL import Image
import pandas as pd


async def send_img_or_msg_if_no_content(message, df: pd.DataFrame, msg: str, value: str):
    from bot import bot
    chat_id = message.chat.id
    if df.index.empty is False:
        with io.BytesIO() as tmp:
            dfi.export(df, tmp, table_conversion=None, max_rows=-1)
            tmp.seek(0)
            await bot.send_photo(chat_id, tmp)
    else:
        await bot.reply_to(message, msg.format(value))

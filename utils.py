import dataframe_image as dfi
import io

import pandas as pd
from telegram import Update


async def send_img_or_msg_if_no_content(update: Update, df: pd.DataFrame, msg: str, value: str):
    """
    Send an img of the dataframe content if it has it, an informative msg otherwise
    :param update: A Telegram Bot Updater
    :param df: A Pandas DataFrame
    :param msg: A String
    :param value: A String
    :return: None
    """
    if df.index.empty is False:
        with io.BytesIO() as tmp:
            dfi.export(df, tmp, table_conversion=None, max_rows=-1)
            tmp.seek(0)
            await update.message.reply_photo(tmp)
    else:
        await update.message.reply_text(msg.format(value))

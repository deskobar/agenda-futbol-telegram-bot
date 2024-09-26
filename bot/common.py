import io

import pandas as pd
from telebot.types import Message
import matplotlib.pyplot as plt


def df_to_image(df: pd.DataFrame) -> io.BytesIO:
    n_rows, n_cols = df.shape
    figure_size = (n_cols * 2, n_rows * 0.5)

    _, ax = plt.subplots(figsize=figure_size)
    ax.axis("tight")
    ax.axis("off")
    ax.table(cellText=df.values, colLabels=df.columns, cellLoc="center", loc="center")

    with io.BytesIO() as buffer:
        plt.savefig(buffer, format="png", bbox_inches="tight", pad_inches=0.1, dpi=300)
        buffer.seek(0)
        return buffer


async def send_img_or_msg_if_no_content(
    message: Message, df: pd.DataFrame, msg: str, value: str
) -> Message:
    from bot import bot

    chat_id = message.chat.id
    if df.empty is True:
        message_sent: Message = await bot.reply_to(message, msg.format(value))
    else:
        img = df_to_image(df)
        message_sent: Message = await bot.send_photo(chat_id, img)
    return message_sent

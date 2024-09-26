import pandas as pd
from telebot.types import Message, InputFile
import matplotlib.pyplot as plt
from bot import bot

import io
from PIL import Image
import uuid

from settings import DPI


def df_to_image(df: pd.DataFrame) -> io.BytesIO:
    plt.ioff()
    fig = plt.figure(figsize=(df.shape[1] * 2, df.shape[0] * 0.5), num=uuid.uuid4().hex)
    ax = fig.gca()
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    table.scale(1, 1.5)

    image_stream = io.BytesIO()
    fig.savefig(image_stream, format='png', bbox_inches='tight', dpi=DPI, transparent=True)
    image_stream.seek(0)

    with Image.open(image_stream) as image:
        image.save(image_stream, format='PNG', optimize=True)

    image_stream.seek(0)
    plt.close(fig)
    return image_stream


async def send_img_or_msg_if_no_content(
        message: Message, df: pd.DataFrame, msg: str, value: str
) -> Message:
    chat_id = message.chat.id
    if df.empty is True:
        message_sent: Message = await bot.reply_to(message, msg.format(value))
    else:
        img = df_to_image(df)
        message_sent: Message = await bot.send_photo(chat_id, InputFile(img))
    return message_sent

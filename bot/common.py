import pandas as pd
from telebot.types import Message, InputFile
import matplotlib.pyplot as plt
from bot import bot

from io import BytesIO
from PIL import Image


def df_to_image(df: pd.DataFrame, dpi: int = 300) -> BytesIO:
    image_stream = BytesIO()
    fig, ax = plt.subplots(figsize=(df.shape[1] * 2, df.shape[0] * 0.5))  # Adjust size based on DataFrame shape
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    table.scale(1, 1.5)
    plt.savefig(image_stream, format='png', bbox_inches='tight', dpi=dpi, transparent=True)
    plt.close(fig)
    image_stream.seek(0)
    with Image.open(image_stream) as image:
        optimized_stream = BytesIO()
        image.save(optimized_stream, format='PNG', optimize=True)
    optimized_stream.seek(0)
    return optimized_stream


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

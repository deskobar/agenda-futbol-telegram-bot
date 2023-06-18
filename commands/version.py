from answers import VERSION


async def version(update, context):
    """
    Send a message when the command /version is issued.
    """
    await update.message.reply_text(VERSION)

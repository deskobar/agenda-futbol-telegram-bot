from answers import HOW_TO_USAGE


async def start(update, _context):
    """
    Send a message when the command /start is issued.
    """
    await update.message.reply_text(HOW_TO_USAGE)

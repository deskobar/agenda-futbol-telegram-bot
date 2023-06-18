from answers import HOW_TO_USAGE


async def help(update, _context):
    """
    Send a message when the command /help is issued.
    """
    await update.message.reply_text(HOW_TO_USAGE)

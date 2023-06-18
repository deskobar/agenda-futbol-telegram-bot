import pandas as pd
from client.queries import events_per_date
from client.graphql import client

from answers import DATE_WITHOUT_ARGS, DATE_WITH_NO_COINCIDENCES
from utils import send_img_or_msg_if_no_content


async def date(update, context):
    """
    Send all the events for a given string date
    """
    if len(context.args) != 1:
        await update.message.reply_text(DATE_WITHOUT_ARGS)
    else:
        date = context.args[0]
        result = await client.execute_async(events_per_date, variable_values={"date": date})
        events_result = result['eventsPerDate']
        events_df = pd.DataFrame(events_result)
        await send_img_or_msg_if_no_content(update, events_df, DATE_WITH_NO_COINCIDENCES, date)

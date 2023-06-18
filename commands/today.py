from datetime import datetime

import pandas as pd
import pytz
from client.queries import events_per_date
from client.graphql import client

from answers import DATE_WITH_NO_COINCIDENCES
from utils import send_img_or_msg_if_no_content


async def today(update, _context):
    """
    Send all the events of the current day
    """
    date = datetime.now(pytz.timezone('America/Santiago')).strftime('%Y-%m-%d')
    result = await client.execute_async(events_per_date, variable_values={"date": date})
    events_result = result['eventsPerDate']
    events_df = pd.DataFrame(events_result)
    await send_img_or_msg_if_no_content(update, events_df, DATE_WITH_NO_COINCIDENCES, 'hoy')

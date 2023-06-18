import pandas as pd
from client.queries import events
from client.graphql import client

from answers import ALL_WITH_NO_COINCIDENCES
from utils import send_img_or_msg_if_no_content


async def all(update, _context):
    """
    Return all the events available
    """
    result = await client.execute_async(events)
    events_result = result['events']
    events_df = pd.DataFrame(events_result)
    await send_img_or_msg_if_no_content(update, events_df, ALL_WITH_NO_COINCIDENCES, 'uwu')

import logging

from settings import TELEGRAM_TOKEN
from telebot.async_telebot import AsyncTeleBot

from client.queries import (
    events,
    events_substring,
    events_per_date,
    set_alias as set_alias_mutation,
)

from answers import (
    ALL_WITH_NO_COINCIDENCES,
    HOW_TO_USAGE,
    DATE_WITHOUT_ARGS,
    ALIAS_ADDED_SUCCESSFULLY,
    ALIAS_WITHOUT_ARGS,
    DATE_WITH_NO_COINCIDENCES,
    VERSION,
    WHEN_WITHOUT_ARGS,
    WHEN_WITH_NO_COINCIDENCES, INVALID_COMMAND
)

from datetime import datetime

import pytz

import pandas as pd

from client.graphql import client

from utils import send_img_or_msg_if_no_content

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

bot = AsyncTeleBot(TELEGRAM_TOKEN, allow_sending_without_reply=True)


@bot.message_handler(commands=['todo'])
async def cmd_all_events(message):
    """
    Return all the events available
    """
    result = await client.execute_async(events)
    events_result = result['events']
    events_df = pd.DataFrame(events_result)
    await send_img_or_msg_if_no_content(message, events_df, ALL_WITH_NO_COINCIDENCES, 'uwu')


@bot.message_handler(commands=['fecha'])
async def cmd_date(message):
    """
    Send all the events for a given string date
    """
    # print(message)
    [_command, *body] = message.text.split(' ')
    if len(body) != 1:
        await bot.reply_to(message, DATE_WITHOUT_ARGS)
    else:
        date = body[0]
        result = await client.execute_async(events_per_date, variable_values={"date": date})
        events_result = result['eventsPerDate']
        events_df = pd.DataFrame(events_result)
        await send_img_or_msg_if_no_content(message, events_df, DATE_WITH_NO_COINCIDENCES, date)


@bot.message_handler(commands=['help', 'start'])
async def cmd_help(message):
    """
    Send a message when the command /help is issued.
    """
    await bot.reply_to(message, HOW_TO_USAGE)


@bot.message_handler(commands=['set_alias'])
async def set_alias(message):
    """
    Set alias to specific team for a given user
    """
    [_command, *body] = message.text.split(' ')
    if len(body) < 2:
        await bot.reply_to(message, ALIAS_WITHOUT_ARGS)
    else:
        user_id = message.chat.id
        [*team_name, alias] = body
        await client.execute_async(
            set_alias_mutation,
            variable_values={
                "userId": str(user_id),
                "teamName": " ".join(team_name).lower(),
                "alias": alias
            }
        )
        await bot.reply_to(message, ALIAS_ADDED_SUCCESSFULLY)


@bot.message_handler(commands=['hoy'])
async def today(message):
    """
    Send all the events of the current day
    """
    date = datetime.now(pytz.timezone('America/Santiago')).strftime('%Y-%m-%d')
    result = await client.execute_async(events_per_date, variable_values={"date": date})
    events_result = result['eventsPerDate']
    events_df = pd.DataFrame(events_result)
    await send_img_or_msg_if_no_content(message, events_df, DATE_WITH_NO_COINCIDENCES, 'hoy')


@bot.message_handler(commands=['version'])
async def version(message):
    """
    Send a message when the command /version is issued.
    """
    await bot.reply_to(message, VERSION)


@bot.message_handler(commands=['cuando'])
async def when(message):
    """
    Given all the events that contains a substring given in their columns
    """
    [_command, *body] = message.text.split(' ')
    if len(body) == 0:
        await bot.reply_to(message, WHEN_WITHOUT_ARGS)
    else:
        user_id = message.chat.id
        substring = " ".join(body)
        result = await client.execute_async(
            events_substring,
            variable_values={
                "text": substring,
                "userId": str(user_id)
            }
        )
        events_result = result['eventsMatchText']
        events_df = pd.DataFrame(events_result)
        await send_img_or_msg_if_no_content(message, events_df, WHEN_WITH_NO_COINCIDENCES, substring)


@bot.message_handler(func=lambda message: True)
def invalid_cmd(message):
    bot.reply_to(message, INVALID_COMMAND)

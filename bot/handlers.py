from datetime import datetime

import pandas as pd
import pytz

from bot.answers import (
    ALL_WITH_NO_COINCIDENCES,
    HOW_TO_USAGE,
    DATE_WITHOUT_ARGS,
    ALIAS_ADDED_SUCCESSFULLY,
    ALIAS_WITHOUT_ARGS,
    DATE_WITH_NO_COINCIDENCES,
    VERSION,
    WHEN_WITHOUT_ARGS,
    WHEN_WITH_NO_COINCIDENCES,
    INVALID_COMMAND
)
from bot.client import bot
from bot.common import send_img_or_msg_if_no_content
from bot.decorator import db_waking_up
from gql_client.graphql import client
from gql_client.queries import (
    events,
    events_substring,
    events_per_date,
    set_alias as set_alias_mutation,
)
from telebot.types import Message


@bot.message_handler(commands=['todo'])
@db_waking_up
async def cmd_all_events(message: Message):
    """
    Return all the events available
    """
    result = await client.execute_async(events)
    events_result = result['events']
    events_df = pd.DataFrame(events_result)
    await send_img_or_msg_if_no_content(message, events_df, ALL_WITH_NO_COINCIDENCES, 'uwu')


@bot.message_handler(commands=['fecha'])
@db_waking_up
async def cmd_date(message: Message):
    """
    Send all the events for a given string date
    """
    [_command, *body] = message.text.split(' ')
    if len(body) != 1:
        await bot.reply_to(message, DATE_WITHOUT_ARGS)
        return
    date = body[0]
    result = await client.execute_async(events_per_date, variable_values={"date": date})
    events_result = result['eventsPerDate']
    events_df = pd.DataFrame(events_result)
    await send_img_or_msg_if_no_content(message, events_df, DATE_WITH_NO_COINCIDENCES, date)


@bot.message_handler(commands=['help', 'start'])
@db_waking_up
async def cmd_help(message: Message):
    """
    Send a message when the command /help is issued.
    """
    await bot.reply_to(message, HOW_TO_USAGE)


@bot.message_handler(commands=['set_alias'])
@db_waking_up
async def cmd_set_alias(message: Message):
    """
    Set alias to specific team for a given user
    """
    [_command, *body] = message.text.split(' ')
    if len(body) < 2:
        await bot.reply_to(message, ALIAS_WITHOUT_ARGS)
        return
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
@db_waking_up
async def cmd_today(message: Message):
    """
    Send all the events of the current day
    """
    date = datetime.now(pytz.timezone('America/Santiago')).strftime('%Y-%m-%d')
    result = await client.execute_async(events_per_date, variable_values={"date": date})
    events_result = result['eventsPerDate']
    events_df = pd.DataFrame(events_result)
    await send_img_or_msg_if_no_content(message, events_df, DATE_WITH_NO_COINCIDENCES, 'hoy')


@bot.message_handler(commands=['version'])
async def cmd_version(message: Message):
    """
    Send a message when the command /version is issued.
    """
    await bot.reply_to(message, VERSION)


@bot.message_handler(commands=['cuando'])
@db_waking_up
async def cmd_when(message: Message):
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
async def invalid_cmd(message: Message):
    """Default handler for every other text"""
    await bot.reply_to(message, INVALID_COMMAND)

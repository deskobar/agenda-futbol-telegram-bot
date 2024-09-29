import aiohttp
import telebot
from fastapi import FastAPI, Request
from pyngrok import ngrok

from bot import bot
from settings import PUBLIC_URL, TELEGRAM_TOKEN
from contextlib import asynccontextmanager
import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook?url={PUBLIC_URL}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as r:
            logging.info("Webhook set with status %s", r.status)
            app.state.webhook_set = True
    yield
    try:
        ngrok.kill()
    except Exception:  # noqa
        pass


app = FastAPI(lifespan=lifespan)


@app.post("/")
async def handler(request: Request):
    content = await request.json()
    update = telebot.types.Update.de_json(content)
    await bot.process_new_updates([update])
    return {"msg": "ok"}

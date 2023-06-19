import requests
import telebot
from fastapi import FastAPI, Request
from pyngrok import ngrok

from bot import bot
from settings import PUBLIC_URL, TELEGRAM_TOKEN

app = FastAPI()


@app.post('/')
async def handler(request: Request):
    content = await request.json()
    update = telebot.types.Update.de_json(content)
    await bot.process_new_updates([update])
    return {"msg": "ok"}


@app.on_event("startup")
async def on_startup():
    base_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook?url={PUBLIC_URL}"
    requests.post(base_url)


@app.on_event("shutdown")
async def on_shutdown():
    ngrok.kill()

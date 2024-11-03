import telebot
from fastapi import FastAPI, Request

from bot import bot
from settings import PUBLIC_URL
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(PUBLIC_URL)
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/")
async def handler(request: Request):
    content = await request.json()
    update = telebot.types.Update.de_json(content)
    await bot.process_new_updates([update])
    return {"msg": "ok"}

@app.get("/")
async def get_handler(request: Request):
    return {"msg": "ok"}

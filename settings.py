from decouple import config

from helpers import get_public_url

API_URL = config("API_URL")
TELEGRAM_TOKEN = config("TOKEN")
SERVE_PORT = config("PORT", default=8080, cast=int)
NGROK_TOKEN = config("NGROK_TOKEN", None)

PUBLIC_URL = config("PUBLIC_URL", None) or get_public_url(NGROK_TOKEN, SERVE_PORT)

DPI = config("DPI", default=600, cast=int)

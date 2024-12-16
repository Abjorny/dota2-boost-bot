import os


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_KEY = os.getenv("API_KEY")


def TextsList (key:str,values = {}) -> str:
    texts = {
        "start-text":f"*Hi dear, {values.get("username","")}!\n"
                        "Welcome to our Dota 2 account boosting bot! 🎮🔥.*",
    }
    if key in texts:
        return texts[key]
    else:
        raise KeyError(f"Key '{key}' not found in texts.")
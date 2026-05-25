import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from groq import Groq
from flask import Flask
from threading import Thread

# =========================
# TOKENS
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# =========================
# GROQ CLIENT
# =========================

client = Groq(api_key=GROQ_API_KEY)

# =========================
# TELEGRAM BOT
# =========================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# =========================
# FLASK SERVER (Render fix)
# =========================

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# =========================
# COMMANDS
# =========================

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("🚀 LEVEL 5 PRO BOT ONLINE")

# =========================
# AI CHAT
# =========================

@dp.message()
async def ai_chat(message: Message):
    user_text = message.text

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a powerful AI assistant."
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ],
            temperature=0.7,
            max_tokens=1024
        )

        ai_response = response.choices[0].message.content

        await message.answer(ai_response)

    except Exception as e:
        await message.answer(f"❌ AI Error:\n{str(e)}")

# =========================
# MAIN
# =========================

async def main():
    print("🤖 Bot started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("🚀 LEVEL 5 PRO BOT STARTED")

    web_thread = Thread(target=run_web)
    web_thread.start()

    asyncio.run(main())

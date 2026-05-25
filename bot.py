import asyncio
import os
import socket

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv
from openai import OpenAI

# Фикс для Windows network timeout
socket.setdefaulttimeout(30)

# Загружаем .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Проверка ключей
print("BOT TOKEN LOADED:", bool(BOT_TOKEN))
print("OPENAI KEY LOADED:", bool(OPENAI_API_KEY))

# Telegram Bot
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
Ты AI-антипрокрастинационный коуч.

Твоя задача:
- помогать человеку начать действие
- разбивать задачи на маленькие шаги
- уменьшать тревогу
- не осуждать
- отвечать коротко и понятно
"""

@dp.message()
async def handle_message(message: Message):
    try:
        user_text = message.text

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ]
        )

        reply = response.choices[0].message.content

        await message.answer(reply)

    except Exception as e:
        print("ERROR:", e)
        await message.answer("Ошибка при запросе к AI")

async def main():
    print("Бот запускается...")

    # Удаляем старые webhook
    await bot.delete_webhook(drop_pending_updates=True)

    print("Бот запущен 🚀")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

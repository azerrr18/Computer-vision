import asyncio
from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from handlers import calories

from aiogram.filters import Command,CommandStart
import os
from aiogram import Bot , Dispatcher,F
from aiogram.types import Message



dp = Dispatcher()




BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

print("Python file:", Path(__file__).resolve())
print(".env path:", ENV_FILE)
print(".env exists:", ENV_FILE.exists())

load_dotenv(ENV_FILE)

bot_token = os.getenv("BOT_TOKEN")

print("Token exists:", bool(bot_token))
print("Token length:", len(bot_token) if bot_token else 0)

@dp.message(CommandStart())
async def start(message:Message,):
    await message.answer("Please upload a photo")



@dp.message(Command('get_photo'))
async def get_photo(message:Message,):
    await message.answer_photo(photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRf56WdJA1tr3WU5vzYWpJM-aQOdiETb74LFeti7R7-_g&s=10.jpg",
    caption = "Pizza")



async def main():
    
    dp.include_router(calories)

    bot = Bot(token=bot_token)

    print("Starting bot....")
    try:
        await dp.start_polling(bot)
    finally:
        print("bot stopped")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
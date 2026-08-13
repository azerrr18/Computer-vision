import asyncio
from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext

from aiogram.fsm.state import StatesGroup,State
import os
from aiogram import Bot , Dispatcher,F
from aiogram.types import Message
from aiogram.filters import CommandStart,Command

dp = Dispatcher()
with open("bot.env", "w", encoding="utf-8") as f:
    f.write("Bot_Token=8792187702:AAGC38MLNdC3axnPeOMzJMNmLjYxNmZCJvU\n")

@dp.message(CommandStart())
async def cmd_start(message:Message):
    await message.answer("Hello please upload your photo:")

@dp.message(Command('get_photo'))
async def get_photo(message:Message,):
    await message.answer_photo(photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRf56WdJA1tr3WU5vzYWpJM-aQOdiETb74LFeti7R7-_g&s=10.jpg",
    caption = "Pizza")

@dp.message(F.photo)
async def  upload_photo(message:Message,bot=Bot):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    await bot.download_file(file.file_path,r"C:\Users\AZER\Downloads\banana.jpg")
    await message.answer("You upload a photo")

async def main():
    load_dotenv("bot.env")
    print("Does file Exists?", Path("bot.env").exists())
    print("All Variables:", dict(os.environ).get("BOT_TOKEN", "Not Found"))
    token = getenv("Bot_Token")
    print("Token loaded:", bool(token))
    if not token:
        error  = "No token Provided"
        raise ValueError(error)
    bot = Bot(token=token)

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
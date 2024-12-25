""" Telegram bot for sending highlights to subscribers """
import asyncio
import logging
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.filters.command import Command

load_dotenv()
logging.basicConfig(level=logging.INFO)

dp = Dispatcher()
bot = Bot(token=os.getenv('TOKEN'))

BASE_DIR, USERS_FILE_PATH = '', ''

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Handle the /start command."""
    with open(USERS_FILE_PATH, "r", encoding="utf-8") as f:
        t = f.read().splitlines()
        print(t)
    with open(USERS_FILE_PATH, "a", encoding="utf-8") as f:
        if str(message.chat.id) not in t:
            f.write("\n" + str( message.chat.id))
    await message.answer(f"It was a mistake, {message.from_user.first_name}! "
                         f"You subscribed to "
                         f"{os.getenv('LINKS').split(',')[0].split('/')[-1]}'s highlights!")


async def video_newsletter(user_id: str, video_path: str):
    """Send a video to a user."""
    try:
        video_file = FSInputFile(video_path)
        await bot.send_video(user_id.strip(), video_file, width=1920, height=1080)
    finally:
        await bot.session.close()



def main():
    """Start the bot."""
    global BASE_DIR, USERS_FILE_PATH
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    USERS_FILE_PATH = os.path.join(BASE_DIR, "users")
    try:
        asyncio.run(dp.start_polling(bot))
    finally:
        asyncio.run(bot.session.close())


if __name__ == "__main__":
    main()

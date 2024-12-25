import asyncio
import logging
import os

from aiogram.types import FSInputFile
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

load_dotenv()
logging.basicConfig(level=logging.INFO)

dp = Dispatcher()
bot = Bot(token=os.getenv('TOKEN'))

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    with open("../data/users", "r") as f:
        t = f.read().splitlines()
        print(t)
    with open("../data/users", "a") as f:
        if str(message.chat.id) not in t:
            f.write("\n" + str( message.chat.id))
    await message.answer(f"It was a mistake, {message.from_user.first_name}! You subscribed to {os.getenv('LINKS').split(',')[0].split('/')[-1]}'s highlights!")


async def video_newsletter(user_id: str, video_path: str):
    try:
        video_file = FSInputFile(video_path)
        await bot.send_video(user_id.strip(), video_file, width=1920, height=1080)
    finally:
        await bot.session.close()



def main():
    try:
        asyncio.run(dp.start_polling(bot))
    finally:
        asyncio.run(bot.session.close())


if __name__ == "__main__":
    main()

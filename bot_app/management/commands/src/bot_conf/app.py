import asyncio
import nest_asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from . bot_settings import API_KEY


loop = asyncio.new_event_loop()
nest_asyncio.apply()  # This might have catastrophic consequences while working around asyncio
# __import__('IPython').embed()
bot = Bot(token=API_KEY, loop=loop)
dp = Dispatcher(bot, storage=MemoryStorage())

async def main(message):
    await bot.send_message(806720968, message)

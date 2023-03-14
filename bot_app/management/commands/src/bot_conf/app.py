import asyncio
import nest_asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from .states import GameStates

from . bot_settings import API_KEY


loop = asyncio.new_event_loop()

nest_asyncio.apply()  # This may cause catastrophic consequences while working around asyncio

# __import__('IPython').embed()
bot = Bot(token=API_KEY, loop=loop)
print(11111111111111111111111111111111111111111111111111)
dp = Dispatcher(bot, storage=MemoryStorage())

async def main(chat_id, message):
    await bot.send_message(chat_id, message)

# async def set_state():
#     print(1)
#     await GameStates.university.set()
#     print(2)

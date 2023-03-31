import asyncio
import nest_asyncio
import logging
import urllib.request

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import exceptions, executor
from .states import GameStates
from aiogram.types import InputFile

from . bot_settings import API_KEY


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
fh = logging.FileHandler("bot.log")
fh.setLevel(logging.INFO)

loop = asyncio.new_event_loop()

nest_asyncio.apply()  # This may cause catastrophic consequences while working around asyncio

# __import__('IPython').embed()
bot = Bot(token=API_KEY, loop=loop)

dp = Dispatcher(bot, storage=MemoryStorage())


# related between-app functions
async def send_msg(chat_id, message):
    await bot.send_message(chat_id, message)


async def send_photo(chat_id, photo_url):
    await bot.send_photo(chat_id, photo_url)

async def send_file(chat_id, file_url, file_name='Document'):
    print(3)
    with urllib.request.urlopen(file_url) as doc_url:
        # await bot.send_document(chat_id, doc_url.read())
        await bot.send_document(chat_id, document=(file_name, doc_url.read()))
    print(4)


async def broadcast_message(user_id, text, photo = False, disable_notification = False) -> bool:
    try:
        if photo:
            with open(photo.image.path, 'rb') as image_file:
                input_file = InputFile(image_file)
                await bot.send_photo(user_id, input_file, caption=text)
        else:
            await bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        log.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        log.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.exception(f"Target [ID:{user_id}]: failed")
    else:
        log.info(f"Target [ID:{user_id}]: success")
        return True
    return False


# def get_users():
#     print(3)
#     yield from (786792821, 806720968)


async def broadcaster(users, pub_message, photo = False) -> int:
    # print(2, flush=True)
    """
    Simple broadcaster
    :return: Count of messages
    """
    count = 0
    try:
        for user_id in users:
            print(user_id, flush=True)
            if await broadcast_message(user_id, pub_message, photo):
                count += 1
            await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
    finally:
        log.info(f"{count} messages successful sent.")

    return count


# async def start_broadcasting():
#     print(1)
#     await executor.start(dp, broadcaster())

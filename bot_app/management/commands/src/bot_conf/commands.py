"""

Основной файл с функциями-слушателями, состояниями и реакциями 

"""

from aiogram import types
from aiogram.dispatcher import FSMContext

from .app import dp, bot
from .states import GameStates
from .keyboards import create_keyboard 
from .data_fetcher import *


@dp.message_handler(commands=['start', 'help'], state='*')  # Декоратор - слушатель
async def send_welcome(message: types.Message, state: FSMContext):

    # Реакция
    text = await read_from_db(BotDictionary, 'стартовое_сообщение')
    await message.answer(text)
    await GameStates.university.set()
    if await check_if_exists(BotUser, message['from']['username']):
        await update_field(BotUser, message['from']['username'])
    else: 
        await write_to_db(BotUser, message['from']['id'], message['from']['username']) 

    # await write_to_db(BotUser, message['from']['id'], message['from']['username'])

    # message example:
    # {"message_id": 657, "from": {"id": 806720968, "is_bot": false, "first_name": 
    # "Eddie", "username": "Eddudos", "language_code": "en"}, "chat": {"id": 806720968, "first_name": 
    # "Eddie", "username": "Eddudos", "type": "private"}, "date": 1675876383, "text": "/start", 
    # "entities": [{"type": "bot_command", "offset": 0, "length": 6}]}


@dp.message_handler(state=GameStates.university)
async def is_uni_active(message: types.Message, state: FSMContext):
    global buttons_lst
    await GameStates.university.set()
    msg = message['text']

    buttons_lst = await read_from_db(BotButton)
    keyboard = create_keyboard(buttons_lst)

    if await check_if_exists(BotClient, msg):
        text = await read_from_db(BotDictionary, 'выбор_типа_обращения')
        await message.answer(text, reply_markup=keyboard)
        await GameStates.request.set()
    else:
        text = await read_from_db(BotDictionary, 'отказ_обслуживания')
        await message.answer(f"{text}  {msg}")     


@dp.callback_query_handler(lambda c: c.data in [ans[0] for ans in buttons_lst], state=GameStates.request)
async def btn_click_call_back_all(callback_query: types.CallbackQuery, state: FSMContext):
    for ans in buttons_lst:
        if callback_query.data == ans[0]:    
            await bot.send_message(callback_query.from_user.id, ans[1])


@dp.message_handler(state=GameStates.request)
async def text_request(message: types.Message, state: FSMContext):
    text = await read_from_db(BotDictionary, 'прощание')
    await message.answer(text)
    await GameStates.new_request.set()
    #
    # TODO:
    # Передача параметров в открытые линии битрикс: 
    # BotUser.objects.all(), message['text'] 
    #


@dp.message_handler(state=GameStates.new_request)
async def text_request(message: types.Message, state: FSMContext):
    text = await read_from_db(BotDictionary, 'новое обращение')
    await message.answer(text)


    # data format:
    # {"id": "3464840176174457904", "from": {"id": 806720968, "is_bot": false, "first_name": "Eddie",
    # "username": "Eddudos", "language_code": "en"}, "message": {"message_id": 475, "from": 
    # {"id": 5900076914, "is_bot": true, "first_name": "my_main_bot", "username": "eddi_kimBot"}, 
    # "chat": {"id": 806720968, "first_name": "Eddie", "username": "Eddudos", "type": "private"}, 
    # "date": 1675697919, "text": "Выберите тип обращения (заявки):", "reply_markup": 
    # {"inline_keyboard": [[{"text": "Ошибка", "callback_data": "error"}], 
    # [{"text": "Баг", "callback_data": "bug"}], [{"text": "Неудобство", "callback_data": "uncomfy"}], 
    # [{"text": "Необходим оператор", "callback_data": "call_help"}]]}}, "chat_instance": "-4369657504028673461", 
    # "data": "uncomfy"}

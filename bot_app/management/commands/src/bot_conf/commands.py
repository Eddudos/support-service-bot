"""

Основной файл с функциями-слушателями, состояниями и реакциями 

"""
import sys

# sys.path.append('/home/sammy/myprojectdir')
# from django.apps import apps
# from django.conf import settings


# settings.configure(INSTALLED_APPS=['snippets'])
# apps.populate(settings.INSTALLED_APPS)

# from snippets.views import * 
# home/sammy/myprojectdir/snippets/views.py

import requests
import time


from urllib.parse import urlencode
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
    # await message.answer(token)
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
    global selected_btn
    for ans in buttons_lst:
        if callback_query.data == ans[0]:
            selected_btn = callback_query.data
            await bot.send_message(callback_query.from_user.id, ans[1])


@dp.message_handler(state=GameStates.request)
async def text_request(message: types.Message, state: FSMContext):
    text = await read_from_db(BotDictionary, 'прощание')
    await message.answer(text)
    await GameStates.new_request.set()

    PARAMS = {
        'CONNECTOR': 'OL_0',
        'LINE': 3,
        'MESSAGES': [{
                
                'user': {
                    'id': 3,
                    'last_name': 'Иванов',
                    'name': 'Иван',
                },
                'message': {
                    'id': False,
                    'date': int(time.time()),
                    'text': message['text']
                },
                'chat': {
                    'id': 1
                }
        
        }],
        'auth': await read_from_db(TokenTable, 'access_token')
    }

    url = CLIEND_ENDPOINT + 'imconnector.send.messages'
    x = requests.post(url, json = PARAMS)
    print('imconnector.send.messages', x.text, '\n')

    if ('error', 'invalid_token') in x.json().items() or ('error', 'expired_token') in x.json().items():
        #
        # TODO: 
        # Check if token does refresh
        #
        query_url = 'https://oauth.bitrix.info/oauth/token/'
        query_data = urlencode({
                    'grant_type': 'refresh_token',
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                    'refresh_token': await read_from_db(TokenTable, 'refresh_token')
        })
        x = requests.get(f'{query_url}?{query_data}')
        print('expired_token!', x.json(), '\n')
        
        token = x.json()['access_token']
        refresh_token = x.json()['refresh_token']
        await update_field(TokenTable, 'access_token', token)
        await update_field(TokenTable, 'refresh_token', refresh_token)
        x = requests.post(url, json = PARAMS)
        print('\n', x.text, '\n')
        

@dp.message_handler(state=GameStates.new_request)
async def text_request(message: types.Message, state: FSMContext):
    text = await read_from_db(BotDictionary, 'новое обращение')
    # await message.answer(text)
    PARAMS = {
        'CONNECTOR': 'OL_0',
        'LINE': 3,
        'MESSAGES': [{
                
                'user': {
                    'id': 3,
                    'last_name': 'Иванов',
                    'name': 'Иван',
                },
                'message': {
                    'id': False,
                    'date': int(time.time()),
                    'text': message['text']
                },
                'chat': {
                    'id': 1
                }
        
        }],
        'auth': await read_from_db(TokenTable, 'access_token')
    }

    url = CLIEND_ENDPOINT + 'imconnector.send.messages'
    x = requests.post(url, json = PARAMS)
    print('imconnector.send.messages', x.text, '\n')

    if ('error', 'invalid_token') in x.json().items() or ('error', 'expired_token') in x.json().items():
        #
        # TODO: 
        # Check if token does refresh
        #
        query_url = 'https://oauth.bitrix.info/oauth/token/'
        query_data = urlencode({
                    'grant_type': 'refresh_token',
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                    'refresh_token': await read_from_db(TokenTable, 'refresh_token')
        })
        x = requests.get(f'{query_url}?{query_data}')
        print('expired_token!', x.json(), '\n')
        
        token = x.json()['access_token']
        refresh_token = x.json()['refresh_token']
        await update_field(TokenTable, 'access_token', token)
        await update_field(TokenTable, 'refresh_token', refresh_token)
        x = requests.post(url, json = PARAMS)
        print('\n', x.text, '\n')


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

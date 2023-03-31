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
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .app import dp, bot
from .states import GameStates
from .keyboards import create_keyboard 
from .data_fetcher import *
from .bot_settings import API_KEY


# selected = ['Не выбрано', '']

def check_update_token(x, refresh_token):
    if ('error', 'invalid_token') in x.json().items() or ('error', 'expired_token') in x.json().items() or ('error','user_access_error') in x.json().items():
        #
        # TODO: 
        # Check if token does refresh
        #
        query_url = 'https://oauth.bitrix.info/oauth/token/'
        query_data = urlencode({
                    'grant_type': 'refresh_token',
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                    'refresh_token': refresh_token
        })
        x = requests.get(f'{query_url}?{query_data}')
        print('expired_token!', x.json(), '\n')
        
        token = x.json()['access_token']
        refresh_token = x.json()['refresh_token']
        return (token, refresh_token)
    else:
        return (None, None)
        



# @dp.message_handler()
@dp.message_handler(commands=['start'], state='*')  # Декоратор - слушатель
async def send_welcome(message: types.Message, state: FSMContext):
    global buttons_lst
    await state.finish()
    # Реакция
    text = await read_from_db(BotDictionary, 'стартовое_сообщение')
    await message.answer(text)

    buttons_lst = await read_from_db(BotButton)

    # for i in buttons_lst:
    #     print(i[0])

    # await message.answer(token)
    text = await read_from_db(BotDictionary, 'выбор_типа_обращения')

    keyboard = create_keyboard(buttons_lst)

    await message.answer(text, reply_markup=keyboard)
    await GameStates.request.set()
    

    # await write_to_db(BotUser, message['from']['id'], message['from']['username'])

    # message example:
    # {"message_id": 657, "from": {"id": 806720968, "is_bot": false, "first_name": 
    # "Eddie", "username": "Eddudos", "language_code": "en"}, "chat": {"id": 806720968, "first_name": 
    # "Eddie", "username": "Eddudos", "type": "private"}, "date": 1675876383, "text": "/start", 
    # "entities": [{"type": "bot_command", "offset": 0, "length": 6}]}


@dp.message_handler(content_types=['text'])  
async def first_message(message: types.Message, state: FSMContext):
    text = await read_from_db(BotDictionary, 'начальное_сообщение')
    await message.answer(text)


# @dp.message_handler(state=GameStates.university)
# async def is_uni_active(message: types.Message, state: FSMContext):
    
#     # await GameStates.university.set()
    
#     msg = message['text']
    
#     keyboard = create_keyboard(buttons_lst)

#     user_data = await state.get_data()

#     # if 'uni' in user_data:
#     #     await GameStates.request.set()

#     if await check_if_exists(BotClient, msg):
#         await state.update_data(uni=msg)
#         await state.update_data(counter=2)
#         text = await read_from_db(BotDictionary, 'выбор_типа_обращения')
#         await message.answer(text, reply_markup=keyboard)
#         await GameStates.request.set()

        # Подсчет обращений 
        # if await check_if_exists(BotUser, message['from']['id']):
        #     await update_field(BotUser, message['from']['id'])
        # else: 
        #     await write_to_db(BotUser, message['from']['id'], message['from']['username'])

#     else:
#         text = await read_from_db(BotDictionary, 'отказ_обслуживания')
#         await message.answer(f"{text}")     


@dp.callback_query_handler(lambda c: c.data in [ans[0] for ans in buttons_lst], state=GameStates.request)
async def btn_click_call_back_all(callback_query: types.CallbackQuery, state: FSMContext): 
    # index of pressed button in buttons_lst
    index = [ind for ind, elem in enumerate(buttons_lst) if elem[0] == callback_query.data][0]
    btn_tuple = buttons_lst[index]
    await state.update_data(btn=btn_tuple[0])
    user_data = await state.get_data()

    if 'msg' not in user_data:
        msg = await bot.send_message(callback_query.from_user.id, btn_tuple[1])
        await state.update_data(msg=msg)
    else:
        await user_data['msg'].edit_text(btn_tuple[1])

    if btn_tuple[2] == False:
        text = await read_from_db(BotDictionary, 'прощание')
        btn = await read_from_db(BotDictionary, 'новое обращение')
        ##### HARDCODE
        key_row = InlineKeyboardButton(text=btn, callback_data=btn, url='t.me/sibteh_alyona_bot?start=0')  
        keyboard = InlineKeyboardMarkup()
        keyboard.add(key_row) 
        await bot.send_message(callback_query.from_user.id, text, reply_markup=keyboard) 
        await GameStates.new_request.set()


@dp.message_handler(state=GameStates.request, content_types=['photo', 'text', 'document'])
async def request(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if 'btn' not in user_data:
        text = await read_from_db(BotDictionary, 'отказ_обслуживания')
        await message.answer(text)
        return

    await GameStates.open_line.set()
    await update_field(BotButton, user_data['btn'])

    # if await check_if_exists(BotUser, message['from']['id']):
    #     await update_field(BotUser, message['from']['id'])
    # else: 
    #     await write_to_db(BotUser, message['from']['id'], message['from']['username'])

    if not await check_if_exists(BotUser, message['from']['id']):
        await write_to_db(BotUser, message['from']['id'], message['from']['username'])
        await state.update_data(num_request=0)
    else:
        counter = await read_from_db(BotUser, message['from']['id'])
        await state.update_data(num_request=counter)

    file_id = await bot.get_user_profile_photos(message.from_id, 0, 1)
    if file_id["total_count"] >= 1:  
        # print('\n', file_id)
        file = await bot.get_file(file_id['photos'][0][0]['file_id']) 
        # print('\n', file)
        file_path = file.file_path
        # print('\n', file_path)
        photo_url = f"https://api.telegram.org/file/bot{API_KEY}/{file_path}"
    else: 
        photo_url = ''

    # {"total_count": 2, "photos": [[{"file_id": "AgACAgIAAxUAAWQO1IMda37tQNcpmC1dXNIkekvgAAK5pzEbyJUVMLMpP8V6SdgVAQADAgADYQADLwQ", "file_unique_id": "AQADuacxG8iVFTAAAQ", "file_size": 8656, "width": 160, "height": 160},
    # {"file_id": "AgACAgIAAxUAAWQO1IMda37tQNcpmC1dXNIkekvgAAK5pzEbyJUVMLMpP8V6SdgVAQADAgADYgADLwQ", "file_unique_id": "AQADuacxG8iVFTBn", "file_size": 27294, "width": 320, "height": 320}, 
    # {"file_id": "AgACAgIAAxUAAWQO1IMda37tQNcpmC1dXNIkekvgAAK5pzEbyJUVMLMpP8V6SdgVAQADAgADYwADLwQ", "file_unique_id": "AQADuacxG8iVFTAB", "file_size": 86296, "width": 640, "height": 640}]]}

    # photo_url = "https://fastly.picsum.photos/id/6/200/200.jpg?hmac=g4Q9Vcu5Ohm8Rwap3b6HSIxUfIALZ6BasESHhw7VjLE"
    
    if 'last_name' in message['from']:
        lastname = message['from']['last_name']
    else:
        lastname = f"@{message['from']['username']}"

    user_data = await state.get_data()

    PARAMS = {
        'CONNECTOR': 'OL_0',
        'LINE': 18,
        'MESSAGES': [{
                
                'user': {
                    'id': message['from']['id'],
                    'last_name': lastname,
                    'name': message['from']['first_name'],
                    'picture': {'url': photo_url},
                },
                'message': {
                    'id': False,
                    'date': int(time.time()),
                    'text': f"Тип обращения: {user_data['btn']}",
                    'files': ''
                },
                'chat': {
                    'id': message['chat']['id']
                }
        
        }],
        'auth': await read_from_db(TokenTable, 'access_token')
    }

    url = CLIEND_ENDPOINT + 'imconnector.send.messages'
    # x = requests.post(url, json = PARAMS)

    # check
    # token, refresh_token = check_update_token(x, await read_from_db(TokenTable, 'refresh_token'))

    # if token and refresh_token:
    #     await update_field(TokenTable, 'access_token', token)
    #     await update_field(TokenTable, 'refresh_token', refresh_token)
    #     PARAMS['auth'] = await read_from_db(TokenTable, 'access_token')
    #     x = requests.post(url, json = PARAMS)
    #     print('\n', x.text, '\n')

    x = requests.post(url, json = PARAMS)

        # check
    token, refresh_token = check_update_token(x, await read_from_db(TokenTable, 'refresh_token'))

    if token and refresh_token:
        await update_field(TokenTable, 'access_token', token)
        await update_field(TokenTable, 'refresh_token', refresh_token)
        PARAMS['auth'] = await read_from_db(TokenTable, 'access_token')
        x = requests.post(url, json = PARAMS)
        print('\n', x.text, '\n')

    # Delete FSM fields
    # user_data = await state.get_data()
    # del state['btn']
    # del state['msg']

    if message.photo:  ####   
        # print('message photo', message.photo)
        file = await bot.get_file(message.photo[-1]['file_id']) 
        # print('get file 2', file)
        file_path = file.file_path
        # print('file path', file_path)
        photo_url = f"https://api.telegram.org/file/bot{API_KEY}/{file_path}"
        print('photo url', photo_url)
        PARAMS['MESSAGES'][0]['message']['files'] = [{'url': photo_url}]
        if message.caption:
            # await message.answer(text)
            PARAMS['MESSAGES'][0]['message']['text'] = message.caption
        x = requests.post(url, json = PARAMS)

    elif message.document:
        file = await bot.get_file(message.document['file_id'])
        file_path = file.file_path
        doc_url = f"https://api.telegram.org/file/bot{API_KEY}/{file_path}"
        print('doc url', doc_url)
        PARAMS['MESSAGES'][0]['message']['files'] = [{'url': doc_url}]
        if message.caption:
            PARAMS['MESSAGES'][0]['message']['text'] = message.caption
        x = requests.post(url, json = PARAMS)
        
    else:
        print(3)
        PARAMS['MESSAGES'][0]['message']['text'] = message['text']
        x = requests.post(url, json = PARAMS)



    print('imconnector.send.messages', x.text, '\n')

    # token, refresh_token = check_update_token(x, await read_from_db(TokenTable, 'refresh_token'))

    # if token and refresh_token:
    #     await update_field(TokenTable, 'access_token', token)
    #     await update_field(TokenTable, 'refresh_token', refresh_token)
    #     PARAMS['auth'] = await read_from_db(TokenTable, 'access_token')
    #     PARAMS['MESSAGES'][0]['message']['text'] = f"{user_data['btn']}  |  {user_data['uni']}"
    #     x = requests.post(url, json = PARAMS)
    #     PARAMS['MESSAGES'][0]['message']['text'] = message['text']
    #     x = requests.post(url, json = PARAMS)
    #     print('\n', x.text, '\n')
        

# @dp.message_handler(state=GameStates.open_line, content_types=['document'])
# async def process_doc_step2(message: types.Message, state: FSMContext):
#     print(message)

# {"message_id": 2598, "from": {"id": 806720968, "is_bot": false, "first_name": "Eddie", "username": "Eddudos", "language_code": "en"}, 
# "chat": {"id": 806720968, "first_name": "Eddie", "username": "Eddudos", "type": "private"}, "date": 1680159688, 
# "document": {"file_name": "Ссылка6.docx", "mime_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
# "file_id": "BQACAgIAAxkBAAIKJmQlM8j2AsvU0DrIjezcYxyqgFMNAAKYJwAC1s8pSdFY6_RS6ZC2LwQ", "file_unique_id": "AgADmCcAAtbPKUk", "file_size": 10273}}


@dp.message_handler(state=GameStates.open_line, content_types=['photo', 'text', 'document'])
async def open_line(message: types.Message, state: FSMContext):
    # text = await read_from_db(BotDictionary, 'новое обращение')
    user_data = await state.get_data()
    if user_data['num_request'] < await read_from_db(BotUser, message['from']['id']):
        if message['text'] != '0' and message['text'] != '1':
            text = await read_from_db(BotDictionary, 'прощание')
            btn = await read_from_db(BotDictionary, 'новое обращение')
            ##### HARDCODE
            key_row = InlineKeyboardButton(text=btn, callback_data=btn, url='t.me/sibteh_alyona_bot?start=0')  
            keyboard = InlineKeyboardMarkup()
            keyboard.add(key_row)
            await message.answer(text, reply_markup=keyboard) 
            await GameStates.new_request.set()
            return


    # if await read_from_db(BotUser, message['from']['id']) >= user_data['counter']:
    #     if message['text'] not in ['0', '1']:
    #         await GameStates.request.set()
    #         keyboard = create_keyboard(buttons_lst)
    #         text = await read_from_db(BotDictionary, 'выбор_типа_обращения')
    #         await state.update_data(counter=user_data['counter'] + 1)
    #         await message.answer(text, reply_markup=keyboard)
    #         return
        

    if 'last_name' in message['from']:
        lastname = message['from']['last_name']
    else:
        lastname = f"@{message['from']['username']}"

    user_data = await state.get_data()

    PARAMS = {
        'CONNECTOR': 'OL_0',
        'LINE': 18,
        'MESSAGES': [{
                
                'user': {
                    'id': message['from']['id'],
                    'last_name': lastname,
                    'name': message['from']['first_name']
                },
                'message': {
                    'id': False,
                    'date': int(time.time()),
                    'text': message['text'],
                    'files': ''
                },
                'chat': {
                    'id': message['chat']['id']
                }
        
        }],
        'auth': await read_from_db(TokenTable, 'access_token')
    }



    if message.photo:
        file = await bot.get_file(message.photo[-1]['file_id']) 
        file_path = file.file_path
        photo_url = f"https://api.telegram.org/file/bot{API_KEY}/{file_path}"
        print('photo url', photo_url)
        PARAMS['MESSAGES'][0]['message']['files'] = [{'url': photo_url}]
        if message.caption:  ####
            PARAMS['MESSAGES'][0]['message']['text'] = message.caption
    if message.document:
        file = await bot.get_file(message.document['file_id'])
        file_path = file.file_path
        doc_url = f"https://api.telegram.org/file/bot{API_KEY}/{file_path}"
        print('doc url', doc_url)
        PARAMS['MESSAGES'][0]['message']['files'] = [{'url': doc_url}]
        if message.caption:
            PARAMS['MESSAGES'][0]['message']['text'] = message.caption

    # [<PhotoSize {"file_id": "AgACAgIAAxkBAAIBtWQZkRxOCpVeMxCsasVaN0KlHkenAALqyzEb4ZvJSN4yxzFShx0XAQADAgADcwADLwQ", 
    # "file_unique_id": "AQAD6ssxG-GbyUh4", "file_size": 1015, "width": 90, "height": 55}>, 
    # <PhotoSize {"file_id": "AgACAgIAAxkBAAIBtWQZkRxOCpVeMxCsasVaN0KlHkenAALqyzEb4ZvJSN4yxzFShx0XAQADAgADbQADLwQ", 
    # "file_unique_id": "AQAD6ssxG-GbyUhy", "file_size": 16246, "width": 320, "height": 194}>, 
    # <PhotoSize {"file_id": "AgACAgIAAxkBAAIBtWQZkRxOCpVeMxCsasVaN0KlHkenAALqyzEb4ZvJSN4yxzFShx0XAQADAgADeAADLwQ", 
    # "file_unique_id": "AQAD6ssxG-GbyUh9", "file_size": 38455, "width": 546, "height": 331}>]

    url = CLIEND_ENDPOINT + 'imconnector.send.messages'
    x = requests.post(url, json = PARAMS)
    print('imconnector.send.messages', x.text, '\n')

    token, refresh_token = check_update_token(x, await read_from_db(TokenTable, 'refresh_token'))

    if token and refresh_token:
        await update_field(TokenTable, 'access_token', token)
        await update_field(TokenTable, 'refresh_token', refresh_token)
        PARAMS['auth'] = await read_from_db(TokenTable, 'access_token')
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


@dp.message_handler(state=GameStates.new_request, content_types=['photo', 'text'])
async def new_request(message: types.Message, state: FSMContext):
    text = await read_from_db(BotDictionary, 'прощание')
    btn = await read_from_db(BotDictionary, 'новое обращение')
    ##### HARDCODE
    key_row = InlineKeyboardButton(text=btn, callback_data=btn, url='t.me/sibteh_alyona_bot?start=0')  
    keyboard = InlineKeyboardMarkup()
    keyboard.add(key_row)
    await message.answer(text, reply_markup=keyboard) 


# @dp.callback_query_handler(state=GameStates.new_request)
# async def new_request_button(message: types.Message, callback_query: types.CallbackQuery, state: FSMContext):
#     print(1)
#     await state.finish()
#     # await GameStates.start.set()
#     # await dp.current_handler().send_welcome(message)
#     print(2)

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# Формирование клавиатуры 
def create_keyboard(keyboard_obj):
    keyboard = InlineKeyboardMarkup()
    for btn_name, btn_value, btn_open_line in keyboard_obj:
        key_row = InlineKeyboardButton(text=btn_name, callback_data=btn_name)
        keyboard.add(key_row)
    
    return keyboard

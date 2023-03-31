from aiogram.dispatcher.filters.state import State, StatesGroup


# Состояния бота для FSM
class GameStates(StatesGroup):
    start = State()
    request = State()
    open_line = State()
    new_request = State()

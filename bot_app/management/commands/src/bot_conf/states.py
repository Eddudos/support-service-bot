from aiogram.dispatcher.filters.state import State, StatesGroup


# Состояния бота для FSM
class GameStates(StatesGroup):
    start = State()
    university = State()
    request = State()
    new_request = State()

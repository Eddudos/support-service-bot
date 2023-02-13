from aiogram import executor
from bot_conf import dp


# Запуск полинга через bot_conf/__init__.py
executor.start_polling(dp, skip_updates=True)

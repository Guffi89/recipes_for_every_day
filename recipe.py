from aiogram2 import Dispatcher, Bot, executor, types
from config import TOKEN

bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handlers(command=['help'])
async def help_command(message: types.Message):
    await message.answer("Список команд:")
    await message.delete()


@dp.message_handlers(command=['start'])
async def start_command(message: types.Message):
    await message.answer("Привет, введите набор продуктов, который имеете в наличии\n(через пробел):")







if __name__ == '__main__':
    executor.start_polling(dp)

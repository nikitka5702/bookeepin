import asyncio
from typing import Optional

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

from config import Config

config = Config()

BOT_TOKEN = config.BOT_TOKEN

loop = asyncio.get_event_loop()

bot = Bot(token=BOT_TOKEN, loop=loop)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class BotStates(StatesGroup):
    balance = State()
    income = State()
    expanses = State()
    account = State()
    amount = State()
    category = State()
    date = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    # TODO: check is user exits else create new user

    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    reply_markup.add('Просмотреть остаток на счёте')
    reply_markup.add('Добавить расходы')
    reply_markup.add('Добавить доходы')

    await bot.send_message(chat_id=message.chat.id, text='Выберите операцию', reply_markup=reply_markup)


@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(lambda message: message.text.lower() == 'cancel', state='*')
async def cancel_handler(message: types.Message, state: FSMContext, raw_state: Optional[str] = None):
    """
    Allow user to cancel any action
    """
    if raw_state is None:
        return
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard
    await message.reply('Canceled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda msg: msg.lower().strip() == 'просмотреть остаток на счёте', state=BotStates.balance)
async def process_balance(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='остаток')


@dp.message_handler(lambda msg: msg.lower().strip() == 'добавить расходы', state=BotStates.expanses)
async def process_income(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='расходы')


@dp.message_handler(lambda msg: msg.lower().strip() == 'добавить доходы', state=BotStates.income)
async def process_expanses(message: types.Message, state: FSMContext):
    await bot.send_message(chat_id=message.chat.id, text='доходы')


@dp.message_handler(state=BotStates.account)
async def process_account(message: types.Message, state: FSMContext):
    # TODO: get user accounts
    pass


def is_float(number: str):
    try:
        float(number)
    except ValueError:
        return False
    return True


@dp.message_handler(lambda message: is_float(message.text), state=BotStates.amount)
async def process_amount(message: types.Message, state: FSMContext):
    pass


@dp.message_handler(state=BotStates.category)
async def process_category(message: types.Message, state: FSMContext):
    pass


@dp.message_handler(state=BotStates.date)
async def process_category(message: types.Message, state: FSMContext):
    pass


if __name__ == '__main__':
    executor.start_polling(dp, loop=loop, skip_updates=True)

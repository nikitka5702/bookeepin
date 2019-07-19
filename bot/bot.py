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

ACCOUNTS = ['наличка', 'Счет']

class BotStates(StatesGroup):
    expense = State()
    balance = State()
    account = State()
    income = State()
    amount = State()
    category = State()
    date = State()

    start = State()
    details = State()


def get_accounts(user):
    return ACCOUNTS


def get_accounts_keyboard_markup(user):
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    for item in get_accounts(user):
        reply_markup.add(item)

    return reply_markup


@dp.message_handler(commands=['start', 'Start'])
@dp.message_handler(lambda msg: msg.text.lower() in ['start'])
async def cmd_start(message: types.Message, state: FSMContext):
    """
    Conversation's entry point
    """
    # TODO: check is user exits else create new user

    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    reply_markup.add('Просмотреть остаток на счёте')
    reply_markup.add('Добавить расходы')
    reply_markup.add('Добавить доходы')
    reply_markup.add('Выход')

    await BotStates.start.set()

    await bot.send_message(chat_id=message.chat.id, text='Выберите операцию', reply_markup=reply_markup)


@dp.message_handler(commands=['cancel'])
@dp.message_handler(lambda message: message.text.lower() in ['cancel', 'выход'], state=BotStates.start)
async def cancel_handler(message: types.Message, state: FSMContext, raw_state: Optional[str] = None):
    """
    Allow user to cancel any action
    """
    if raw_state is None:
        return
    # Cancel state and inform user about it
    await state.finish()

    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    reply_markup.add('Start')
    # And remove keyboard
    await message.reply('Canceled.', reply_markup=reply_markup)


@dp.message_handler(lambda msg: msg.text.lower() == 'просмотреть остаток на счёте', state=BotStates.start)
async def process_balance(message: types.Message, state: FSMContext):

    # TODO: send request for balance for this user

    await bot.send_message(chat_id=message.chat.id, text='остаток')


@dp.message_handler(lambda msg: msg.text == 'Добавить расходы', state=BotStates.start)
async def process_income(message: types.Message, state: FSMContext):

    reply_markup = get_accounts_keyboard_markup(message.from_user)
    await BotStates.details.set()

    async with state.proxy() as data:
        data['opp'] = 'расходы'

    await bot.send_message(chat_id=message.chat.id, text='Выберите источник', reply_markup=reply_markup)


@dp.message_handler(lambda msg: msg.text == 'Добавить доходы', state=BotStates.start)
async def process_expanses(message: types.Message, state: FSMContext=None):

    # TODO: next step
    await BotStates.details.set()

    async with state.proxy() as data:
        data['opp'] = 'доходы'

    await bot.send_message(chat_id=message.chat.id, text='Выберите куда начислены средства')


@dp.message_handler(lambda msg: msg.text in get_accounts(msg.from_user), state=BotStates.details)
async def process_amount(message: types.Message, state: FSMContext):

    await bot.send_message(chat_id=message.chat.id, text='details')

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
async def process_date(message: types.Message, state: FSMContext):
    pass


if __name__ == '__main__':
    executor.start_polling(dp, loop=loop, skip_updates=True)

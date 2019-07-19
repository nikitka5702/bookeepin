import asyncio
import locale

from typing import Optional

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

from config import config


INCOME = 'I'
EXPENSE = 'E'

BOT_TOKEN = config.BOT_TOKEN

loop = asyncio.get_event_loop()

bot = Bot(token=BOT_TOKEN, loop=loop)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

ACCOUNTS = {1: 'наличка', 2: 'Счет'}
CATEGORIES = {1: 'Машина', 2: 'Магазин', 3: 'Обеды'}

class BotStates(StatesGroup):
    start = State()
    details = State()
    amount = State()
    description = State()
    category = State()
    date = State()


def get_categories(user) -> list:
    res = list(CATEGORIES.values())

    return res


def get_category_keyboard_markup(user, opp_type):
    choice = get_categories(user)
    choice.append('Отмена')
    choice.insert(0, 'skip')

    return get_keyboard_markup(choice)


def get_category_id(name, type):
    for key, value in CATEGORIES.items():
        if value == name:
            return key


def get_accounts(user):
    res = list(ACCOUNTS.values())

    return res


def get_account_id(name: str):
    for key, value in ACCOUNTS.items():
        if value == name:
            return key


def get_keyboard_markup(choice: list):
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    for item in choice:
        reply_markup.add(item)

    return reply_markup


def get_accounts_keyboard_markup(user, choice: list=None):
    if not choice:
        choice = get_accounts(user)

    choice.append('Отмена')
    return get_keyboard_markup(choice)


def get_start_menu():
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    reply_markup.add('Просмотреть остаток на счёте')
    reply_markup.add('Добавить расходы')
    reply_markup.add('Добавить доходы')
    # reply_markup.add('Отмена')

    return reply_markup


@dp.message_handler(commands=['start', 'Start'])
@dp.message_handler(lambda msg: msg.text.lower() in ['start'])
async def cmd_start(message: types.Message, state: FSMContext):
    """
    Conversation's entry point
    """
    # TODO: check is user exits else create new user

    reply_markup = get_start_menu()

    await BotStates.start.set()

    await bot.send_message(chat_id=message.chat.id, text='Выберите операцию', reply_markup=reply_markup)


@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(lambda message: message.text.lower() in ['cancel', 'выход', 'отмена'], state='*')
async def cancel_handler(message: types.Message, state: FSMContext, raw_state: Optional[str] = None):
    """
    Allow user to cancel any action
    """
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    reply_markup.add('Start')

    if raw_state is None:
        return await message.reply('Canceled.', reply_markup=reply_markup)
    # Cancel state and inform user about it
    # await state.finish()
    async with state.proxy() as data:
        data.state = None

    # And remove keyboard
    return await message.reply('Canceled.', reply_markup=reply_markup)


@dp.message_handler(lambda msg: msg.text.lower() == 'просмотреть остаток на счёте', state=BotStates.start)
async def process_balance(message: types.Message, state: FSMContext):

    # TODO: send request for balance for this user

    await bot.send_message(chat_id=message.chat.id, text='остаток')


@dp.message_handler(lambda msg: msg.text == 'Добавить расходы', state=BotStates.start)
async def process_income(message: types.Message, state: FSMContext):

    reply_markup = get_accounts_keyboard_markup(message.from_user)
    await BotStates.details.set()

    async with state.proxy() as data:
        data['opp'] = EXPENSE

    await bot.send_message(chat_id=message.chat.id, text='Выберите источник', reply_markup=reply_markup)


@dp.message_handler(lambda msg: msg.text == 'Добавить доходы', state=BotStates.start)
async def process_expanses(message: types.Message, state: FSMContext=None):

    # TODO: next step
    await BotStates.details.set()

    async with state.proxy() as data:
        data['opp'] = INCOME

    reply_markup = get_accounts_keyboard_markup(message.from_user)
    await bot.send_message(chat_id=message.chat.id, text='Выберите куда начислены средства', reply_markup=reply_markup)


@dp.message_handler(lambda msg: msg.text in get_accounts(msg.from_user), state=BotStates.details)
async def process_account(message: types.Message, state: FSMContext):
    reply_markup = get_accounts_keyboard_markup(message.from_user)

    async with state.proxy() as data:
        data['account'] = get_account_id(message.text)

    await BotStates.amount.set()

    await bot.send_message(chat_id=message.chat.id, text='Введите сумму (копейки через точку):',
                           reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=BotStates.amount)
async def process_amount(message: types.Message, state: FSMContext):
    if is_float(message.text):
        amount = locale.atof(message.text)

        async with state.proxy() as data:
            data['ammount'] = amount

        await BotStates.description.set()

        reply_markup = get_keyboard_markup(['skip', 'Отмена'])

        await bot.send_message(chat_id=message.chat.id, text='Описание:', reply_markup=reply_markup)
    else:
        await bot.send_message(chat_id=message.chat.id, text='Введите сумму (копейки через точку):')


@dp.message_handler(state=BotStates.description)
async def process_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text != 'skip':
            data['description'] = message.text
        opp_type = data['opp']

    await BotStates.category.set()

    reply_markup = get_category_keyboard_markup(message.from_user, opp_type)

    await bot.send_message(chat_id=message.chat.id, text='Выберите группу (если нет нужной, просто введите ее):',
                           reply_markup=reply_markup)


@dp.message_handler(state=BotStates.category)
async def process_category(message: types.Message, state: FSMContext):
    if message.text != 'skip':
        async with state.proxy() as data:
            opp_type = data['opp']
            data['category'] = get_category_id(message.text, opp_type)

    await BotStates.date.set()

    reply_markup = get_keyboard_markup(['skip', 'Отмена'])
    await bot.send_message(chat_id=message.chat.id, text='Дата совершения операции YYYY-MM-DD(автоматически подставиться сегодня):',
                           reply_markup=reply_markup)


@dp.message_handler(state=BotStates.date)
async def process_date(message: types.Message, state: FSMContext, raw_state: Optional[str] = None):
    if message.text != 'skip':
        async with state.proxy() as data:
            data['date'] = message.text

    # TODO: send request for create record in BD

    message = await bot.send_message(chat_id=message.chat.id, text='Запись создана!')
    return await cancel_handler(message=message, state=state, raw_state=raw_state)


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

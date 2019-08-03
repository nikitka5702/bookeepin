import asyncio
import locale

import redis
from typing import Optional

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

from config import config
from api import sign_in, create_category, get_accounts_dict, get_categories_dict, create_expense, create_income

r = redis.StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB)

INCOME = 'I'
EXPENSE = 'E'

BOT_TOKEN = config.BOT_TOKEN

loop = asyncio.get_event_loop()

bot = Bot(token=BOT_TOKEN, loop=loop)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class BotStates(StatesGroup):
    start = State()
    details = State()
    amount = State()
    description = State()
    category = State()
    date = State()

    sign_in = State()


def get_category_keyboard_markup(user, opp_type):
    choice = get_categories(opp_type, user)
    choice.append('Отмена')
    choice.insert(0, 'skip')

    return get_keyboard_markup(choice)


def get_token_from_redis(user):
    return r.get(user.id).decode()


def get_categories(categories_type, user) -> list:
    token = get_token_from_redis(user)
    res = list(get_categories_dict(categories_type, token).values())

    return res


def get_category_id(name, type_, user):
    for key, value in get_categories_dict(type_, user).items():
        if value == name:
            return key
    return create_category(type_, name, get_token_from_redis(user))


def get_accounts(user):
    token = get_token_from_redis(user)
    accounts = get_accounts_dict(token)
    if accounts:
        res = list(accounts.values())
        return res
    else:
        return []


def get_account_id(name: str, user):
    token = get_token_from_redis(user)
    for key, value in get_accounts_dict(token).items():
        if value == name:
            return key


def get_keyboard_markup(choice: list):
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    for item in choice:
        reply_markup.add(item)

    return reply_markup


def get_accounts_keyboard_markup(user, choice: list = None):
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


def is_existing_user(user_id):
    return r.get(user_id) is not None


def get_auth_token(user_id):
    return r.get(user_id)


@dp.message_handler(commands=['start'])
@dp.message_handler(lambda msg: msg.text.lower() in ['start', 'Start'])
async def cmd_start(message: types.Message, state: FSMContext):

    if is_existing_user(message.from_user.id):
        token = get_auth_token(message.from_user.id)
    else:
        await BotStates.sign_in.set()
        reply_markup = get_keyboard_markup(['отмена'])
        return await bot.send_message(chat_id=message.chat.id, text='Введите логин и пароль\nв фомате:\n"логин:пароль"',
                                      reply_markup=reply_markup)

    async with state.proxy() as data:
        data['token'] = token

    reply_markup = get_start_menu()
    await BotStates.start.set()

    await bot.send_message(chat_id=message.chat.id, text='Выберите операцию', reply_markup=reply_markup)


@dp.message_handler(lambda msg: msg.text.lower() not in ['отмена'], state=BotStates.sign_in)
async def sign_in_handler(message: types.Message, state: FSMContext):
    username, password = message.text.split(':')
    token = sign_in(username, password)
    if token:
        r.set(message.from_user.id, token)
        reply_markup = get_start_menu()
        await BotStates.start.set()

        await bot.send_message(chat_id=message.chat.id, text=f'Выберите операцию\n{token}', reply_markup=reply_markup)
    else:
        await bot.send_message(chat_id=message.chat.id, text='Введите логин и пароль\nв фомате:\n"логин:пароль"')


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
async def process_expanses(message: types.Message, state: FSMContext = None):
    # TODO: next step
    await BotStates.details.set()

    async with state.proxy() as data:
        data['opp'] = INCOME

    reply_markup = get_accounts_keyboard_markup(message.from_user)
    await bot.send_message(chat_id=message.chat.id, text='Выберите куда начислены средства', reply_markup=reply_markup)


@dp.message_handler(lambda msg: msg.text in get_accounts(msg.from_user), state=BotStates.details)
async def process_account(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['account'] = get_account_id(message.text, message.from_user)

    await BotStates.amount.set()

    await bot.send_message(chat_id=message.chat.id, text='Введите сумму (копейки через точку):',
                           reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=BotStates.amount)
async def process_amount(message: types.Message, state: FSMContext):
    if is_float(message.text):
        amount = locale.atof(message.text)

        async with state.proxy() as data:
            data['amount'] = amount

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
        else:
            data['description'] = ''
        opp_type = data['opp']

    await BotStates.category.set()

    reply_markup = get_category_keyboard_markup(message.from_user, opp_type)

    await bot.send_message(chat_id=message.chat.id, text='Выберите категорию (если нет нужной, просто введите ее):',
                           reply_markup=reply_markup)


@dp.message_handler(state=BotStates.category)
async def process_category(message: types.Message, state: FSMContext):
    if message.text != 'skip':
        async with state.proxy() as data:
            opp_type = data['opp']
            data['category'] = get_category_id(message.text, opp_type, message.from_user)

    await BotStates.date.set()

    reply_markup = get_keyboard_markup(['skip', 'Отмена'])
    await bot.send_message(chat_id=message.chat.id,
                           text='Дата совершения операции YYYY-MM-DD(автоматически подставиться сегодня):',
                           reply_markup=reply_markup)


@dp.message_handler(state=BotStates.date)
async def process_date(message: types.Message, state: FSMContext, raw_state: Optional[str] = None):
    if message.text != 'skip':
        async with state.proxy() as data:
            data['date'] = message.text

    # TODO: send request for create record in BD
    res = {}
    token = get_token_from_redis(message.from_user)
    async with state.proxy() as data:
        for key, value in data.items():
            if key in ['account',
                       'amount',
                       'date',
                       'description',
                       'group']:
                res[key] = value
        if data['opp'] == EXPENSE:
            res = create_expense(token, res)
        elif data['opp'] == INCOME:
            res = create_income(token, res)
    if res:
        message = await bot.send_message(chat_id=message.chat.id, text='Запись создана!')
    else:
        message = await bot.send_message(chat_id=message.chat.id, text='Запись НЕ создана!')
    return await cancel_handler(message=message, state=state, raw_state=raw_state)


def is_float(number: str):
    try:
        float(number)
    except ValueError:
        return False
    return True


if __name__ == '__main__':
    executor.start_polling(dp, loop=loop, skip_updates=True)

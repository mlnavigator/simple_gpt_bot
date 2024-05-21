import asyncio
import logging
import sys
import os
from collections import defaultdict
import json

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold
from aiogram.filters import Command, Filter
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import config

from generator import generate, update_client

as_lock = asyncio.Lock()
bot = None


# Bot token can be obtained via https://t.me/BotFather
TOKEN = config.config["BOT_TOKEN"]
ACCESS_KEY = config.config["ACCESS_KEY"]
SU_ACCESS_KEY = config.config["SU_ACCESS_KEY"]


users = set()
superusers = set()

user_data = defaultdict(lambda: {'messages': [], 'system': '',
                                       'user_name': '', 'first_name': '',
                                       'user_id': '', 'cnt': 0})

user_data_path = os.path.join(config.base_dir, 'assets/user_data.json')


def update_user_data():
    global user_data
    global user_data_path
    with open(user_data_path, 'w') as fd:
        json.dump(dict(user_data), fd, ensure_ascii=False)


def load_user_data():
    global user_data
    global user_data_path
    try:
        with open(user_data_path, 'r') as fd:
            data = json.load(fd)
    except:
        data = dict()

    for k, v in data.items():
        user_data[k] = v


if os.path.exists(user_data_path):
    load_user_data()
    users = set(user_data.keys())


# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


def _escape(text: str) -> str:
    text = str(text).replace('<', '&lt;').\
        replace('>', '&gt;').replace('&', '&amp;')
    return text


def create_keyboard():
    menu_btns = [
        [KeyboardButton(text='/reset'), KeyboardButton(text='/start')]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=menu_btns,
        resize_keyboard=True,
        # input_field_placeholder="Ask your question",
    )
    return keyboard


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    print(message)
    user_id = str(message.chat.id)
    text = message.text.split('/start')[-1].strip()
    if user_id in users or text == ACCESS_KEY:
        users.add(user_id)
        user_data[user_id]['user_name'] = message.chat.username
        user_data[user_id]['first_name'] = message.chat.first_name
        user_data[user_id]['user_id'] = str(user_id)

        keyboard = create_keyboard()

        await message.answer("Доступ получен. напишите ваше сообщение\n"
                             "Для установки системного сообщения напишите\n/system ваше сообщение\n\n"
                             "Бот помнит последние 10 сообщений\n\n"
                             "/info - для получения вашей информации\n\n"
                             "/reset - очистить историю сообщений\n\n",
                             reply_markup=keyboard
                             )
        print(user_data)
    else:
        await message.answer(
            f"Ваш user_id\n{user_id}\n\n"
            "для доступа к боту введите /start ACCESS_KEY"
                             )


@dp.message(Command(commands=["admin"]))
async def command_admin_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    user_id = str(message.chat.id)
    text = message.text.split('/admin')[-1].strip()

    if user_id in superusers or text == SU_ACCESS_KEY:
        superusers.add(user_id)
        users.add(user_id)
        user_data[user_id]['user_name'] = message.chat.username
        user_data[user_id]['first_name'] = message.chat.first_name
        # print(user_data[user_id])
        await message.answer("Админский доступ получен.\n\n"
                             "/admin список админ команд\n\n"
                             "/config key value\n\n"
                             "/reboot - перезапустить бота\n\n"
                             "/reset_client - обновить подключение к чат гпт\n\n"
                             "/stat - статистика по пользователям\n\n"
                             "/rm user_id - удалить пользователя\n\n"
                             "/add user_id - добавить пользователя\n\n"
                             )
    else:
        await message.answer("для доступа к админке введите /admin ACCESS_KEY")


@dp.message(Command(commands=["stat"]))
async def command_stat_handler(message: Message) -> None:
    user_id = str(message.chat.id)
    if user_id not in superusers:
        await message.answer("нет доступа")
        return

    stats = sorted(user_data.values(), key=lambda x: -x['cnt'])[:10]
    stats = [f"@{u['user_name']} {u['first_name']} {u['user_id']} {u['cnt']//1000}k" for u in stats]
    msg = '\n'.join(stats)
    await message.answer(msg)


@dp.message(Command(commands=["config"]))
async def command_config_handler(message: Message) -> None:
    user_id = str(message.chat.id)
    if user_id not in superusers:
        await message.answer("нет доступа")
        return

    text = message.text
    parts = text.split()

    if len(parts) == 1:
        msg = '\n\n'.join(config.config.keys())
        await message.answer(msg)
        return

    key = parts[1]
    value = parts[2]

    async with as_lock:
        config.update_config_attribute(key, value)

    msg = f'установлены значения "{key}": "{value}"'

    await message.answer(msg)


@dp.message(Command(commands=["reset_client"]))
async def command_reset_client_handler(message: Message) -> None:
    user_id = str(message.chat.id)
    if user_id not in superusers:
        await message.answer("нет доступа")
        return
    update_client()
    msg = f'инициализирован клиент'

    await message.answer(msg)


@dp.message(Command(commands=["reboot"]))
async def command_reboot_handler(message: Message) -> None:
    user_id = str(message.chat.id)
    if user_id not in superusers:
        await message.answer("нет доступа")
        return

    sys.exit(0)


@dp.message(Command(commands=["rm"]))
async def command_reset_client_handler(message: Message) -> None:
    user_id = str(message.chat.id)
    if user_id not in superusers:
        await message.answer("нет доступа")
        return

    text = message.text
    parts = text.split()

    if len(parts) != 2:
        msg = 'не верный формат'
        await message.answer(msg)
        return

    del_user_id = parts[1]

    async with as_lock:
        users.remove(del_user_id)
        user_data.pop(del_user_id, None)
        update_user_data()

    msg = f'удален юзер с id {del_user_id}'

    await message.answer(msg)


@dp.message(Command(commands=["add"]))
async def command_reset_client_handler(message: Message) -> None:
    user_id = str(message.chat.id)
    if user_id not in superusers:
        await message.answer("нет доступа")
        return

    text = message.text
    parts = text.split()

    if len(parts) != 2:
        msg = 'не верный формат'
        await message.answer(msg)
        return

    add_user_id = str(parts[1])
    users.add(add_user_id)
    user_data[add_user_id]['user_id'] = add_user_id
    print(users)

    async with as_lock:
        update_user_data()

    msg = f'добавлен юзер с id {add_user_id}'
    await message.answer(msg)


@dp.message(Command(commands=["system"]))
async def command_system_handler(message: Message) -> None:
    user_id = str(message.chat.id)
    if user_id not in users:
        await message.answer("для доступа к боту введите /start ACCESS_KEY")
        return

    print(user_id)
    print(message.text)
    text = message.text
    text = text.replace('/system', '').strip()
    user_data[user_id]['system'] = text
    await message.answer(f'Вы установили системное сообщение\n{text}')


@dp.message(Command(commands=["info"]))
async def command_info_handler(message: Message) -> None:
    user_id = str(message.chat.id)
    if user_id not in users:
        await message.answer("для доступа к боту введите /start ACCESS_KEY")
        return

    data = f'Ваш телеграм чат ID:\n{user_id}\n\n'
    data += f'system_message: {user_data[user_id]["system"]}\n\n'
    data += 'История диалога:\n\n'
    for m in user_data[user_id]['messages']:
        data += f'role: {m[0]}\n{m[1]}\n\n'

    await message.answer(data)


@dp.message(Command(commands=["reset"]))
async def command_reset_handler(message: Message) -> None:
    user_id = str(message.chat.id)
    if user_id not in users:
        await message.answer("для доступа к боту введите /start ACCESS_KEY")
        return

    user_data[user_id]['messages'] = []
    await message.answer('история сообщений очищена')


@dp.message(Command(commands=["mass"]))
async def command_mass_handler(message: Message) -> None:
    global bot

    user_id = str(message.chat.id)
    if user_id not in superusers:
        await message.answer("нет доступа")
        return

    text = message.text
    parts = text.split()

    if len(parts) < 2:
        msg = 'не верный формат'
        await message.answer(msg)
        return

    mass_message = _escape(' '.join(parts[1:]))
    all_users = list(users)

    for user_id in all_users:
        await bot.send_message(user_id, mass_message)


@dp.message()
async def message_handler(message: types.Message) -> None:
    user_id = str(message.chat.id)
    if user_id not in users:
        await message.answer("для доступа к боту введите /start ACCESS_KEY")
        return

    user_data[user_id]['messages'].append(('u', message.text))
    user_data[user_id]['messages'] = user_data[user_id]['messages'][-10:]
    user_data[user_id]['cnt'] += len(str(message.text))
    async with as_lock:
        update_user_data()
    try:
        generated = generate(user_data[user_id])
        generated = _escape(generated)

        user_data[user_id]['messages'].append(('ai', generated))
        user_data[user_id]['messages'] = user_data[user_id]['messages'][-10:]
        user_data[user_id]['cnt'] += len(str(generated))

        print(user_data[user_id]['messages'])
        print(user_data[user_id]['user_name'], user_data[user_id]['user_name'], user_data[user_id]['cnt'])

        keyboard = create_keyboard()

        await message.answer(generated, reply_markup=keyboard)

        async with as_lock:
            update_user_data()

    except Exception as e:
        await message.answer(f'Произошла ошибка {str(e)}')


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    global bot
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


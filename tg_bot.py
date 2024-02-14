import asyncio
import logging
import sys
import os
from collections import defaultdict

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold
from aiogram.filters import Command, Filter
from aiogram.types import Message

# import cred.cred

from generator import generate


# Bot token can be obtained via https://t.me/BotFather
TOKEN = os.getenv("BOT_TOKEN")
ACCESS_KEY = os.getenv("ACCESS_KEY")

"""
user_data = {
    user_id: {
        'messages': list[tuple[role: str, text: str]]
        'system': str
    }
}
"""
users = set()

user_data: dict = defaultdict(lambda: {'messages': [], 'system': ''})

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """

    user_id  = message.chat.id
    text = message.text.split('/start')[-1].strip()
    if user_id in users or text == ACCESS_KEY:
        users.add(message.chat.id)
        await message.answer("Доступ получен. напишите ваше сообщение\n"
                             "Для установки системного сообщения напишите\n/system ваше сообщение\n"
                             "Бот помнит последние 10 сообщений\n"
                             "/info - для получения вашей информации\n"
                             "/reset - очистить историю сообщений\n"
                             )
    else:
        await message.answer("для доступа к боту введите /start ACCESS_KEY")


@dp.message(Command(commands=["system"]))
async def command_system_handler(message: Message) -> None:
    user_id = message.chat.id
    if user_id not in users:
        await message.answer("для доступа к боту введите /start ACCESS_KEY")
        return

    print(message.chat.id)
    print(message.text)
    text = message.text
    text = text.replace('/system', '').strip()
    user_data[user_id]['system'] = text
    await message.answer(f'Вы установили системное сообщение\n{text}')


@dp.message(Command(commands=["info"]))
async def command_system_handler(message: Message) -> None:
    user_id = message.chat.id
    if user_id not in users:
        await message.answer("для доступа к боту введите /start ACCESS_KEY")
        return

    data = f'Ваш телеграм чат ID: {message.chat.id}\n\n'
    data += f'system_message: {user_data["user_id"]["system"]}\n\n'
    data += 'История диалога:\n\n'
    for m in user_data[user_id]['messages']:
        data += f'role: {m[0]}\n{m[1]}\n\n'

    await message.answer(data)


@dp.message(Command(commands=["reset"]))
async def command_system_handler(message: Message) -> None:
    user_id = message.chat.id
    if user_id not in users:
        await message.answer("для доступа к боту введите /start ACCESS_KEY")
        return

    user_data[user_id]['messages'] = []
    await message.answer('история сообщений очищена')


@dp.message()
async def echo_handler(message: types.Message) -> None:
    user_id = message.chat.id
    if user_id not in users:
        await message.answer("для доступа к боту введите /start ACCESS_KEY")
        return

    user_data[user_id]['messages'].append(('u', message.text))
    user_data[user_id]['messages'] = user_data[user_id]['messages'][-10:]

    try:
        generated = generate(user_data[user_id])

        user_data[user_id]['messages'].append(('ai', generated))
        user_data[user_id]['messages'] = user_data[user_id]['messages'][-10:]

        print(user_data[user_id]['messages'])

        await message.answer(generated)
    except Exception as e:
        await message.answer(f'Произошла ошибка {str(e)}')


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


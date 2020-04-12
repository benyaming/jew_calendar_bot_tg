import asyncio
import logging

from psycopg2 import connect
from aiogram import Bot, Dispatcher, types
from aiogram.utils import exceptions, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import settings


logging.basicConfig(level=logging.INFO)
log = logging.getLogger('broadcast')

loop = asyncio.get_event_loop()
bot = Bot(token='905901843:AAEkpF2RoCXeRcTe9CuJ8pLBksOezsBjBlk', loop=loop, parse_mode=types.ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot, loop=loop)


def get_users():
    with connect(settings.DB_PARAMS) as conn:
        cur = conn.cursor()
        query = 'SELECT users.id, lang.lang FROM users ' \
                'JOIN lang ON users.id = lang.id ' \
                'LEFT JOIN omer_subscriptions on users.id = omer_subscriptions.user_id ' \
                'WHERE user_id IS NULL'
        cur.execute(query)
        for i in cur.fetchall():
            yield i
    # yield 5979588, 'English'


def get_button(lang: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(settings.button_texts.get(lang), callback_data='omer'))

    return keyboard


async def send_message(user_id: int, text: str, keyboard: InlineKeyboardMarkup) -> bool:
    try:
        await bot.send_message(user_id, text, reply_markup=keyboard, parse_mode='Markdown')
    except exceptions.BotBlocked:
        log.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text, keyboard=keyboard)  # Recursive call
    except exceptions.UserDeactivated:
        log.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.exception(f"Target [ID:{user_id}]: failed")
    else:
        log.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcaster() -> int:
    count = 0
    try:
        for user_id, lang in get_users():
            print(user_id, lang)
            # message = settings.messages.get(lang, 'English')
            # keyboard = get_button(lang)
            # if await send_message(user_id, message, keyboard):
            #     count += 1
            # await asyncio.sleep(.05)
    finally:
        log.info(f"{count} messages successful sent.")

    return count


if __name__ == '__main__':
    # Execute broadcaster
    executor.start(dp, broadcaster())

# -*- coding: utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler

from time import sleep
from os import path

import telebot
import db_operations
import settings
import text_handler
import callback_handler
import utils
import jcb_chatbase

from flask import Flask, request


route_path = f'/{settings.URI}/'

logger = logging.getLogger('bot_logger')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(
    path.join(
        settings.logs_path,
        'jcb_logfile.log'
    ),
    maxBytes=1024*1024*3,
    backupCount=20
)
formatter = logging.Formatter(
    fmt='%(filename)s[LINE:%(lineno)d]# ' 
    '%(levelname)-8s [%(asctime)s]  '
    '%(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

bot = telebot.TeleBot(settings.TOKEN)

app = Flask(__name__)


@app.route(route_path, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return 'ok'


@bot.message_handler(commands=['start'])
def handle_start(message: telebot.types.Message):
    jcb_chatbase.chatbase_user_msg_handler(
        message.from_user.id,
        message.text,
        'start_command'
    )
    bot.send_chat_action(message.from_user.id, 'typing')
    if settings.IS_SERVER:
        logger.info(
            f'Command: \'\\start\', from: {message.from_user.id}, START'
        )
    db_operations.check_id_in_db(message.from_user)
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.row('Русский', 'English')
    response = 'Выберите язык/Choose the language'
    bot.send_message(message.from_user.id, response, reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def handle_help(message: telebot.types.Message):
    jcb_chatbase.chatbase_user_msg_handler(
        message.from_user.id,
        message.text,
        'help_command'
    )
    bot.send_chat_action(message.from_user.id, 'typing')
    if settings.IS_SERVER:
        logger.info(
            f' Command: \'\\help\', from: {message.from_user.id}, START'
        )
    db_operations.check_id_in_db(message.from_user)
    text_handler.TextHandler(message.from_user.id, 'Help').handle_text()


@bot.message_handler(commands=['settings'])
def handle_start(message: telebot.types.Message):
    jcb_chatbase.chatbase_user_msg_handler(
        message.from_user.id,
        message.text,
        'settings_command'
    )
    bot.send_chat_action(message.from_user.id, 'typing')
    if settings.IS_SERVER:
        logger.info(
            f' Command: \'\\settings\', from: {message.from_user.id}, SETTINGS'
        )
    db_operations.check_id_in_db(message.from_user)
    text_handler.TextHandler(message.from_user.id, 'Settings').handle_text()


@bot.message_handler(commands=['language'])
def handle_start(message: telebot.types.Message):
    jcb_chatbase.chatbase_user_msg_handler(
        message.from_user.id,
        message.text,
        'language_command'
    )
    bot.send_chat_action(message.from_user.id, 'typing')
    if settings.IS_SERVER:
        logger.info(
            f' Command: \'\\language\', from: {message.from_user.id}, LANGUAGE'
        )
    db_operations.check_id_in_db(message.from_user)
    text_handler.TextHandler(message.from_user.id, 'Language').handle_text()


@bot.message_handler(commands=['location'])
def handle_start(message: telebot.types.Message):
    jcb_chatbase.chatbase_user_msg_handler(
        message.from_user.id,
        message.text,
        'location_command'
    )
    bot.send_chat_action(message.from_user.id, 'typing')
    if settings.IS_SERVER:
        logger.info(
            f' Command: \'\\location\', from: {message.from_user.id}, LOCATION'
        )
    db_operations.check_id_in_db(message.from_user)
    text_handler.TextHandler(message.from_user.id, 'Location').handle_text()


@bot.message_handler(commands=['converter'])
def handle_start(message: telebot.types.Message):
    jcb_chatbase.chatbase_user_msg_handler(
        message.from_user.id,
        message.text,
        'converter_command'
    )
    bot.send_chat_action(message.from_user.id, 'typing')
    if settings.IS_SERVER:
        logger.info(
            f' Command: \'\\converter\', from: {message.from_user.id}, '
            f'CONVERTER'
        )
    db_operations.check_id_in_db(message.from_user)
    text_handler.TextHandler(
        message.from_user.id,
        'Date converter'
    ).handle_text()


@bot.message_handler(commands=['report'])
def handle_report(message: telebot.types.Message):
    jcb_chatbase.chatbase_user_msg_handler(
        message.from_user.id,
        message.text,
        'report_command'
    )
    bot.send_chat_action(message.from_user.id, 'typing')
    if settings.IS_SERVER:
        logger.info(
            f' Command: \'\\help\', from: {message.from_user.id}, REPORT'
        )
    db_operations.check_id_in_db(message.from_user)
    text_handler.TextHandler(
        message.from_user.id,
        'Report a bug'
    ).handle_text()


@bot.message_handler(
    func=lambda message: True, content_types=['location', 'venue']
)
def handle_venue(message: telebot.types.Message):
    jcb_chatbase.chatbase_user_msg_handler(
        message.from_user.id,
        message.text,
        'geotag received'
    )
    bot.send_chat_action(message.from_user.id, 'typing')
    db_operations.check_id_in_db(message.from_user)
    if db_operations.check_location(
            message.from_user.id,
            message.location.latitude,
            message.location.longitude,
            bot
    ):
        text_handler.TextHandler(message.from_user.id, 'Back').handle_text()
        tz = utils.get_tz_by_location(
            db_operations.get_location_by_id(message.from_user.id)
        )
        db_operations.check_tz(message.from_user.id, tz)


@bot.message_handler(regexp=r'^-?\d{1,2}\.{1}\d+, {0,1}-?\d{1,3}\.{1}\d+$')
def handle_reg(message: telebot.types.Message):
    jcb_chatbase.chatbase_user_msg_handler(
        message.from_user.id,
        message.text,
        'text location received'
    )
    bot.send_chat_action(message.from_user.id, 'typing')
    db_operations.check_id_in_db(message.from_user)
    loc = message.text.split(sep=', ')
    if loc[0] == message.text:
        loc = message.text.split(sep=',')
    if db_operations.check_location(message.from_user.id, loc[0], loc[1], bot):
        tz = utils.get_tz_by_location(
            db_operations.get_location_by_id(message.from_user.id)
        )
        db_operations.check_tz(message.from_user.id, tz)
        text_handler.TextHandler(message.from_user.id, 'Back').handle_text()


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text_message(message: telebot.types.Message):
    db_operations.check_id_in_db(message.from_user)
    text_handler.TextHandler(message.from_user.id, message.text).handle_text()


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call: telebot.types.CallbackQuery):
    callback_handler.CallbackHandler(call.from_user.id, call).handle_call()


if __name__ == '__main__':
    if settings.IS_SERVER:
        logger.info('STARTING WEBHOOK...')

    else:
        logger.info('STARTING POLLING....')
        bot.remove_webhook()
        sleep(1)
        bot.polling(True, timeout=50)

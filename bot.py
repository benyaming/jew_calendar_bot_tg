# -*- coding: utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler
from time import sleep

import telebot
import db_operations

import settings
import text_handler
import utils as f

import tornado.web

from tornado import httpserver
from tornado.web import HTTPError
from tornado.escape import json_decode
from tornado.ioloop import IOLoop


WEBHOOK_HOST = settings.BOT_HOST
WEBHOOK_PORT = settings.BOT_PORT
WEBHOOK_SSL_CERT = '/hdd/certs/webhook_cert.pem'
WEBHOOK_SSL_PRIV = '/hdd/certs//webhook_pkey.pem'
WEBHOOK_URL_BASE = f'{WEBHOOK_HOST}:{WEBHOOK_PORT}'
WEBHOOK_URL_PATH = f'/{settings.TOKEN}/'


bot = telebot.TeleBot(settings.TOKEN)


class WebhookServer(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def post(self):
        headers = self.request.headers
        if 'content-length' in headers and 'content-type' in headers and \
                headers['content-type'] == 'application/json':

            json_string = json_decode(self.request.body)
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
        else:
            raise HTTPError(403)


application = tornado.web.Application([
    (WEBHOOK_URL_PATH, WebhookServer),
])


@bot.message_handler(commands=['start'])
def handle_start(message):
    if settings.IS_SERVER:
        logger.info(f' Command: \'\start\', from: {message.from_user.id}, START')
    db_operations.check_id_in_db(message.from_user)
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Русский', 'English')
    bot.send_message(message.from_user.id,
                     'Выберите язык/Choose the language',
                     reply_markup=user_markup
                     )


@bot.message_handler(commands=['help'])
def handle_help(message):
    if settings.IS_SERVER:
        logger.info(f' Command: \'\help\', from: {message.from_user.id}, START')
    db_operations.check_id_in_db(message.from_user)
    menu = telebot.types.ReplyKeyboardMarkup(True, False)
    menu.row('🇷🇺', '🇱🇷', 'Назад/Back')
    help_str = 'Пожалуйста, выберите язык справки'
    bot.send_message(message.from_user.id,
                     help_str,
                     reply_markup=menu)


@bot.message_handler(commands=['report'])
def handle_report(message):
    if settings.IS_SERVER:
        logger.info(f' Command: \'\help\', from: {message.from_user.id}, REPORT')
    db_operations.check_id_in_db(message.from_user)
    report_str = 'Чтобы сообщить об ошибке, пожалуйста, напишите сюда: \n' \
                 't.me/benyomin, или сюда: \nt.me/Meir_Yartzev. \nПожалуйста,'\
                 ' убедитесь, что вы ознакомились с часто задаваемыми' \
                 ' вопросами, доступными по команде /help\n\nFor bug report ' \
                 'please write to \nt.me/benyomin or \nt.me/Meir_Yartzev. ' \
                 '\nPlease, make sure that you had been read '\
                 'F.A.Q. available by command /help'
    bot.send_message(message.from_user.id,
                     report_str,
                     disable_web_page_preview=True)


@bot.message_handler(func=lambda message: True, content_types=['location',
                                                               'venue'])
def handle_venue(message):
    db_operations.check_id_in_db(message.from_user)
    if db_operations.check_location(
            message.from_user.id,
            message.location.latitude,
            message.location.longitude,
            bot
    ):
        text_handler.handle_text(message.from_user.id, 'Back')
        tz = f.get_tz_by_location(
            db_operations.get_location_by_id(message.from_user.id))
        db_operations.check_tz(message.from_user.id, tz)
        # 'Получил геометку')


@bot.message_handler(regexp=r'^-?\d{1,2}\.{1}\d+, {0,1}-?\d{1,3}\.{1}\d+$')
def handle_reg(message):
    db_operations.check_id_in_db(message.from_user)
    loc = message.text.split(sep=', ')
    if loc[0] == message.text:
        loc = message.text.split(sep=',')
    if db_operations.check_location(message.from_user.id, loc[0], loc[1], bot):
        text_handler.handle_text(message.from_user.id, 'Back')
        tz = f.get_tz_by_location(
            db_operations.get_location_by_id(message.from_user.id))
        db_operations.check_tz(message.from_user.id, tz)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text_message(message):
    db_operations.check_id_in_db(message.from_user)
    text_handler.handle_text(message.from_user.id, message.text)


if __name__ == '__main__':
    if settings.IS_SERVER:
        logger = logging.getLogger('bot_logger')
        logger.setLevel(logging.INFO)
        handler = RotatingFileHandler('/hdd/logs/bot_logger',
                                      maxBytes=1024*1024*3,
                                      backupCount=20)
        formatter = logging.Formatter(fmt='%(filename)s[LINE:%(lineno)d]# ' 
                                          '%(levelname)-8s [%(asctime)s]  '
                                          '%(message)s'
                                      )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        server = httpserver.HTTPServer(
            application,
            ssl_options={
                "certfile": WEBHOOK_SSL_CERT,
                "keyfile": WEBHOOK_SSL_PRIV,
            }
        )

        bot.remove_webhook()
        sleep(2)
        bot.set_webhook(
            url=f'{WEBHOOK_URL_BASE}{WEBHOOK_URL_PATH}',
            certificate=open(WEBHOOK_SSL_CERT, 'r')
        )
        server.listen(WEBHOOK_PORT)
        IOLoop().current().start()
    else:
        bot.remove_webhook()
        sleep(2)
        bot.polling(True)
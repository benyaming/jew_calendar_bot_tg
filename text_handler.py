# -*- coding: utf-8 -*-
import re
from datetime import datetime

from telebot import TeleBot

import db_operations
import keyboards
import zmanim, converter, localization, data
import shabbos
import rosh_hodesh
import daf
import settings
import states
import jcb_chatbase

import localization as l
import holidays as h


def get_zmanim():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'zmanim'
    )
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        response = zmanim.get_zmanim(user, lang)
        if response['polar_error']:
            bot.send_chat_action(user, 'typing')
            response_message = response['polar_error']
            bot.send_message(user, response_message)
            jcb_chatbase.chatbase_bot_handler(user, 'zmanim polar error')
        elif response['zmanim_set_error']:
            bot.send_chat_action(user, 'typing')
            response_message = response['zmanim_set_error']
            user_markup = keyboards.get_zmanim_callback_menu(lang, user)
            bot.send_message(user, response_message, reply_markup=user_markup)
            jcb_chatbase.chatbase_bot_handler(user, 'zmanim set error')
        else:
            bot.send_chat_action(user, 'upload_photo')
            response_pic = response['zmanim_pic']
            bot.send_photo(user, response_pic)
            response_pic.close()
            jcb_chatbase.chatbase_bot_handler(user, 'zmanim sent')


def request_date():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'zmanim by the date'
    )
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        request_location()
    else:
        bot.send_chat_action(user, 'typing')
        states.set_state(user, 'waiting_for_date')
        response = l.Utils.request_date(lang)
        keyboard = keyboards.get_cancel_keyboard(lang)
        bot.send_message(
            user,
            response,
            parse_mode='Markdown',
            reply_markup=keyboard
        )
        jcb_chatbase.chatbase_bot_handler(user, 'request date for zmanim sent')


def handle_date():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'received custom date'
    )
    reg_pattern = r'^[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,4}$'
    extracted_date = re.search(reg_pattern, text)
    if extracted_date:
        day = int(extracted_date.group().split('.')[0])
        month = int(extracted_date.group().split('.')[1])
        year = int(extracted_date.group().split('.')[2])
        try:
            datetime(year, month, day)
            get_zmanim_by_the_date(day, month, year)
            main_menu()
        except ValueError:
            incorrect_date('incorrect_date_value')
            jcb_chatbase.chatbase_bot_handler(user, 'incorrect date value')
    else:
        incorrect_date('incorrect_date_format')
        jcb_chatbase.chatbase_bot_handler(user, 'incorrect date format')


def get_zmanim_by_the_date(day: int, month: int, year: int):
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        states.delete_state(user)
        result = request_location
    else:
        custom_date = (year, month, day)
        response = zmanim.get_zmanim(user, lang, custom_date)
        if response['polar_error']:
            bot.send_chat_action(user, 'typing')
            response_message = response['polar_error']
            bot.send_message(user, response_message)
            jcb_chatbase.chatbase_bot_handler(user, 'zmanim polar error')
        elif response['zmanim_set_error']:
            bot.send_chat_action(user, 'typing')
            response_message = response['zmanim_set_error']
            user_markup = keyboards.get_zmanim_callback_menu(lang, user)
            bot.send_message(user, response_message, reply_markup=user_markup)
            jcb_chatbase.chatbase_bot_handler(user, 'zmanim set error')
        else:
            bot.send_chat_action(user, 'upload_photo')
            response_pic = response['zmanim_pic']
            bot.send_photo(user, response_pic)
            response_pic.close()
            states.delete_state(user)
            jcb_chatbase.chatbase_bot_handler(user, 'zmanim by the date sent')
        result = main_menu
    return result


def incorrect_date(error_type: str) -> None:
    bot.send_chat_action(user, 'typing')
    responses = {
        'incorrect_date_format': l.Utils.incorrect_date_format(lang),
        'incorrect_date_value': l.Utils.incorrect_date_value(lang),
        'incorrect_heb_date_format': l.Converter.incorrect_heb_date_format(
            lang
        ),
        'incorrect_heb_date_value': l.Converter.incorrect_heb_date_value(lang)
    }
    response = responses.get(error_type, '')
    keyboard = keyboards.get_cancel_keyboard(lang)
    bot.send_message(
        user,
        response,
        parse_mode='Markdown',
        reply_markup=keyboard
    )


def shabbat():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'shabbos'
    )
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        bot.send_chat_action(user, 'upload_photo')
        response_pic = shabbos.get_shabbos(loc, lang, user)
        bot.send_photo(user, response_pic)
        response_pic.close()
        jcb_chatbase.chatbase_bot_handler(user, 'shabbos sent')


def rosh_chodesh() -> None:
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'rosh chodesh'
    )
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        bot.send_chat_action(user, 'upload_photo')
        response_pic = rosh_hodesh.get_rh(loc, lang)
        bot.send_photo(user, response_pic)
        response_pic.close()
        jcb_chatbase.chatbase_bot_handler(user, 'rosh chodesh sent')


def holidays():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'holidays menu'
    )
    bot.send_chat_action(user, 'typing')
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        response = l.Utils.get_holiday_menu(lang)
        holiday_menu = keyboards.get_holiday_menu(lang)
        bot.send_message(user, response, reply_markup=holiday_menu)
        jcb_chatbase.chatbase_bot_handler(user, 'open holidays menu')


def fasts():
    bot.send_chat_action(user, 'typing')
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'holidays menu'
    )
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        response = l.Utils.get_fast_menu(lang)
        fast_menu = keyboards.get_fast_menu(lang)
        bot.send_message(user, response, reply_markup=fast_menu)
        jcb_chatbase.chatbase_bot_handler(user, 'open fasts menu')


def daf_yomi() -> None:
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'daf yomi'
    )
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        bot.send_chat_action(user, 'upload_photo')
        response_pic = daf.get_daf(loc, lang)
        bot.send_photo(user, response_pic)
        response_pic.close()
        jcb_chatbase.chatbase_bot_handler(user, 'daf yomi sent')


def update_location():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'update location'
    )
    bot.send_chat_action(user, 'typing')
    geobutton = keyboards.get_geobutton(lang, True)
    response = l.Utils.request_location(lang)
    bot.send_message(
        user,
        response,
        reply_markup=geobutton,
        parse_mode='Markdown'
    )
    jcb_chatbase.chatbase_bot_handler(user, 'open menu update location')


def request_location():
    bot.send_chat_action(user, 'typing')
    geobutton = keyboards.get_geobutton(lang)
    response = l.Utils.request_location(lang)
    bot.send_message(
        user,
        response,
        reply_markup=geobutton,
        parse_mode='Markdown'
    )
    jcb_chatbase.chatbase_bot_handler(user, 'request location')


def set_lang():
    db_operations.set_lang(user, lang)
    return main_menu()


def main_menu():
    auth = db_operations.get_location_by_id(user)
    if not auth:
        request_location()
    else:
        user_markup = keyboards.get_main_menu(lang)
        response = l.Utils.get_main_menu(lang)
        bot.send_message(user, response, reply_markup=user_markup)
        jcb_chatbase.chatbase_bot_handler(user, 'open main menu')


def faq():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'faq'
    )
    auth = db_operations.get_location_by_id(user)
    if not auth:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        request_location()
    bot.send_chat_action(user, 'typing')
    responses = {
        'Russian': 'http://telegra.ph/Hebrew-Calendar-Bot-FAQ-05-10',
        'English': 'http://telegra.ph/Hebrew-Calendar-Bot-FAQ-EN-05-10'
    }
    response = responses.get(lang, '')
    bot.send_message(user, response)
    jcb_chatbase.chatbase_bot_handler(user, 'faq sent')


def report():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'report'
    )
    bot.send_chat_action(user, 'typing')
    auth = db_operations.get_location_by_id(user)
    if not auth:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        request_location()
    else:
        response = l.Utils.report(lang)
        bot.send_message(user, response, disable_web_page_preview=True)
        jcb_chatbase.chatbase_bot_handler(user, 'report message sent')


def more_holiday_menu():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'more holidays menu'
    )
    auth = db_operations.get_location_by_id(user)
    if not auth:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        user_markup = keyboards.get_more_holiday_menu(lang)
        response = l.Utils.get_more_holiday_menu(lang)
        bot.send_message(user, response, reply_markup=user_markup)
        jcb_chatbase.chatbase_bot_handler(user, 'open more holidays menu')


def rosh_hashana():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'rosh hashana'
    )
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        bot.send_chat_action(user, 'upload_photo')
        response_pic = h.get_holiday_pic('Rosh Hashana', user, lang)
        bot.send_photo(user, response_pic)
        response_pic.close()
        jcb_chatbase.chatbase_bot_handler(user, 'rosh hashana sent')


def yom_kippur():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'rosh hashana'
    )
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        bot.send_chat_action(user, 'upload_photo')
        response_pic = h.get_holiday_pic('Yom Kippur', user, lang)
        bot.send_photo(user, response_pic)
        response_pic.close()
        jcb_chatbase.chatbase_bot_handler(user, 'yom kippur sent')


def succot():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'succos'
    )
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        bot.send_chat_action(user, 'upload_photo')
        response_pic = h.get_holiday_pic('Succos', user, lang)
        bot.send_photo(user, response_pic)
        response_pic.close()
        jcb_chatbase.chatbase_bot_handler(user, 'succos sent')


def shmini_atzeret():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'shmini atzeres'
    )
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        bot.send_chat_action(user, 'upload_photo')
        response_pic = h.get_holiday_pic('Shmini Atzeres', user, lang)
        bot.send_photo(user, response_pic)
        response_pic.close()
        jcb_chatbase.chatbase_bot_handler(user, 'shmini atzeres sent')


def chanukah():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'chanukah'
    )
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        bot.send_chat_action(user, 'upload_photo')
        response_pic = h.get_holiday_pic('Chanuka', user, lang)
        bot.send_photo(user, response_pic)
        response_pic.close()
        jcb_chatbase.chatbase_bot_handler(user, 'chanukah sent')


def tu_beshvat():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'tu bishvat'
    )
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        bot.send_chat_action(user, 'upload_photo')
        response_pic = h.get_holiday_pic('Tu B\'shvat', user, lang)
        bot.send_photo(user, response_pic)
        response_pic.close()
        jcb_chatbase.chatbase_bot_handler(user, 'tu bishvat sent')


def purim():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'purim'
    )
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        bot.send_chat_action(user, 'upload_photo')
        response_pic = h.get_holiday_pic('Purim', user, lang)
        bot.send_photo(user, response_pic)
        response_pic.close()
        jcb_chatbase.chatbase_bot_handler(user, 'purim sent')


def pesach():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'pesach'
    )
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        bot.send_chat_action(user, 'upload_photo')
        response_pic = h.get_holiday_pic('Pesach', user, lang)
        bot.send_photo(user, response_pic)
        response_pic.close()
        jcb_chatbase.chatbase_bot_handler(user, 'pesach sent')


def lag_baomer():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'lag baomer'
    )
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        bot.send_chat_action(user, 'upload_photo')
        response_pic = h.get_holiday_pic('Lag Ba\'omer', user, lang)
        bot.send_photo(user, response_pic)
        response_pic.close()
        jcb_chatbase.chatbase_bot_handler(user, 'lag baomer sent')


def shavuot():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'shavuos'
    )
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        bot.send_chat_action(user, 'upload_photo')
        response_pic = h.get_holiday_pic('Shavuos', user, lang)
        bot.send_photo(user, response_pic)
        response_pic.close()
        jcb_chatbase.chatbase_bot_handler(user, 'shavuos sent')


def israel():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'israel'
    )
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        bot.send_chat_action(user, 'upload_photo')
        response_pic = h.get_holiday_pic('israel_holidays', user, lang)
        bot.send_photo(user, response_pic)
        response_pic.close()
        jcb_chatbase.chatbase_bot_handler(user, 'israel sent')


def fast_gedaliah():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'fast gedaliah'
    )
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        bot.send_chat_action(user, 'upload_photo')
        response_pic = h.get_holiday_pic('Tzom Gedalia', user, lang)
        bot.send_photo(user, response_pic)
        response_pic.close()
        jcb_chatbase.chatbase_bot_handler(user, 'fast gedaliah sent')


def asarah_betevet():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        '10 of tevet'
    )
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        bot.send_chat_action(user, 'upload_photo')
        response_pic = h.get_holiday_pic('10 of Teves', user, lang)
        bot.send_photo(user, response_pic)
        response_pic.close()
        jcb_chatbase.chatbase_bot_handler(user, '10 of tevet sent')


def fast_esther():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'fast esther'
    )
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        bot.send_chat_action(user, 'upload_photo')
        response_pic = h.get_holiday_pic('Taanis Esther', user, lang)
        bot.send_photo(user, response_pic)
        response_pic.close()
        jcb_chatbase.chatbase_bot_handler(user, 'fast esther sent')


def sheva_asar_betammuz():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        '17 of tammuz'
    )
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        bot.send_chat_action(user, 'upload_photo')
        response_pic = h.get_holiday_pic('17 of Tamuz', user, lang)
        bot.send_photo(user, response_pic)
        response_pic.close()
        jcb_chatbase.chatbase_bot_handler(user, '17 of tammuz sent')


def tisha_beav():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        '9 of av'
    )
    loc = db_operations.get_location_by_id(user)
    if not loc:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        return request_location()
    else:
        bot.send_chat_action(user, 'upload_photo')
        response_pic = h.get_holiday_pic('9 of Av', user, lang)
        bot.send_photo(user, response_pic)
        response_pic.close()
        jcb_chatbase.chatbase_bot_handler(user, '9 of av sent')


def change_lang():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'change lang'
    )
    response = 'Выберите язык/Choose the language'
    lang_markup = keyboards.get_lang_menu()
    bot.send_message(user, response, reply_markup=lang_markup)
    jcb_chatbase.chatbase_bot_handler(user, 'open language menu')


def incorrect_text():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'not handled',
        not_handled=True
    )
    bot.send_chat_action(user, 'typing')
    response = l.Utils.incorrect_text(lang)
    bot.send_message(user, response)


def settings_menu():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'settings menu'
    )
    auth = db_operations.get_location_by_id(user)
    if not auth:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        request_location()
    else:
        user_markup = keyboards.get_settings_menu(lang)
        responses = {
            'Russian': 'Добро пожаловать в настройки!',
            'English': 'Welcome to settings!',
            # TODO
        }
        response = responses.get(lang, '')
        bot.send_message(user, response, reply_markup=user_markup)
        jcb_chatbase.chatbase_bot_handler(user, 'open settings menu')


def select_zmanim():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'select zmanim'
    )
    auth = db_operations.get_location_by_id(user)
    if not auth:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        request_location()
    else:
        bot.send_chat_action(user, 'typing')
        user_markup = keyboards.get_zmanim_callback_menu(lang, user)
        responses = {
            'Russian': 'Выберите зманим для отображения',
            'English': 'Choose zmanim that will shown',
            'Hebrew': ''  # TODO hebrew
        }
        response = responses.get(lang, '')
        bot.send_message(user, response, reply_markup=user_markup)
        jcb_chatbase.chatbase_bot_handler(user, 'open zmanim options')


def select_candle_offset():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'select candle offset'
    )
    auth = db_operations.get_location_by_id(user)
    if not auth:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        request_location()
    else:
        bot.send_chat_action(user, 'typing')
        user_markup = keyboards.get_candle_offset_callback_menu(user)
        response = l.Shabos.shabos_candle_offset(lang)
        bot.send_message(user, response, reply_markup=user_markup)
        jcb_chatbase.chatbase_bot_handler(user, 'open candle offset options')


def select_diaspora():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'select diaspora'
    )
    auth = db_operations.get_location_by_id(user)
    if not auth:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        request_location()
    else:
        bot.send_chat_action(user, 'typing')
        user_markup = keyboards.get_diaspora_callback_menu(lang, user)
        diaspora_status = db_operations.get_diaspora_status(user)
        response = l.Utils.diaspora(lang, diaspora_status)
        print(1, response)
        bot.send_message(
            user,
            response,
            reply_markup=user_markup,
            parse_mode='Markdown'
        )
        jcb_chatbase.chatbase_bot_handler(user, 'open diaspora options')


def converter_startup():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'converter'
    )
    auth = db_operations.get_location_by_id(user)
    if not auth:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        request_location()
    else:
        bot.send_chat_action(user, 'typing')
        response = l.Converter.welcome_to_converter(lang)
        markup = keyboards.get_converter_menu(lang)
        bot.send_message(user, response, reply_markup=markup)
        jcb_chatbase.chatbase_bot_handler(user, 'open converter menu')


def converter_greg_to_heb():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'convert greg -> heb'
    )
    bot.send_chat_action(user, 'typing')
    auth = db_operations.get_location_by_id(user)
    if not auth:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        request_location()
    else:
        states.set_state(user, 'waiting_for_greg_date')
        response = l.Converter.request_date_for_converter_greg(lang)
        keyboard = keyboards.get_cancel_keyboard(lang)
        bot.send_message(
            user,
            response,
            parse_mode='Markdown',
            reply_markup=keyboard
        )
        jcb_chatbase.chatbase_bot_handler(user, 'ask for date to convert')


def convert_heb_to_greg():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'convert heb -> greg'
    )
    bot.send_chat_action(user, 'typing')
    auth = db_operations.get_location_by_id(user)
    if not auth:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        request_location()
    else:
        states.set_state(user, 'waiting_for_heb_date')
        response = l.Converter.request_date_for_converter_heb(lang)
        keyboard = keyboards.get_cancel_keyboard(lang)
        bot.send_message(
            user,
            response,
            parse_mode='Markdown',
            reply_markup=keyboard
        )
        jcb_chatbase.chatbase_bot_handler(user, 'ask for date to convert')


def handle_greg_date():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'handle greg date'
    )
    bot.send_chat_action(user, 'typing')
    reg_pattern = r'^[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,4}$'
    extracted_date = re.search(reg_pattern, text)
    if extracted_date:
        day = int(extracted_date.group().split('.')[0])
        month = int(extracted_date.group().split('.')[1])
        year = int(extracted_date.group().split('.')[2])
        try:
            datetime(year, month, day)
            date = (year, month, day)
            response = converter.convert_greg_to_heb(date, lang)
            keyboard = keyboards.get_zmanim_for_converter_button(date, lang)
            bot.send_message(
                user,
                response,
                parse_mode='Markdown',
                reply_markup=keyboard
            )
            states.delete_state(user)
            main_menu()
            jcb_chatbase.chatbase_bot_handler(user, 'greg date converted')
        except Exception as e:
            incorrect_date('incorrect_date_value')
            jcb_chatbase.chatbase_bot_handler(user, 'incorrect date value')
    else:
        incorrect_date('incorrect_date_format')
        jcb_chatbase.chatbase_bot_handler(user, 'incorrect date format')


def handle_heb_date():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'handle heb date'
    )
    bot.send_chat_action(user, 'typing')
    year, month, day = None, None, None
    input_data = text.split()
    if len(input_data) in [3, 4]:
        # check day
        if input_data[0].isdigit():
            day = int(input_data[0])
            if not 0 < day < 31:
                return incorrect_date('incorrect_heb_date_value')
        # check month
        if len(input_data) == 3:
            # all exept adar ii
            if input_data[1].lower() in data.heb_months_names_ru or \
                    input_data[1].lower() in data.heb_months_names_en or \
                    input_data[1].lower() in data.heb_months_names_he:
                month = localization.Converter.get_month_name(
                    lang,
                    input_data[1].lower()
                )
        elif len(input_data) == 4 \
                and input_data[1].lower() in ['adar', 'адар', 'qqqq'] \
                and input_data[2] in ['1', '2']:
            month = localization.Converter.get_month_name(
                lang,
                f'{input_data[1].lower()} {input_data[2]}'
            )
        else:
            return incorrect_date('incorrect_heb_date_format')
        # check year
        if input_data[-1].isdigit():
            year = int(input_data[-1])
            if year < 0:
                return incorrect_date('incorrect_heb_date_value')
            # final calculation
            else:
                hebrew_date = (year, month, day)
                response = converter.convert_heb_to_greg(hebrew_date, lang)
                if response:
                    message_text = response['response']
                    keyboard = keyboards.get_zmanim_for_converter_button(
                        response['date'],
                        lang
                    )
                    bot.send_message(
                        user,
                        message_text,
                        parse_mode='Markdown',
                        reply_markup=keyboard
                    )
                    states.delete_state(user)
                    jcb_chatbase.chatbase_bot_handler(
                        user,
                        'heb date converted'
                    )
                    main_menu()
                else:
                    return incorrect_date('incorrect_heb_date_value')
                jcb_chatbase.chatbase_bot_handler(user, 'incorrect date value')
    else:
        return incorrect_date('incorrect_heb_date_format')
    jcb_chatbase.chatbase_bot_handler(user, 'incorrect date format')


def get_help():
    jcb_chatbase.chatbase_user_msg_handler(
        user,
        text,
        'help'
    )
    auth = db_operations.get_location_by_id(user)
    if not auth:
        jcb_chatbase.chatbase_bot_handler(user, 'location missed')
        request_location()
    else:
        bot.send_chat_action(user, 'typing')
        response = localization.Utils.help_menu(lang)
        keyboard = keyboards.get_help_menu(lang)
        bot.send_message(user, response, reply_markup=keyboard)
        jcb_chatbase.chatbase_bot_handler(user, 'open help menu')


def handle_text(user_id: int, message: str) -> None:
    global bot, user, lang, text
    bot = TeleBot(settings.TOKEN)
    user = user_id
    text = message
    if message in ['Русский', 'English', 'Hebrew']:
        langs = {
            'Русский': 'Russian',
            'English': 'English',
            'Hebrew': 'Hebrew'
        }
        lang = langs.get(message, '')
    else:
        lang = db_operations.get_lang_from_redis(user)
    user_has_state = states.check_state(user_id)
    if user_has_state['ok']:
        if text in ['Отмена', 'Cancel']:
            states.delete_state(user)
            main_menu()
        else:
            user_states = {
                'waiting_for_date': handle_date,
                'waiting_for_greg_date': handle_greg_date,
                'waiting_for_heb_date': handle_heb_date

            }
            func = user_states.get(user_has_state['state'], '')
            return func()
    else:
        messages = {
            'Язык': change_lang,
            'Language': change_lang,
            'Отмена': main_menu,
            'Cancel': main_menu,
            'Русский': set_lang,
            'English': set_lang,
            'Hebrew': set_lang,
            'Назад/Back': change_lang,
            'Зманим': get_zmanim,
            'Zmanim': get_zmanim,
            'זמנים': get_zmanim,
            'Зманим по дате': request_date,
            'Zmanim by the date': request_date,
            'Шаббат': shabbat,
            'Shabbos': shabbat,
            'שבת': shabbat,
            'Рош Ходеш': rosh_chodesh,
            'Rosh Chodesh': rosh_chodesh,
            'ראש חודש': rosh_chodesh,
            'Праздники': holidays,
            'Holidays': holidays,
            'חגים': holidays,
            'Посты': fasts,
            'Fast days': fasts,
            'כהנה': fasts,
            'Даф Йоми': daf_yomi,
            'Daf Yomi': daf_yomi,
            'דף יומי': daf_yomi,
            'Местоположение': update_location,
            'Location': update_location,
            'Назад': main_menu,
            'Back': main_menu,
            'ЧаВо': faq,
            'F.A.Q.': faq,
            '🇷🇺': faq,
            '🇱🇷': faq,
            'Ещё...': more_holiday_menu,
            'More...': more_holiday_menu,
            'Основные праздники': holidays,
            'Main holidays': holidays,
            'Main menu': main_menu,
            'Главное меню': main_menu,
            'Рош Ашана': rosh_hashana,
            'Rosh HaShanah': rosh_hashana,
            'ראש השנה': rosh_hashana,
            'Йом Кипур': yom_kippur,
            'Yom Kippur': yom_kippur,
            'יום כיפור': yom_kippur,
            'Суккот': succot,
            'Succos': succot,
            'סוכות': succot,
            'Шмини Ацерет': shmini_atzeret,
            'Shmini Atzeres': shmini_atzeret,
            'שמיני עצרת': shmini_atzeret,
            'Ханука': chanukah,
            'Chanukah': chanukah,
            'חנוכה': chanukah,
            'Ту биШват': tu_beshvat,
            'Tu BShevat': tu_beshvat,
            'ט"ו בשבט': tu_beshvat,
            'Пурим': purim,
            'Purim': purim,
            'פורים': purim,
            'Пейсах': pesach,
            'Pesach': pesach,
            'פסח': pesach,
            'Лаг баОмер': lag_baomer,
            'Lag BaOmer': lag_baomer,
            'ל"ג בעומר': lag_baomer,
            'Шавуот': shavuot,
            'Shavuot': shavuot,
            'שבועות': shavuot,
            'Израильские праздники': israel,
            'Israel holidays': israel,
            'Пост Гедалии': fast_gedaliah,
            'Fast of Gedaliah': fast_gedaliah,
            'צום גדליה': fast_gedaliah,
            '10 Тевета': asarah_betevet,
            '10 of Tevet': asarah_betevet,
            'עשרה בטבת': asarah_betevet,
            'Пост Эстер': fast_esther,
            'Fast of Esther': fast_esther,
            'תענית אסתר': fast_esther,
            '17 Таммуза': sheva_asar_betammuz,
            '17 of Tammuz': sheva_asar_betammuz,
            'שבעה עשר בתמוז': sheva_asar_betammuz,
            '9 Ава': tisha_beav,
            '9 of Av': tisha_beav,
            'תשעה באב': tisha_beav,
            'Настройки': settings_menu,
            'Settings': settings_menu,
            'Выбрать зманим': select_zmanim,
            'Select zmanim': select_zmanim,
            'Зажигание свечей': select_candle_offset,
            'Candle lighting': select_candle_offset,
            'Диаспора': select_diaspora,
            'Diaspora': select_diaspora,
            'Конвертер дат': converter_startup,
            'Date converter': converter_startup,
            'Григорианский ➡️ Еврейский': converter_greg_to_heb,
            'Gregorian ➡️ Hebrew': converter_greg_to_heb,
            'Еврейский ➡️ Григорианский': convert_heb_to_greg,
            'Hebrew ➡️ Gregorian': convert_heb_to_greg,
            'Помощь': get_help,
            'Help': get_help,
            'Сообщить об ошибке': report,
            'Report a bug': report

        }
        func = messages.get(message, incorrect_text)
        return func()

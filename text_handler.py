# -*- coding: utf-8 -*-
import re
from datetime import datetime

from telebot import TeleBot

import db_operations
import keyboards as kbrd
import zmanim
import converter as conv
import localization as locale
import data
import shabbos
import rosh_hodesh
import daf
import settings
import states
import jcb_chatbase
import holidays


def check_auth(func):
    def wrapper(instanse, *args):
        auth = db_operations.get_location_by_id(instanse._user_id)
        if not auth:
            instanse._chatbase('location missed')
            instanse._request_location()
        else:
            return func(instanse, *args)
    return wrapper


class TextHandler(object):

    def __init__(self, user_id: int, text: str):
        self._bot = TeleBot(settings.TOKEN)
        self._user_id = user_id
        self._text = text
        if self._text in ['Русский', 'English']:
            self._lang = self._langs.get(self._text, '')
        else:
            self._lang = db_operations.get_lang_from_redis(self._user_id)

    def _chatbase(self, intent: str, agent='bot', not_handled=False):
        if agent == 'user':
            jcb_chatbase.chatbase_user_msg_handler(
                self._user_id,
                self._text,
                intent,
                not_handled
            )
        elif agent == 'bot':
            jcb_chatbase.chatbase_bot_handler(self._user_id, intent)

    def handle_text(self):
        user_has_state = states.check_state(self._user_id)
        if user_has_state['ok']:
            if self._text in ['Отмена', 'Cancel']:
                states.delete_state(self._user_id)
                self._main_menu()
            else:
                func = self._user_states.get(user_has_state['state'])
                return func(self)
        else:
            func = self._handlers.get(self._text)
            if func:
                func(self)
            else:
                self._incorrect_text()

###############################################################################
#                      MENU, LANGUAGE, LOCATION, HELP                         #
###############################################################################

    @check_auth
    def _main_menu(self):
        user_markup = kbrd.get_main_menu(self._lang)
        response = locale.Utils.get_main_menu(self._lang)
        self._bot.send_message(
            self._user_id,
            response,
            reply_markup=user_markup
        )
        self._chatbase('open main menu')

    def _change_lang(self):
        self._chatbase('change lang', 'user')
        response = 'Выберите язык/Choose the language'
        lang_markup = kbrd.get_lang_menu()
        self._bot.send_message(
            self._user_id,
            response,
            reply_markup=lang_markup
        )
        self._chatbase('open language menu')

    def _set_lang(self):
        db_operations.set_lang(self._user_id, self._lang)
        self._main_menu()

    def _request_location(self):
        self._bot.send_chat_action(self._user_id, 'typing')
        geobutton = kbrd.get_geobutton(self._lang)
        response = locale.Utils.request_location(self._lang)
        self._bot.send_message(
            self._user_id,
            response,
            reply_markup=geobutton,
            parse_mode='Markdown'
        )
        self._chatbase('request location')

    def _update_location(self):
        self._chatbase('update location', 'user')
        self._bot.send_chat_action(self._user_id, 'typing')
        geobutton = kbrd.get_geobutton(self._lang, True)
        response = locale.Utils.request_location(self._lang)
        self._bot.send_message(
            self._user_id,
            response,
            reply_markup=geobutton,
            parse_mode='Markdown'
        )
        self._chatbase('open menu update location')

    @check_auth
    def _report(self):
        self._chatbase('report', 'user')
        self._bot.send_chat_action(self._user_id, 'typing')
        response = locale.Utils.report(self._lang)
        self._bot.send_message(
            self._user_id,
            response,
            disable_web_page_preview=True
        )
        self._chatbase('report message sent')

    @check_auth
    def _get_help(self):
        self._chatbase('help', 'user')
        self._bot.send_chat_action(self._user_id, 'typing')
        response = locale.Utils.help_menu(self._lang)
        keyboard = kbrd.get_help_menu(self._lang)
        self._bot.send_message(
            self._user_id,
            response,
            reply_markup=keyboard
        )
        self._chatbase('open help menu')

    @check_auth
    def _faq(self):
        self._chatbase('faq', 'user')
        response = locale.Utils.get_faq(self._lang)
        self._bot.send_message(self._user_id, response)
        self._chatbase('faq sent')

    def _incorrect_text(self):
        self._chatbase('not handled', 'user', not_handled=True)
        self._bot.send_chat_action(self._user_id, 'typing')
        response = locale.Utils.incorrect_text(self._lang)
        self._bot.send_message(self._user_id, response)

###############################################################################
#                               SETTINGS                                      #
###############################################################################

    @check_auth
    def _settings_menu(self):
        self._chatbase('settings menu', 'user')
        user_markup = kbrd.get_settings_menu(self._lang)
        response = locale.Utils.get_settings_menu(self._lang)
        self._bot.send_message(
            self._user_id,
            response,
            reply_markup=user_markup
        )
        self._chatbase('open settings menu')

    @check_auth
    def _select_zmanim(self):
        self._chatbase('select zmanim', 'user')
        self._bot.send_chat_action(self._user_id, 'typing')
        user_markup = kbrd.get_zmanim_callback_menu(
            self._lang,
            self._user_id
        )
        response = locale.Utils.get_zmanim_menu(self._lang)
        self._bot.send_message(
            self._user_id,
            response,
            reply_markup=user_markup
        )
        self._chatbase('open zmanim options')

    @check_auth
    def _select_candle_offset(self):
        self._chatbase('select candle offset', 'user')
        self._bot.send_chat_action(self._user_id, 'typing')
        user_markup = kbrd.get_candle_offset_callback_menu(self._user_id)
        response = locale.Shabos.shabos_candle_offset(self._lang)
        self._bot.send_message(
            self._user_id,
            response,
            reply_markup=user_markup
        )
        self._chatbase('open candle offset options')

    @check_auth
    def _select_diaspora(self):
        self._chatbase('select diaspora', 'user')
        self._bot.send_chat_action(self._user_id, 'typing')
        user_markup = kbrd.get_diaspora_callback_menu(
            self._lang,
            self._user_id
        )
        diaspora_status = db_operations.get_diaspora_status(self._user_id)
        response = locale.Utils.diaspora(self._lang, diaspora_status)
        self._bot.send_message(
            self._user_id,
            response,
            reply_markup=user_markup,
            parse_mode='Markdown'
        )
        self._chatbase('open diaspora options')

###############################################################################
#                          MAIN MENU FUNCTIONS                                #
###############################################################################

    @check_auth
    def _get_zmanim(self):
        self._chatbase('zmanim', 'user')
        response = zmanim.get_zmanim(self._user_id, self._lang)
        if response['polar_error']:
            self._bot.send_chat_action(self._user_id, 'typing')
            response_message = response['polar_error']
            self._bot.send_message(self._user_id, response_message)
            self._chatbase('zmanim polar error')
        elif response['zmanim_set_error']:
            self._bot.send_chat_action(self._user_id, 'typing')
            response_message = response['zmanim_set_error']
            user_markup = kbrd.get_zmanim_callback_menu(
                self._lang,
                self._user_id)
            self._bot.send_message(
                self._user_id,
                response_message,
                reply_markup=user_markup
            )
            self._chatbase('zmanim set error')
        else:
            self._bot.send_chat_action(self._user_id, 'upload_photo')
            response_pic = response['zmanim_pic']
            self._bot.send_photo(self._user_id, response_pic)
            response_pic.close()
            self._chatbase('zmanim sent')

    @check_auth
    def _get_zmanim_by_the_date(self, day: int, month: int, year: int):
        custom_date = (year, month, day)
        response = zmanim.get_zmanim(self._user_id, self._lang, custom_date)
        if response['polar_error']:
            self._bot.send_chat_action(self._user_id, 'typing')
            response_message = response['polar_error']
            self._bot.send_message(self._user_id, response_message)
            self._chatbase('zmanim polar error')
        elif response['zmanim_set_error']:
            self._bot.send_chat_action(self._user_id, 'typing')
            response_message = response['zmanim_set_error']
            user_markup = kbrd.get_zmanim_callback_menu(
                self._lang,
                self._user_id
            )
            self._bot.send_message(
                self._user_id,
                response_message,
                reply_markup=user_markup
            )
            self._chatbase('zmanim set error')
        else:
            self._bot.send_chat_action(self._user_id, 'upload_photo')
            response_pic = response['zmanim_pic']
            self._bot.send_photo(self._user_id, response_pic)
            response_pic.close()
            states.delete_state(self._user_id)
            self._chatbase('zmanim by the date sent')
        self._main_menu()

    @check_auth
    def _shabbat(self):
        self._chatbase('shabbos', 'user')
        self._bot.send_chat_action(self._user_id, 'upload_photo')
        response_pic = shabbos.get_shabbos(self._lang, self._user_id)
        self._bot.send_photo(self._user_id, response_pic)
        response_pic.close()
        self._chatbase('shabbos sent')

    @check_auth
    def _rosh_chodesh(self):
        self._chatbase('rosh chodesh', 'user')
        self._bot.send_chat_action(self._user_id, 'upload_photo')
        response_pic = rosh_hodesh.get_rh(self._user_id, self._lang)
        self._bot.send_photo(self._user_id, response_pic)
        response_pic.close()
        self._chatbase('rosh chodesh sent')

    @check_auth
    def _daf_yomi(self) -> None:
        self._chatbase('daf yomi', 'user')
        self._bot.send_chat_action(self._user_id, 'upload_photo')
        response_pic = daf.get_daf(self._user_id, self._lang)
        self._bot.send_photo(self._user_id, response_pic)
        response_pic.close()
        self._chatbase('daf yomi sent')

###############################################################################
#                                CONVERTER                                    #
###############################################################################

    @check_auth
    def _converter_startup(self):
        self._chatbase('converter', 'user')
        self._bot.send_chat_action(self._user_id, 'typing')
        response = locale.Converter.welcome_to_converter(self._lang)
        markup = kbrd.get_converter_menu(self._lang)
        self._bot.send_message(self._user_id, response, reply_markup=markup)
        self._chatbase('open converter menu')

    @check_auth
    def _converter_greg_to_heb(self):
        self._chatbase('convert greg -> heb', 'user')
        self._bot.send_chat_action(self._user_id, 'typing')
        states.set_state(self._user_id, 'waiting_for_greg_date')
        response = locale.Converter.request_date_for_converter_greg(self._lang)
        keyboard = kbrd.get_cancel_keyboard(self._lang)
        self._bot.send_message(
            self._user_id,
            response,
            parse_mode='Markdown',
            reply_markup=keyboard
        )
        self._chatbase('ask for date to convert')

    @check_auth
    def _convert_heb_to_greg(self):
        self._chatbase('convert heb -> greg', 'user')
        self._bot.send_chat_action(self._user_id, 'typing')
        states.set_state(self._user_id, 'waiting_for_heb_date')
        response = locale.Converter.request_date_for_converter_heb(self._lang)
        keyboard = kbrd.get_cancel_keyboard(self._lang)
        self._bot.send_message(
            self._user_id,
            response,
            parse_mode='Markdown',
            reply_markup=keyboard
        )
        self._chatbase('ask for date to convert')

###############################################################################
#                             HANDLING DATES                                  #
###############################################################################

    @check_auth
    def _request_date(self):
        self._chatbase('zmanim by the date', 'user')
        self._bot.send_chat_action(self._user_id, 'typing')
        states.set_state(self._user_id, 'waiting_for_date')
        response = locale.Utils.request_date(self._lang)
        keyboard = kbrd.get_cancel_keyboard(self._lang)
        self._bot.send_message(
            self._user_id,
            response,
            parse_mode='Markdown',
            reply_markup=keyboard
        )
        self._chatbase('request date for zmanim sent')

    def _handle_date(self):
        self._chatbase('received custom date', 'user')
        reg_pattern = r'^[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,4}$'
        extracted_date = re.search(reg_pattern, self._text)
        if extracted_date:
            day = int(extracted_date.group().split('.')[0])
            month = int(extracted_date.group().split('.')[1])
            year = int(extracted_date.group().split('.')[2])
            try:
                datetime(year, month, day)
                self._get_zmanim_by_the_date(day, month, year)
                self._main_menu()
            except ValueError:
                self._incorrect_date('incorrect_date_value')
                self._chatbase('incorrect date value')
        else:
            self._incorrect_date('incorrect_date_format')
            self._chatbase('incorrect date format')

    def _handle_greg_date(self):
        self._chatbase('handle greg date', 'user')
        self._bot.send_chat_action(self._user_id, 'typing')
        reg_pattern = r'^[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,4}$'
        extracted_date = re.search(reg_pattern, self._text)
        if extracted_date:
            day = int(extracted_date.group().split('.')[0])
            month = int(extracted_date.group().split('.')[1])
            year = int(extracted_date.group().split('.')[2])
            try:
                datetime(year, month, day)
                date = (year, month, day)
                response = conv.convert_greg_to_heb(date, self._lang)
                keyboard = kbrd.get_zmanim_for_converter_button(
                    date,
                    self._lang
                )
                self._bot.send_message(
                    self._user_id,
                    response,
                    parse_mode='Markdown',
                    reply_markup=keyboard
                )
                states.delete_state(self._user_id)
                self._chatbase('greg date converted')
                self._main_menu()
            except:
                self._incorrect_date('incorrect_date_value')
                self._chatbase('incorrect date value')
        else:
            self._incorrect_date('incorrect_date_format')
            self._chatbase('incorrect date format')

    def _handle_heb_date(self):
        self._chatbase('handle heb date', 'user')
        self._bot.send_chat_action(self._user_id, 'typing')
        year, month, day = None, None, None
        input_data = self._text.split()
        if len(input_data) in [3, 4]:
            # check day
            if input_data[0].isdigit():
                day = int(input_data[0])
                if not 0 < day < 31:
                    self._incorrect_date('incorrect_heb_date_value')
            # check month
            if len(input_data) == 3:
                # all exept adar ii
                if input_data[1].lower() in data.heb_months_names_ru or \
                        input_data[1].lower() in data.heb_months_names_en or \
                        input_data[1].lower() in data.heb_months_names_he:
                    month = locale.Converter.get_month_name(
                        self._lang,
                        input_data[1].lower()
                    )
            elif len(input_data) == 4 \
                    and input_data[1].lower() in ['adar', 'адар', 'qqqq'] \
                    and input_data[2] in ['1', '2']:
                month = locale.Converter.get_month_name(
                    self._lang,
                    f'{input_data[1].lower()} {input_data[2]}'
                )
            else:
                self._incorrect_date('incorrect_heb_date_format')
            # check year
            if input_data[-1].isdigit():
                year = int(input_data[-1])
                if year < 0:
                    self._incorrect_date('incorrect_heb_date_value')
                # final calculation
                else:
                    hebrew_date = (year, month, day)
                    response = conv.convert_heb_to_greg(
                        hebrew_date,
                        self._lang
                    )
                    if response:
                        message_text = response['response']
                        keyboard = kbrd.get_zmanim_for_converter_button(
                            response['date'],
                            self._lang
                        )
                        self._bot.send_message(
                            self._user_id,
                            message_text,
                            parse_mode='Markdown',
                            reply_markup=keyboard
                        )
                        states.delete_state(self._user_id)
                        self._chatbase('heb date converted')
                        self._main_menu()
                    else:
                        self._chatbase('incorrect date value')
                        self._incorrect_date('incorrect_heb_date_value')
        else:
            self._chatbase('incorrect date format')
            self._incorrect_date('incorrect_heb_date_format')

    def _incorrect_date(self, error_type: str) -> None:
        self._bot.send_chat_action(self._user_id, 'typing')
        responses = {
            'incorrect_date_format': locale.Utils.incorrect_date_format(
                self._lang
            ),
            'incorrect_date_value': locale.Utils.incorrect_date_value(
                self._lang
            ),
            'incorrect_heb_date_format':
                locale.Converter.incorrect_heb_date_format(self._lang),
            'incorrect_heb_date_value':
                locale.Converter.incorrect_heb_date_value(self._lang)
        }
        response = responses.get(error_type, '')
        keyboard = kbrd.get_cancel_keyboard(self._lang)
        self._bot.send_message(
            self._user_id,
            response,
            parse_mode='Markdown',
            reply_markup=keyboard
        )

###############################################################################
#                               HOLIDAYS                                      #
###############################################################################

    @check_auth
    def _holidays(self):
        self._chatbase('holidays menu', 'user')
        self._bot.send_chat_action(self._user_id, 'typing')
        response = locale.Utils.get_holiday_menu(self._lang)
        holiday_menu = kbrd.get_holiday_menu(self._lang)
        self._bot.send_message(
            self._user_id,
            response,
            reply_markup=holiday_menu
        )
        self._chatbase('open holidays menu')

    @check_auth
    def _more_holiday_menu(self):
        self._chatbase('more holidays menu', 'user')
        user_markup = kbrd.get_more_holiday_menu(self._lang)
        response = locale.Utils.get_more_holiday_menu(self._lang)
        self._bot.send_message(
            self._user_id,
            response,
            reply_markup=user_markup
        )
        self._chatbase('open more holidays menu')

    @check_auth
    def _rosh_hashana(self):
        self._chatbase('rosh hashana', 'user')
        self._bot.send_chat_action(self._user_id, 'upload_photo')
        response_pic = holidays.get_holiday_pic(
            'Rosh Hashana',
            self._user_id,
            self._lang
        )
        self._bot.send_photo(self._user_id, response_pic)
        response_pic.close()
        self._chatbase('rosh hashana sent')

    @check_auth
    def _yom_kippur(self):
        self._chatbase('yom kippur', 'user')
        self._bot.send_chat_action(self._user_id, 'upload_photo')
        response_pic = holidays.get_holiday_pic(
            'Yom Kippur',
            self._user_id,
            self._lang
        )
        self._bot.send_photo(self._user_id, response_pic)
        response_pic.close()
        self._chatbase('yom kippur sent')

    @check_auth
    def _succot(self):
        self._chatbase('succos', 'user')
        self._bot.send_chat_action(self._user_id, 'upload_photo')
        response_pic = holidays.get_holiday_pic(
            'Succos',
            self._user_id,
            self._lang
        )
        self._bot.send_photo(self._user_id, response_pic)
        response_pic.close()
        self._chatbase('succos sent')

    @check_auth
    def _shmini_atzeret(self):
        self._chatbase('shmini atzeres', 'user')
        self._bot.send_chat_action(self._user_id, 'upload_photo')
        response_pic = holidays.get_holiday_pic(
            'Shmini Atzeres',
            self._user_id,
            self._lang
        )
        self._bot.send_photo(self._user_id, response_pic)
        response_pic.close()
        self._chatbase('shmini atzeres sent')

    @check_auth
    def _chanukah(self):
        self._chatbase('chanukah', 'user')
        self._bot.send_chat_action(self._user_id, 'upload_photo')
        response_pic = holidays.get_holiday_pic(
            'Chanuka',
            self._user_id,
            self._lang
        )
        self._bot.send_photo(self._user_id, response_pic)
        response_pic.close()
        self._chatbase('chanukah sent')

    @check_auth
    def _tu_beshvat(self):
        self._chatbase('tu bishvat', 'user')
        self._bot.send_chat_action(self._user_id, 'upload_photo')
        response_pic = holidays.get_holiday_pic(
            'Tu B\'shvat',
            self._user_id,
            self._lang
        )
        self._bot.send_photo(self._user_id, response_pic)
        response_pic.close()
        self._chatbase('tu bishvat sent')

    @check_auth
    def _purim(self):
        self._chatbase('purim', 'user')
        self._bot.send_chat_action(self._user_id, 'upload_photo')
        response_pic = holidays.get_holiday_pic(
            'Purim',
            self._user_id,
            self._lang
        )
        self._bot.send_photo(self._user_id, response_pic)
        response_pic.close()
        self._chatbase('purim sent')

    @check_auth
    def _pesach(self):
        self._chatbase('pesach', 'user')
        self._bot.send_chat_action(self._user_id, 'upload_photo')
        response_pic = holidays.get_holiday_pic(
            'Pesach',
            self._user_id,
            self._lang
        )
        self._bot.send_photo(self._user_id, response_pic)
        response_pic.close()
        self._chatbase('pesach sent')

    @check_auth
    def _lag_baomer(self):
        self._chatbase('lag baomer', 'user')
        self._bot.send_chat_action(self._user_id, 'upload_photo')
        response_pic = holidays.get_holiday_pic(
            'Lag Ba\'omer',
            self._user_id,
            self._lang
        )
        self._bot.send_photo(self._user_id, response_pic)
        response_pic.close()
        self._chatbase('lag baomer sent')

    @check_auth
    def _shavuot(self):
        self._chatbase('shavuos', 'user')
        self._bot.send_chat_action(self._user_id, 'upload_photo')
        response_pic = holidays.get_holiday_pic(
            'Shavuos',
            self._user_id,
            self._lang
        )
        self._bot.send_photo(self._user_id, response_pic)
        response_pic.close()
        self._chatbase('shavuos sent')

    @check_auth
    def _israel(self):
        self._chatbase('israel', 'user')
        self._bot.send_chat_action(self._user_id, 'upload_photo')
        response_pic = holidays.get_holiday_pic(
            'israel_holidays',
            self._user_id,
            self._lang
        )
        self._bot.send_photo(self._user_id, response_pic)
        response_pic.close()
        self._chatbase('israel sent')

###############################################################################
#                                 FASTS                                       #
###############################################################################

    @check_auth
    def _fasts(self):
        self._bot.send_chat_action(self._user_id, 'typing')
        self._chatbase('holidays menu', 'user')
        response = locale.Utils.get_fast_menu(self._lang)
        fast_menu = kbrd.get_fast_menu(self._lang)
        self._bot.send_message(self._user_id, response, reply_markup=fast_menu)
        self._chatbase('open fasts menu')

    @check_auth
    def _fast_gedaliah(self):
        self._chatbase('fast gedaliah', 'user')
        self._bot.send_chat_action(self._user_id, 'upload_photo')
        response_pic = holidays.get_holiday_pic(
            'Tzom Gedalia',
            self._user_id,
            self._lang
        )
        self._bot.send_photo(self._user_id, response_pic)
        response_pic.close()
        self._chatbase('fast gedaliah sent')

    @check_auth
    def _asarah_betevet(self):
        self._chatbase('10 of tevet', 'user')
        self._bot.send_chat_action(self._user_id, 'upload_photo')
        response_pic = holidays.get_holiday_pic(
            '10 of Teves',
            self._user_id,
            self._lang
        )
        self._bot.send_photo(self._user_id, response_pic)
        response_pic.close()
        self._chatbase('10 of tevet sent')

    @check_auth
    def _fast_esther(self):
        self._chatbase('fast esther', 'user')
        self._bot.send_chat_action(self._user_id, 'upload_photo')
        response_pic = holidays.get_holiday_pic(
            'Taanis Esther',
            self._user_id,
            self._lang
        )
        self._bot.send_photo(self._user_id, response_pic)
        response_pic.close()
        self._chatbase('fast esther sent')

    @check_auth
    def _sheva_asar_betammuz(self):
        self._chatbase('17 of tammuz', 'user')
        self._bot.send_chat_action(self._user_id, 'upload_photo')
        response_pic = holidays.get_holiday_pic(
            '17 of Tamuz',
            self._user_id,
            self._lang
        )
        self._bot.send_photo(self._user_id, response_pic)
        response_pic.close()
        self._chatbase('17 of tammuz sent')

    @check_auth
    def _tisha_beav(self):
        self._chatbase('9 of av', 'user')
        self._bot.send_chat_action(self._user_id, 'upload_photo')
        response_pic = holidays.get_holiday_pic(
            '9 of Av',
            self._user_id,
            self._lang
        )
        self._bot.send_photo(self._user_id, response_pic)
        response_pic.close()
        self._chatbase('9 of av sent')

    _handlers = {
        'Язык': _change_lang,
        'Language': _change_lang,
        'Отмена': _main_menu,
        'Cancel': _main_menu,
        'Русский': _set_lang,
        'English': _set_lang,
        'Hebrew': _set_lang,
        'Назад/Back': _change_lang,
        'Зманим': _get_zmanim,
        'Zmanim': _get_zmanim,
        'זמנים': _get_zmanim,
        'Зманим по дате': _request_date,
        'Zmanim by the date': _request_date,
        'Шаббат': _shabbat,
        'Shabbos': _shabbat,
        'שבת': _shabbat,
        'Рош Ходеш': _rosh_chodesh,
        'Rosh Chodesh': _rosh_chodesh,
        'ראש חודש': _rosh_chodesh,
        'Праздники': _holidays,
        'Holidays': _holidays,
        'חגים': _holidays,
        'Посты': _fasts,
        'Fast days': _fasts,
        'כהנה': _fasts,
        'Даф Йоми': _daf_yomi,
        'Daf Yomi': _daf_yomi,
        'דף יומי': _daf_yomi,
        'Местоположение': _update_location,
        'Location': _update_location,
        'Назад': _main_menu,
        'Back': _main_menu,
        'ЧаВо': _faq,
        'F.A.Q.': _faq,
        '🇷🇺': _faq,
        '🇱🇷': _faq,
        'Ещё...': _more_holiday_menu,
        'More...': _more_holiday_menu,
        'Основные праздники': _holidays,
        'Main holidays': _holidays,
        'Main menu': _main_menu,
        'Главное меню': _main_menu,
        'Рош Ашана': _rosh_hashana,
        'Rosh HaShanah': _rosh_hashana,
        'ראש השנה': _rosh_hashana,
        'Йом Кипур': _yom_kippur,
        'Yom Kippur': _yom_kippur,
        'יום כיפור': _yom_kippur,
        'Суккот': _succot,
        'Succos': _succot,
        'סוכות': _succot,
        'Шмини Ацерет': _shmini_atzeret,
        'Shmini Atzeres': _shmini_atzeret,
        'שמיני עצרת': _shmini_atzeret,
        'Ханука': _chanukah,
        'Chanukah': _chanukah,
        'חנוכה': _chanukah,
        'Ту биШват': _tu_beshvat,
        'Tu BShevat': _tu_beshvat,
        'ט"ו בשבט': _tu_beshvat,
        'Пурим': _purim,
        'Purim': _purim,
        'פורים': _purim,
        'Пейсах': _pesach,
        'Pesach': _pesach,
        'פסח': _pesach,
        'Лаг баОмер': _lag_baomer,
        'Lag BaOmer': _lag_baomer,
        'ל"ג בעומר': _lag_baomer,
        'Шавуот': _shavuot,
        'Shavuot': _shavuot,
        'שבועות': _shavuot,
        'Израильские праздники': _israel,
        'Israel holidays': _israel,
        'Пост Гедалии': _fast_gedaliah,
        'Fast of Gedaliah': _fast_gedaliah,
        'צום גדליה': _fast_gedaliah,
        '10 Тевета': _asarah_betevet,
        '10 of Tevet': _asarah_betevet,
        'עשרה בטבת': _asarah_betevet,
        'Пост Эстер': _fast_esther,
        'Fast of Esther': _fast_esther,
        'תענית אסתר': _fast_esther,
        '17 Таммуза': _sheva_asar_betammuz,
        '17 of Tammuz': _sheva_asar_betammuz,
        'שבעה עשר בתמוז': _sheva_asar_betammuz,
        '9 Ава': _tisha_beav,
        '9 of Av': _tisha_beav,
        'תשעה באב': _tisha_beav,
        'Настройки': _settings_menu,
        'Settings': _settings_menu,
        'Выбрать зманим': _select_zmanim,
        'Select zmanim': _select_zmanim,
        'Зажигание свечей': _select_candle_offset,
        'Candle lighting': _select_candle_offset,
        'Диаспора': _select_diaspora,
        'Diaspora': _select_diaspora,
        'Конвертер дат': _converter_startup,
        'Date converter': _converter_startup,
        'Григорианский ➡️ Еврейский': _converter_greg_to_heb,
        'Gregorian ➡️ Hebrew': _converter_greg_to_heb,
        'Еврейский ➡️ Григорианский': _convert_heb_to_greg,
        'Hebrew ➡️ Gregorian': _convert_heb_to_greg,
        'Помощь': _get_help,
        'Help': _get_help,
        'Сообщить об ошибке': _report,
        'Report a bug': _report
    }
    _user_states = {
        'waiting_for_date': _handle_date,
        'waiting_for_greg_date': _handle_greg_date,
        'waiting_for_heb_date': _handle_heb_date

    }
    _langs = {
        'Русский': 'Russian',
        'English': 'English',
        'Hebrew': 'Hebrew'
    }

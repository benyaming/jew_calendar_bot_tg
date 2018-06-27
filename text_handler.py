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

import localization as l
import holidays as h


def get_zmanim():
    # loc = db_operations.get_location_by_id(user)
    # if not loc:
    #     return request_location()
    # else:
    response = zmanim.get_zmanim(user, lang)
    # , parse_mode='Markdown'
    bot.send_message(user, response)


def request_date():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        request_location()
    else:
        states.set_state(user, 'waiting_for_date')
        response = l.Utils.request_date_for_zmanim(lang)
        keyboard = keyboards.get_cancel_keyboard(lang)
        bot.send_message(
            user,
            response,
            parse_mode='Markdown',
            reply_markup=keyboard
        )


def handle_date():
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
    else:
        incorrect_date('incorrect_date_format')


def get_zmanim_by_the_date(day: int, month: int, year: int):
    loc = db_operations.get_location_by_id(user)
    if not loc:
        states.delete_state(user)
        result = request_location
    else:
        custom_date = (year, month, day)
        response = zmanim.get_zmanim(user, lang, custom_date)
        bot.send_message(user, response, parse_mode='Markdown')
        states.delete_state(user)
        result = main_menu
    return result


def incorrect_date(error_type: str) -> None:
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
    loc = db_operations.get_location_by_id(user)
    if not loc:
        return request_location()
    else:
        response = shabbos.get_shabbos_string(loc, lang, user)
        bot.send_message(user, response, parse_mode='Markdown')


def rosh_chodesh():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        return request_location()
    else:
        response = rosh_hodesh.get_rh(loc, lang)
        bot.send_message(user, response, parse_mode='Markdown')


def holidays():
    responses = {
        'Russian': 'Выберите интересующий вас праздник:',
        'English': 'Choose:'
    }
    response = responses.get(lang, '')
    holiday_menu = keyboards.get_holiday_menu(lang)
    bot.send_message(user, response, reply_markup=holiday_menu)


def fasts():
    responses = {
        'Russian': 'Выберите:',
        'English': 'Choose:'
    }
    response = responses.get(lang, '')
    fast_menu = keyboards.get_fast_menu(lang)
    bot.send_message(user, response, reply_markup=fast_menu)


def daf_yomi():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        return request_location()
    else:
        response = daf.get_daf(loc, lang)
        bot.send_message(user, response, parse_mode='Markdown')


def update_location():
    geobutton = keyboards.get_geobutton(lang, True)
    response = l.Utils.request_location(lang)
    bot.send_message(
        user,
        response,
        reply_markup=geobutton,
        parse_mode='Markdown'
    )


def request_location():
    geobutton = keyboards.get_geobutton(lang)
    response = l.Utils.request_location(lang)
    bot.send_message(
        user,
        response,
        reply_markup=geobutton,
        parse_mode='Markdown'
    )


def set_lang():
    db_operations.set_lang(user, lang)
    return main_menu()


def main_menu():
    auth = db_operations.get_location_by_id(user)
    if not auth:
        request_location()
    else:
        user_markup = keyboards.get_main_menu(lang)
        responses = {
            'Russian': 'Выберите:',
            'English': 'Choose:'
        }
        response = responses.get(lang, '')
        bot.send_message(user, response, reply_markup=user_markup)


def faq():
    responses = {
        'Russian': 'http://telegra.ph/Hebrew-Calendar-Bot-FAQ-05-10',
        'English': 'http://telegra.ph/Hebrew-Calendar-Bot-FAQ-EN-05-10'
    }
    response = responses.get(lang, '')
    bot.send_message(user, response)


def report():
    response = l.Utils.report(lang)
    bot.send_message(user, response, disable_web_page_preview=True)


def more_holiday_menu():
    auth = db_operations.get_location_by_id(user)
    if not auth:
        return request_location()
    else:
        user_markup = keyboards.get_more_holiday_menu(lang)
        responses = {
            'Russian': 'Выберите:',
            'English': 'Choose:'
        }
        response = responses.get(lang, '')
        bot.send_message(user, response, reply_markup=user_markup)


def rosh_hashana():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        return request_location()
    else:
        response = h.rosh_hashanah(user, lang)
        bot.send_message(user, response, parse_mode='Markdown')


def yom_kippur():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        return request_location()
    else:
        response = h.yom_kipur(user, lang)
        bot.send_message(user, response, parse_mode='Markdown')


def succot():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        return request_location()
    else:
        response = h.succos(user, lang)
        bot.send_message(user, response, parse_mode='Markdown')


def shmini_atzeret():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        return request_location()
    else:
        response = h.shmini_atzeres_simhat(user, lang)
        bot.send_message(user, response, parse_mode='Markdown')


def chanukah():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        return request_location()
    else:
        response = h.chanukah(user, lang)
        bot.send_message(user, response, parse_mode='Markdown')


def tu_beshvat():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        return request_location()
    else:
        response = h.tu_bshevat(user, lang)
        bot.send_message(user, response, parse_mode='Markdown')


def purim():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        return request_location()
    else:
        response = h.purim(user, lang)
        bot.send_message(user, response, parse_mode='Markdown')


def pesach():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        return request_location()
    else:
        response = h.pesach(user, lang)
        bot.send_message(user, response, parse_mode='Markdown')


def lag_baomer():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        return request_location()
    else:
        response = h.lag_baomer(user, lang)
        bot.send_message(user, response, parse_mode='Markdown')


def shavuot():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        return request_location()
    else:
        response = h.shavuot(user, lang)
        bot.send_message(user, response, parse_mode='Markdown')


def israel():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        return request_location()
    else:
        response = h.get_israel(user, lang)
        bot.send_message(user, response, parse_mode='Markdown')


def fast_gedaliah():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        return request_location()
    else:
        response = h.tzom_gedaliah(user, lang)
        bot.send_message(user, response, parse_mode='Markdown')


def asarah_betevet():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        return request_location()
    else:
        response = h.asarah_btevet(user, lang)
        bot.send_message(user, response, parse_mode='Markdown')


def fast_esther():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        return request_location()
    else:
        response = h.taanit_esther(user, lang)
        bot.send_message(user, response, parse_mode='Markdown')


def sheva_asar_betammuz():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        return request_location()
    else:
        response = h.shiva_asar_tammuz(user, lang)
        bot.send_message(user, response, parse_mode='Markdown')


def tisha_beav():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        return request_location()
    else:
        response = h.tisha_bav(user, lang)
        bot.send_message(user, response, parse_mode='Markdown')


def change_lang():
    response = 'Выберите язык/Choose the language'
    lang_markup = keyboards.get_lang_menu()
    bot.send_message(user, response, reply_markup=lang_markup)


def incorrect_text():
    response = l.Utils.incorrect_text(lang)
    bot.send_message(user, response)


def settings_menu():
    auth = db_operations.get_location_by_id(user)
    if not auth:
        request_location()
    else:
        user_markup = keyboards.get_settings_menu(lang)
        responses = {
            'Russian': 'Добро пожаловать в настройки!',
            'English': 'Welcome to settings!'
        }
        response = responses.get(lang, '')
        bot.send_message(user, response, reply_markup=user_markup)


def select_zmanim():
    auth = db_operations.get_location_by_id(user)
    if not auth:
        request_location()
    else:
        user_markup = keyboards.get_zmanim_callback_menu(lang, user)
        responses = {
            'Russian': 'Выберите зманим для отображения',
            'English': 'Choose zmanim that will shown'
        }
        response = responses.get(lang, '')
        bot.send_message(user, response, reply_markup=user_markup)
        # TODO init


def select_candle_offset():
    auth = db_operations.get_location_by_id(user)
    if not auth:
        request_location()
    else:
        user_markup = keyboards.get_candle_offset_callback_menu(user)
        response = l.Shabos.shabos_candle_offset(lang)
        bot.send_message(user, response, reply_markup=user_markup)
        # TODO предупреждение о настройках
        # TODO init


def select_diaspora():
    auth = db_operations.get_location_by_id(user)
    if not auth:
        request_location()
    else:
        user_markup = keyboards.get_diaspora_callback_menu(lang, user)
        diaspora_status = db_operations.get_diaspora_status(user)
        response = l.Utils.diaspora(lang, diaspora_status)
        bot.send_message(
            user,
            response,
            reply_markup=user_markup,
            parse_mode='Markdown'
        )
        # TODO предупреждение о настройках
        # TODO init


def converter_startup():
    auth = db_operations.get_location_by_id(user)
    if not auth:
        request_location()
    else:
        response = l.Converter.welcome_to_converter(lang)
        markup = keyboards.get_converter_menu(lang)
        bot.send_message(user, response, reply_markup=markup)


def converter_greg_to_heb():
    auth = db_operations.get_location_by_id(user)
    if not auth:
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


def convert_heb_to_greg():
    auth = db_operations.get_location_by_id(user)
    if not auth:
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


def handle_greg_date():
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
        except Exception as e:
            incorrect_date('incorrect_date_value')
    else:
        incorrect_date('incorrect_date_format')


def handle_heb_date():
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
                    main_menu()
                else:
                    return incorrect_date('incorrect_heb_date_value')
    else:
        return incorrect_date('incorrect_heb_date_format')


def handle_text(user_id: int, message: str) -> None:
    global bot, user, lang, text
    bot = TeleBot(settings.TOKEN)
    user = user_id
    text = message
    if message in ['Русский', 'English']:
        langs = {
            'Русский': 'Russian',
            'English': 'English'
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
            func()
    else:
        if message in ['Русский', 'English']:
            langs = {
                'Русский': 'Russian',
                'English': 'English'
            }
            lang = langs.get(message, '')
        else:
            lang = db_operations.get_lang_from_redis(user)
        messages = {
            'Язык': change_lang,
            'Language': change_lang,
            'Отмена': main_menu,
            'Cancel': main_menu,
            'Русский': set_lang,
            'English': set_lang,
            'Назад/Back': change_lang,
            'Зманим': get_zmanim,
            'Zmanim': get_zmanim,
            'Зманим по дате': request_date,
            'Zmanim by the date': request_date,
            'Шаббат': shabbat,
            'Shabbos': shabbat,
            'Рош Ходеш': rosh_chodesh,
            'Rosh Chodesh': rosh_chodesh,
            'Праздники': holidays,
            'Holidays': holidays,
            'Посты': fasts,
            'Fast days': fasts,
            'Даф Йоми': daf_yomi,
            'Daf Yomi': daf_yomi,
            'Местоположение': update_location,
            'Location': update_location,
            'Назад': main_menu,
            'Back': main_menu,
            'ЧаВо': faq,
            'F.A.Q.': faq,
            '🇷🇺': faq,
            '🇱🇷': faq,
            'Больше...': more_holiday_menu,
            'More...': more_holiday_menu,
            'Основные праздники': holidays,
            'Main holidays': holidays,
            'Main menu': main_menu,
            'Главное меню': main_menu,
            'Рош Ашана': rosh_hashana,
            'Rosh HaShanah': rosh_hashana,
            'Йом Кипур': yom_kippur,
            'Yom Kippur': yom_kippur,
            'Суккот': succot,
            'Succos': succot,
            'Шмини Ацерет': shmini_atzeret,
            'Shmini Atzeres': shmini_atzeret,
            'Ханука': chanukah,
            'Chanukah': chanukah,
            'Ту биШват': tu_beshvat,
            'Tu BShevat': tu_beshvat,
            'Пурим': purim,
            'Purim': purim,
            'Пейсах': pesach,
            'Pesach': pesach,
            'Лаг баОмер': lag_baomer,
            'Lag BaOmer': lag_baomer,
            'Шавуот': shavuot,
            'Shavuot': shavuot,
            'Израильские праздники': israel,
            'Israel holidays': israel,
            'Пост Гедалии': fast_gedaliah,
            'Tzom Gedaliah': fast_gedaliah,
            '10 Тевета': asarah_betevet,
            'Asarah BTevet': asarah_betevet,
            'Пост Эстер': fast_esther,
            'Taanit Esther': fast_esther,
            '17 Таммуза': sheva_asar_betammuz,
            'Shiva Asar BTammuz': sheva_asar_betammuz,
            '9 Ава': tisha_beav,
            'Tisha BAv': tisha_beav,
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

        }
        func = messages.get(message, incorrect_text)
        func()

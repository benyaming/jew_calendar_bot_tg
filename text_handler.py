# -*- coding: utf-8 -*-
import re
from datetime import datetime

from telebot import TeleBot

import db_operations
import keyboards
import zmanim
import shabbos
import rosh_hodesh
import daf
import settings
import states

import localization as l
import holidays as h


def get_zmanim():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        return request_location()
    else:
        response = zmanim.get_zmanim(user, lang)
        bot.send_message(user, response, parse_mode='Markdown')


def ext_zmanim():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        return request_location()
    else:
        response = zmanim.get_ext_zmanim(user, lang)
        bot.send_message(user, response, parse_mode='Markdown')


def request_date():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        request_location()
    else:
        states.set_state(user, 'waiting_for_date')
        response = l.Utils.request_date(lang)
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
        except ValueError:
            incorrect_date('incorrect_date_value')
    else:
        if text in ['Отмена', 'Cancel']:
            states.delete_state(user)
            main_menu()
        else:
            incorrect_date('incorrect_date_format')


def get_zmanim_by_the_date(day: int, month: int, year: int):
    loc = db_operations.get_location_by_id(user)
    if not loc:
        states.delete_state(user)
        result = request_location
    else:
        response = zmanim.get_ext_zmanim(user, lang, day, month, year)
        bot.send_message(user, response, parse_mode='Markdown')
        states.delete_state(user)
        result = main_menu
    return result


def incorrect_date(error_type: str) -> None:
    responses = {
        'incorrect_date_format': l.Utils.incorrect_date_format(lang),
        'incorrect_date_value': l.Utils.incorrect_date_value(lang)
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
        response = shabbos.get_shabbos_string(loc, lang)
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
        'Russian': 'Выберите: (клавиатуру можно скроллить)',
        'English': 'Choose: (scroll keyboard)'
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


def tu_beav():
    loc = db_operations.get_location_by_id(user)
    if not loc:
        return request_location()
    else:
        response = h.tu_bav(user, lang)
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
        user_states = {
            'waiting_for_date': handle_date
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
            'Зманим (Полные)': ext_zmanim,
            'Зманим по дате': request_date,
            'Zmanim by the date': request_date,
            'Zmanim (Full)': ext_zmanim,
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
            'Обратная связь': report,
            'Contact': report,
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
            '15 Ава': tu_beav,
            'Tu BAv': tu_beav,
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
        }
        func = messages.get(message, incorrect_text)
        func()

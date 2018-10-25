from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import main_menu_buttons as main
from data import holiday_menu_buttons as holiday
from data import fast_menu_buttons as fast
from data import settings_menu_buttons as setting
from data import help_menu_buttons

from localization import Zmanim
from zmanim import ZmanimList

import db_operations, data


def get_main_menu(lang):
    user_markup = ReplyKeyboardMarkup(True, False)
    user_markup.row(main['Zmanim'][lang],
                    main['Shabbos'][lang],
                    main['Holidays'][lang])
    user_markup.row(main['Rosh Chodesh'][lang],
                    main['Daf Yomi'][lang],
                    main['Fast days'][lang])
    user_markup.row(main['Zmanim by the date'][lang],
                    main['Date converter'][lang])
    user_markup.row(main['Help'][lang],
                    main['Settings'][lang])
    return user_markup


def get_settings_menu(lang):
    user_markup = ReplyKeyboardMarkup(True, False)
    user_markup.row(setting['Select zmanim'][lang],
                    setting['Candle lighting'][lang],
                    setting['Language'][lang])
    user_markup.row(setting['Diaspora'][lang],
                    setting['Location'][lang],
                    setting['Back'][lang])
    return user_markup


def get_holiday_menu(lang):
    user_markup = ReplyKeyboardMarkup(True, False)
    user_markup.row(holiday['Rosh HaShanah'][lang],
                    holiday['Yom Kippur'][lang],
                    holiday['Succos'][lang])
    user_markup.row(holiday['Shmini Atzeres'][lang],
                    holiday['Chanukah'][lang],
                    holiday['Purim'][lang])
    user_markup.row(holiday['Pesach'][lang],
                    holiday['Shavuot'][lang],
                    holiday['More'][lang])
    user_markup.row(holiday['Back'][lang])
    return user_markup


def get_more_holiday_menu(lang: str) -> ReplyKeyboardMarkup:
    user_markup = ReplyKeyboardMarkup(True, False)
    user_markup.row(holiday['Tu BShevat'][lang],
                    holiday['Lag BaOmer'][lang])
    user_markup.row(holiday['Israel holidays'][lang])
    user_markup.row(holiday['Main holidays'][lang],
                    holiday['Main menu'][lang])
    return user_markup


def get_fast_menu(lang):
    user_markup = ReplyKeyboardMarkup(True, False)
    user_markup.row(fast['Tzom Gedaliah'][lang],
                    fast['Asarah BTevet'][lang])
    user_markup.row(fast['Taanit Esther'][lang],
                    fast['Shiva Asar BTammuz'][lang])
    user_markup.row(fast['Tisha BAv'][lang])
    user_markup.row(fast['Back'][lang])
    return user_markup


def get_lang_menu():
    lang_markup = ReplyKeyboardMarkup(True, False)
    lang_markup.row('Русский', 'English')
    return lang_markup


def get_geobutton(lang, is_update=False):
    geobutton = ReplyKeyboardMarkup(True)
    title = {
        'Russian': 'Отправить координаты',
        'English': 'Send location',
        'Hebrew': 'Send location'
    }
    geobutton.row(KeyboardButton(
        request_location=True,
        text=title.get(lang, ''))
    )
    if is_update:
        cancel = {
            'Russian': 'Отмена',
            'English': 'Cancel',
            'Hebrew': 'cancel'
        }
        geobutton.row(cancel.get(lang, ''))
    return geobutton


def get_cancel_keyboard(lang):
    keyboard = ReplyKeyboardMarkup(True)
    cancel = {
        'Russian': 'Отмена',
        'English': 'Cancel',
        'Hebrew': 'cancel'
    }
    keyboard.row(cancel.get(lang, ''))
    return keyboard


def get_converter_menu(lang: str) -> ReplyKeyboardMarkup:
    cancel = {
        'Russian': 'Отмена',
        'English': 'Cancel',
        'Hebrew': ''  # TODO перевод
    }
    markup = ReplyKeyboardMarkup(True, False)
    markup.row(data.converter_buttons_name_greg_to_heb[lang])
    markup.row(data.converter_buttons_name_heb_to_greg[lang])
    markup.row(cancel.get(lang, ''))
    return markup


def get_help_menu(lang: str) -> ReplyKeyboardMarkup:
    user_markup = ReplyKeyboardMarkup(True, False)
    user_markup.row(
        help_menu_buttons['faq'][lang],
        help_menu_buttons['report'][lang]
    )
    user_markup.row(setting['Back'][lang])
    return user_markup

# ============================================================================#


def get_alot_ma_button(lang: str, status: bool) -> InlineKeyboardButton:
    zman_code = 'alot_ma'
    if status:
        status_emoji = '✅'
        status_code = 1
    else:
        status_emoji = '❌'
        status_code = 0
    button = InlineKeyboardButton(
        text=f'{status_emoji}  {Zmanim.get_zman_name(zman_code, lang)}',
        callback_data=f'zmanim-{zman_code}-{status_code}'
    )
    return button


def get_sunrise_button(lang: str, status: bool) -> InlineKeyboardButton:
    zman_code = 'sunrise'
    if status:
        status_emoji = '✅'
        status_code = 1
    else:
        status_emoji = '❌'
        status_code = 0
    button = InlineKeyboardButton(
        text=f'{status_emoji}  {Zmanim.get_zman_name(zman_code, lang)}',
        callback_data=f'zmanim-{zman_code}-{status_code}'
    )
    return button


def get_talis_ma_button(lang: str, status: bool) -> InlineKeyboardButton:
    zman_code = 'talis_ma'
    if status:
        status_emoji = '✅'
        status_code = 1
    else:
        status_emoji = '❌'
        status_code = 0
    button = InlineKeyboardButton(
        text=f'{status_emoji}  {Zmanim.get_zman_name(zman_code, lang)}',
        callback_data=f'zmanim-{zman_code}-{status_code}'
    )
    return button


def get_sof_zman_shema_ma_button(
        lang: str,
        status: bool
) -> InlineKeyboardButton:
    zman_code = 'sof_zman_shema_ma'
    if status:
        status_emoji = '✅'
        status_code = 1
    else:
        status_emoji = '❌'
        status_code = 0
    button = InlineKeyboardButton(
        text=f'{status_emoji}  {Zmanim.get_zman_name(zman_code, lang)}',
        callback_data=f'zmanim-{zman_code}-{status_code}'
    )
    return button


def get_sof_zman_shema_gra_button(
        lang: str,
        status: bool
) -> InlineKeyboardButton:
    zman_code = 'sof_zman_shema_gra'
    if status:
        status_emoji = '✅'
        status_code = 1
    else:
        status_emoji = '❌'
        status_code = 0
    button = InlineKeyboardButton(
        text=f'{status_emoji}  {Zmanim.get_zman_name(zman_code, lang)}',
        callback_data=f'zmanim-{zman_code}-{status_code}'
    )
    return button


def get_sof_zman_tefila_ma_button(
        lang: str,
        status: bool
) -> InlineKeyboardButton:
    zman_code = 'sof_zman_tefila_ma'
    if status:
        status_emoji = '✅'
        status_code = 1
    else:
        status_emoji = '❌'
        status_code = 0
    button = InlineKeyboardButton(
        text=f'{status_emoji}  {Zmanim.get_zman_name(zman_code, lang)}',
        callback_data=f'zmanim-{zman_code}-{status_code}'
    )
    return button


def get_sof_zman_tefila_gra_button(
        lang: str,
        status: bool
) -> InlineKeyboardButton:
    zman_code = 'sof_zman_tefila_gra'
    if status:
        status_emoji = '✅'
        status_code = 1
    else:
        status_emoji = '❌'
        status_code = 0
    button = InlineKeyboardButton(
        text=f'{status_emoji}  {Zmanim.get_zman_name(zman_code, lang)}',
        callback_data=f'zmanim-{zman_code}-{status_code}'
    )
    return button


def get_chatzos_button(lang: str, status: bool) -> InlineKeyboardButton:
    zman_code = 'chatzos'
    if status:
        status_emoji = '✅'
        status_code = 1
    else:
        status_emoji = '❌'
        status_code = 0
    button = InlineKeyboardButton(
        text=f'{status_emoji}  {Zmanim.get_zman_name(zman_code, lang)}',
        callback_data=f'zmanim-{zman_code}-{status_code}'
    )
    return button


def get_mincha_gedola_ma_button(
        lang: str,
        status: bool
) -> InlineKeyboardButton:
    zman_code = 'mincha_gedola_ma'
    if status:
        status_emoji = '✅'
        status_code = 1
    else:
        status_emoji = '❌'
        status_code = 0
    button = InlineKeyboardButton(
        text=f'{status_emoji}  {Zmanim.get_zman_name(zman_code, lang)}',
        callback_data=f'zmanim-{zman_code}-{status_code}'
    )
    return button


def get_mincha_ketana_gra_button(
        lang: str,
        status: bool
) -> InlineKeyboardButton:
    zman_code = 'mincha_ketana_gra'
    if status:
        status_emoji = '✅'
        status_code = 1
    else:
        status_emoji = '❌'
        status_code = 0
    button = InlineKeyboardButton(
        text=f'{status_emoji}  {Zmanim.get_zman_name(zman_code, lang)}',
        callback_data=f'zmanim-{zman_code}-{status_code}'
    )
    return button


def get_plag_mincha_button(lang: str, status: bool) -> InlineKeyboardButton:
    zman_code = 'plag_mincha'
    if status:
        status_emoji = '✅'
        status_code = 1
    else:
        status_emoji = '❌'
        status_code = 0
    button = InlineKeyboardButton(
        text=f'{status_emoji}  {Zmanim.get_zman_name(zman_code, lang)}',
        callback_data=f'zmanim-{zman_code}-{status_code}'
    )
    return button


def get_sunset_button(lang: str, status: bool) -> InlineKeyboardButton:
    zman_code = 'sunset'
    if status:
        status_emoji = '✅'
        status_code = 1
    else:
        status_emoji = '❌'
        status_code = 0
    button = InlineKeyboardButton(
        text=f'{status_emoji}  {Zmanim.get_zman_name(zman_code, lang)}',
        callback_data=f'zmanim-{zman_code}-{status_code}'
    )
    return button


def get_tzeis_595d_button(lang: str, status: bool) -> InlineKeyboardButton:
    zman_code = 'tzeis_595d'
    if status:
        status_emoji = '✅'
        status_code = 1
    else:
        status_emoji = '❌'
        status_code = 0
    button = InlineKeyboardButton(
        text=f'{status_emoji}  {Zmanim.get_zman_name(zman_code, lang)}',
        callback_data=f'zmanim-{zman_code}-{status_code}'
    )
    return button


def get_tzeis_850d_button(lang: str, status: bool) -> InlineKeyboardButton:
    zman_code = 'tzeis_850d'
    if status:
        status_emoji = '✅'
        status_code = 1
    else:
        status_emoji = '❌'
        status_code = 0
    button = InlineKeyboardButton(
        text=f'{status_emoji}  {Zmanim.get_zman_name(zman_code, lang)}',
        callback_data=f'zmanim-{zman_code}-{status_code}'
    )
    return button


def get_tzeis_42m_button(lang: str, status: bool) -> InlineKeyboardButton:
    zman_code = 'tzeis_42m'
    if status:
        status_emoji = '✅'
        status_code = 1
    else:
        status_emoji = '❌'
        status_code = 0
    button = InlineKeyboardButton(
        text=f'{status_emoji}  {Zmanim.get_zman_name(zman_code, lang)}',
        callback_data=f'zmanim-{zman_code}-{status_code}'
    )
    return button


def get_tzeis_rt_button(lang: str, status: bool) -> InlineKeyboardButton:
    zman_code = 'tzeis_rt'
    if status:
        status_emoji = '✅'
        status_code = 1
    else:
        status_emoji = '❌'
        status_code = 0
    button = InlineKeyboardButton(
        text=f'{status_emoji}  {Zmanim.get_zman_name(zman_code, lang)}',
        callback_data=f'zmanim-{zman_code}-{status_code}'
    )
    return button


def get_chatzos_laila_button(lang: str, status: bool) -> InlineKeyboardButton:
    zman_code = 'chatzos_laila'
    if status:
        status_emoji = '✅'
        status_code = 1
    else:
        status_emoji = '❌'
        status_code = 0
    button = InlineKeyboardButton(
        text=f'{status_emoji}  {Zmanim.get_zman_name(zman_code, lang)}',
        callback_data=f'zmanim-{zman_code}-{status_code}'
    )
    return button


def get_astronomical_hour_ma_button(
        lang: str,
        status: bool
) -> InlineKeyboardButton:
    zman_code = 'astronomical_hour_ma'
    if status:
        status_emoji = '✅'
        status_code = 1
    else:
        status_emoji = '❌'
        status_code = 0
    button = InlineKeyboardButton(
        text=f'{status_emoji}  {Zmanim.get_zman_name(zman_code, lang)}',
        callback_data=f'zmanim-{zman_code}-{status_code}'
    )
    return button


def get_astronomical_hour_gra_button(
        lang: str,
        status: bool
) -> InlineKeyboardButton:
    zman_code = 'astronomical_hour_gra'
    if status:
        status_emoji = '✅'
        status_code = 1
    else:
        status_emoji = '❌'
        status_code = 0
    button = InlineKeyboardButton(
        text=f'{status_emoji}  {Zmanim.get_zman_name(zman_code, lang)}',
        callback_data=f'zmanim-{zman_code}-{status_code}'
    )
    return button


def make_button_by_zman_number(
        number: int,
        zmanim_set: str,
        lang: str
) -> InlineKeyboardButton:
    zman = int(zmanim_set[number])
    status = False
    if zman:
        status = True
    zman_code = ZmanimList(number).name
    func = funcs.get(zman_code, '')
    button = func(lang, status)
    return button


def make_row_by_zman_number(numbers: list, zmanim_set: str, lang: str) -> list:
    row = []
    for i in numbers:
        zman = int(zmanim_set[i])
        status = False
        if zman:
            status = True
        zman_code = ZmanimList(i).name
        func = funcs.get(zman_code, '')
        button = func(lang, status)
        row.append(button)
    return row


def build_zmanim_menu(user: int, lang: str) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup()
    zmanim_set = db_operations.get_zmanim_set(user)

    # группируем алот и нец
    row = make_row_by_zman_number([0, 1], zmanim_set, lang)
    keyboard.row(*row)

    # мишеякир
    button = make_button_by_zman_number(2, zmanim_set, lang)
    keyboard.add(button)

    # зман шма (агро и МА)
    row = make_row_by_zman_number([3, 4], zmanim_set, lang)
    keyboard.row(*row)

    # зман тфила (агро и МА)
    row = make_row_by_zman_number([5, 6], zmanim_set, lang)
    keyboard.row(*row)

    # хацот и минха гдола
    row = make_row_by_zman_number([7, 8], zmanim_set, lang)
    keyboard.row(*row)

    # минха ктана и плаг минха
    row = make_row_by_zman_number([9, 10], zmanim_set, lang)
    keyboard.row(*row)

    # остальное
    for i in range(11, 19):
        button = make_button_by_zman_number(i, zmanim_set, lang)
        keyboard.add(button)

    return keyboard

# ============================================================================#


def get_zmanim_callback_menu(lang: str, user: int) -> InlineKeyboardMarkup:
    menu = build_zmanim_menu(user, lang)
    return menu


def get_candle_offset_callback_menu(user: int) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    user_offset = db_operations.get_candle_offset(user)
    possible_offsets = [10, 15, 18, 20, 22, 30, 40]
    markup_row = []
    for i in possible_offsets:
        if i == user_offset:
            i = f'✅ {i}'
        offset_button = InlineKeyboardButton(
            text=i,
            callback_data=f'candle_offset-{i}'
        )
        markup_row.append(offset_button)
    markup.add(*markup_row)
    return markup


def get_diaspora_callback_menu(
        lang: str,
        user: int
) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    diaspora_status = db_operations.get_diaspora_status(user)
    if diaspora_status:
        diaspora_button = InlineKeyboardButton(
            text=f'❌ {data.diaspora_button_off[lang]}',
            callback_data='diaspora-0'
        )
    else:
        diaspora_button = InlineKeyboardButton(
            text=f'✅ {data.diaspora_button_on[lang]}',
            callback_data='diaspora-1'
        )
    markup.add(diaspora_button)
    return markup


def get_zmanim_for_converter_button(
        date: tuple,
        lang: str
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text=data.get_zmanim_button_converter[lang],
            callback_data=f'get_zmanim-{date[0]}.{date[1]}.{date[2]}'
        )
    )
    return keyboard


def get_zmanim_for_converter_button_adars(
        date: list,
        lang: str
) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text=data.get_zmanim_button_converter_adar1[lang],
            callback_data=f'get_zmanim-{date[0][0]}.{date[0][1]}.{date[0][2]}'
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text=data.get_zmanim_button_converter_adar2[lang],
            callback_data=f'get_zmanim-{date[1][0]}.{date[1][1]}.{date[1][2]}'
        )
    )
    return keyboard


funcs = {
        'alot_ma': get_alot_ma_button,
        'talis_ma': get_talis_ma_button,
        'sunrise': get_sunrise_button,
        'sof_zman_shema_ma': get_sof_zman_shema_ma_button,
        'sof_zman_shema_gra': get_sof_zman_shema_gra_button,
        'sof_zman_tefila_ma': get_sof_zman_tefila_ma_button,
        'sof_zman_tefila_gra': get_sof_zman_tefila_gra_button,
        'chatzos': get_chatzos_button,
        'mincha_gedola_ma': get_mincha_gedola_ma_button,
        'mincha_ketana_gra': get_mincha_ketana_gra_button,
        'plag_mincha': get_plag_mincha_button,
        'sunset': get_sunset_button,
        'tzeis_595d': get_tzeis_595d_button,
        'tzeis_850d': get_tzeis_850d_button,
        'tzeis_42m': get_tzeis_42m_button,
        'tzeis_rt': get_tzeis_rt_button,
        'astronomical_hour_ma': get_astronomical_hour_ma_button,
        'astronomical_hour_gra': get_astronomical_hour_gra_button,
        'chatzos_laila': get_chatzos_laila_button
    }

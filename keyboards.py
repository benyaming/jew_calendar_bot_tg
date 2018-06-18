from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu(lang):
    user_markup = ReplyKeyboardMarkup(True, False)
    if lang == 'English':
        user_markup.row('Zmanim', 'Shabbos', 'Holidays')
        user_markup.row('Zmanim (Full)', 'Rosh Chodesh', 'Fast days')
        user_markup.row('Zmanim by the date', 'Daf Yomi', 'Location')
        user_markup.row('Language', 'F.A.Q.', 'Contact')
    elif lang == 'Russian':
        user_markup.row('Зманим', 'Шаббат', 'Праздники')
        user_markup.row('Зманим (Полные)', 'Рош Ходеш', 'Посты')
        user_markup.row('Зманим по дате', 'Даф Йоми', 'Местоположение')
        user_markup.row('Язык', 'ЧаВо', 'Обратная связь')
    return user_markup


def get_holiday_menu(lang):
    user_markup = ReplyKeyboardMarkup(True, False)
    if lang == 'Russian':
        user_markup.row('Рош Ашана', 'Йом Кипур')
        user_markup.row('Суккот', 'Шмини Ацерет')
        user_markup.row('Ханука', 'Ту биШват', 'Пурим')
        user_markup.row('Пейсах', 'Лаг баОмер', 'Шавуот')
        user_markup.row('15 Ава', 'Израильские праздники')
        user_markup.row('Назад')
    elif lang == 'English':
        user_markup.row('Rosh HaShanah', 'Yom Kippur')
        user_markup.row('Succos', 'Shmini Atzeres')
        user_markup.row('Chanukah', 'Tu BShevat', 'Purim')
        user_markup.row('Pesach', 'Lag BaOmer', 'Shavuot')
        user_markup.row('Tu BAv', 'Israel holidays')
        user_markup.row('Back')
    return user_markup


def get_fast_menu(lang):
    user_markup = ReplyKeyboardMarkup(True, False)
    if lang == 'Russian':
        user_markup.row('Пост Гедалии', '10 Тевета')
        user_markup.row('Пост Эстер', '17 Таммуза')
        user_markup.row('9 Ава')
        user_markup.row('Назад')
    elif lang == 'English':
        user_markup.row('Tzom Gedaliah', 'Asarah BTevet')
        user_markup.row('Taanit Esther', 'Shiva Asar BTammuz')
        user_markup.row('Tisha BAv')
        user_markup.row('Back')
    return user_markup


def get_lang_menu():
    lang_markup = ReplyKeyboardMarkup(True, False)
    lang_markup.row('Русский', 'English')
    return lang_markup


def get_geobutton(lang, is_update=False):
    geobutton = ReplyKeyboardMarkup(True)
    title = {
        'Russian': 'Отправить координаты',
        'English': 'Send location'
    }
    geobutton.row(KeyboardButton(
        request_location=True,
        text=title.get(lang, ''))
    )
    if is_update:
        cancel = {
            'Russian': 'Отмена',
            'English': 'Cancel'
        }
        geobutton.row(cancel.get(lang, ''))
    return geobutton


def get_cancel_keyboard(lang):
    keyboard = ReplyKeyboardMarkup(True)
    cancel = {
        'Russian': 'Отмена',
        'English': 'Cancel'
    }
    keyboard.row(cancel.get(lang, ''))
    return keyboard

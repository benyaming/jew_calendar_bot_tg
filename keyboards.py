from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu(lang):
    user_markup = ReplyKeyboardMarkup(True, False)
    if lang == 'English':
        user_markup.row('Zmanim', 'Shabbos', 'Holidays')
        user_markup.row('Daf Yomi', 'Rosh Chodesh', 'Fast days')
        user_markup.row('Zmanim (Full)', 'Zmanim by the date', 'Location')
        user_markup.row('Language', 'F.A.Q.', 'Contact')
    elif lang == 'Russian':
        user_markup.row('Зманим', 'Шаббат', 'Праздники')
        user_markup.row('Даф Йоми', 'Рош Ходеш', 'Посты')
        user_markup.row('Зманим (Полные)', 'Зманим по дате', 'Местоположение')
        user_markup.row('Язык', 'ЧаВо', 'Обратная связь')
    return user_markup


def get_holiday_menu(lang):
    user_markup = ReplyKeyboardMarkup(True, False)
    if lang == 'Russian':
        user_markup.row('Рош Ашана', 'Йом Кипур', 'Суккот')
        user_markup.row('Шмини Ацерет', 'Ханука', 'Пурим')
        user_markup.row('Пейсах', 'Шавуот', 'Больше...')
        user_markup.row('Назад')
    elif lang == 'English':
        user_markup.row('Rosh HaShanah', 'Yom Kippur', 'Succos')
        user_markup.row('Shmini Atzeres', 'Chanukah', 'Purim')
        user_markup.row('Pesach', 'Shavuot', 'More...')
        user_markup.row('Back')
    return user_markup


def get_more_holiday_menu(lang: str) -> ReplyKeyboardMarkup:
    user_markup = ReplyKeyboardMarkup(True, False)
    if lang == 'Russian':
        user_markup.row('Ту биШват', 'Лаг баОмер')
        user_markup.row('Израильские праздники')
        user_markup.row('Основные праздники', 'Главное меню')
    elif lang == 'English':
        user_markup.row('Tu BShevat', 'Lag BaOmer')
        user_markup.row('Israel holidays')
        user_markup.row('Main holidays', 'Main menu')
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

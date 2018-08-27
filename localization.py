# -*- coding: utf-8 -*-
import data


# ЛОКАЛИЗАЦИЯ ДЛЯ ДАФ ЙОМИ
class DafYomi(object):

    titles = {
        'Russian': 'ДАФ ЙОМИ',
        'English': 'DAF YOMI',
        'Hebrew': 'דף יומ'
    }

    @staticmethod
    def get_str(lang: str, masechta: str, daf: str) -> str:
        responses = {
            'Russian': f'Трактат: | {data.talmud[masechta]}\n'
                       f'Лист: |{daf}',
            'English': f'Masechta: |{masechta}\n'
                       f'Daf: |{daf}',
            'Hebrew': f'*דף יומי*\n\n📗 *מסכתא:* {data.talmud_he[masechta]}\n '
                      f'📄 *דף*: {daf}'
        }
        daf_str = responses.get(lang, '')
        return daf_str


# ЛОКАЛИЗАЦИЯ ДЛЯ РОШ ХОДЕША
class RoshHodesh(object):

    titles = {
        'Russian': 'РОШ ХОДЕШ',
        'English': 'ROSH CHODESH',
        'Hebrew': 'ראש חודש'
    }

    # если два дня РХ в разных годах
    @staticmethod
    def two_days_in_different_years(
            lang: str,
            first_year: int,
            second_year: int
    ) -> str:
        responses = {
            'Russian': f'31 декабря {first_year} года и *1 '
                       f'января {second_year} года*',
            'English': f'31 December {first_year} and *1 '
                       f'January {second_year}*',
            'Hebrew': f' ו {first_year} בדצמבר 31'
                      f'{second_year} בינואר'
        }
        rh_days = responses.get(lang, '')
        return rh_days

    # если 2 дня РХ в разных месяцах, но в одном году
    @staticmethod
    def two_days_in_different_months(
            lang: str,
            first_day: int,
            first_month: int,
            second_month: int,
            year: int
    ) -> str:
        responses = {
            'Russian': f'{first_day} и 1 {data.gr_months_index[first_month]} '
                       f'и {data.gr_months_index[second_month]} {year} года*',
            'English': f'{first_day} and 1 '
                       f'{data.gr_months_index_en[first_month]}'
                       f' and {data.gr_months_index_en[second_month]} {year}*',
            'Hebrew':  f'{first_day} ו 1 '
                       f'{data.gr_months_index_he[first_month]}'
                       f' ו {data.gr_months_index_he[second_month]} {year}'
        }
        rh_days = responses.get(lang, '')
        return rh_days

    # если в РХ 2 дня
    @staticmethod
    def two_days(
            lang: str,
            first_day: int,
            second_day: int,
            month: int,
            year: int
    ) -> str:
        responses = {
            'Russian': f'{first_day} и {second_day} '
                       f'{data.gr_months_index[month]} {year} года*',
            'English': f'{first_day} and {second_day} '
                       f'{data.gr_months_index_en[month]} {year}*',
            'Hebrew': f'{first_day} ו {second_day} '
                      f'{data.gr_months_index_he[month]} {year}'
        }
        rh_days = responses.get(lang, '')
        return rh_days

    # если в РХ 1 день выпадает на 1 января
    @staticmethod
    def one_day_first_day_of_jan(lang: str, year: int) -> str:
        responses = {
            'Russian': f'1 января {year} года',
            'English': f'1 January {year}',
            'Hebrew': f'1 {year} בינואר'
        }
        rh_days = responses.get(lang, '')
        return rh_days

    # если в РХ 1 день выпадает на начало месяца
    @staticmethod
    def one_day_first_day_of_month(
            lang: str,
            month: int,
            year: int
    ) -> str:
        responses = {
            'Russian': f'1 {data.gr_months_index[month]} {year} года',
            'English': f'1 {data.gr_months_index_en[month]} {year}',
            'Hebrew': f'1 {data.gr_months_index_he[month]} {year}'
        }
        rh_days = responses.get(lang, '')
        return rh_days

    # если в РХ 1 день
    @staticmethod
    def one_day(
            lang: str,
            day: int,
            month: int,
            year: int
    ) -> str:
        responses = {
            'Russian': f'{day} {data.gr_months_index[month]} {year} года',
            'English': f'{day} {data.gr_months_index_en[month]} {year}',
            'Hebrew': f'{day} {data.gr_months_index_he[month]} {year}'
        }
        rh_days = responses.get(lang, '')
        return rh_days

    # определяем день недели
    @staticmethod
    def get_rh_day_of_week(
            lang: str,
            first_day: int,
            second_day=None
    ) -> str:
        responses = ''
        if second_day:
            responses = {
                'Russian': f'{data.days_ru[first_day]}-'
                           f'{data.days_ru[second_day]}',
                'English': f'{data.days_en[first_day]}-'
                           f'{data.days_en[second_day]}',
                'Hebrew': f'{data.days_he[first_day]}-'
                          f'{data.days_he[second_day]}'
            }
        elif not second_day:
            responses = {
                'Russian': f'{data.days_ru[first_day]}',
                'English': f'{data.days_en[first_day]}',
                'Hebrew': f'{data.days_he[first_day]}'
            }
        day_of_week = responses.get(lang, '')
        return day_of_week

    # определяем молад
    @staticmethod
    def get_molad_str(
            lang: str,
            day: int,
            month: str,
            day_of_week: str,
            nhours: int,
            hours: str,
            nminutes: int,
            nchalakim: int,
            chalakim: str
    ) -> str:
        responses = {
            'Russian': f'{day} {data.gr_months[month]}, '
                       f'{data.gr_dayofweek[day_of_week]},^'
                       f'{nhours} {data.hours.get(hours[-1:], "часов")} '
                       f'{nminutes} '
                       f'{data.minutes.get(nminutes, "минут")} и '
                       f'{nchalakim} {data.chalakim.get(chalakim, "частей")}',
            'English': f'{day} {month}, {day_of_week},^'
                       f'{nhours} {data.hours_en.get(hours, "hours")} '
                       f'{nminutes} '
                       f'{data.minutes_en.get(nminutes, "minutes")} and '
                       f'{nchalakim} '
                       f'{data.chalakim_en.get(chalakim, "chalakim")}',
            'Hebrew': f'{day} {data.gr_months_he[month]}, '
                      f'{data.gr_dayofweek_he[day_of_week]}, '
                      f'{nhours} {data.hours_he.get(hours, "שעות")} '
                      f'{nminutes} '
                      f'{data.minutes_he.get(nminutes, "דקות")} '
                      f'ו {nchalakim}'
                      f' {data.chalakim_he.get(chalakim, "חלקים")}'
        }
        molad_str = responses.get(lang, '')
        return molad_str

    # определяем РХ
    @staticmethod
    def get_rh_str(
            lang: str,
            month: str,
            length: int,
            rosh_hodesh: str,
            molad: str
    ) -> str:
        responses = {
            'Russian': f'Месяц: |{data.jewish_months[month]}\n'
                       f'Число дней: |{length} '
                       f'{data.length_ru[f"{length}"]}\n'
                       f'Дата: |{rosh_hodesh}\nМолад: |{molad}',
            'English': f'Month: |{month}\n'
                       f'Number of days: |{length} '
                       f'{data.length_en[f"{length}"]}\n'
                       f'Date: |{rosh_hodesh}\nMolad: |{molad}',
            'Hebrew': f'*חודש:* |{data.jewish_months_he[month]}\n'
                      f' *משך ראש חודש:* |{length}'
                      f' {data.length_he[f"{length}"]}\n '
                      f'ראש חודש: |{rosh_hodesh}\nמולד: |{molad}'
        }
        rh = responses.get(lang, '')
        return rh


# ЛОКАЛИЗАЦИЯ ДЛЯ ШАББАТА
class Shabos(object):
    titles = {
        'Russian': 'ШАББАТ',
        'English': 'SHABBOS',
        'Hebrew': 'שבת'
    }

    # TODO  ошибки вида   if parasha == 'PESACH_VIII': parasha = 'PESACH'
    # для шаббатов, в которых невозможно вычислить зманим
    @staticmethod
    def shabos_with_latitude_error(lang: str, parasha: str) -> str:
        responses = {
            'Russian': f'Недельная глава: |{data.parashat[parasha]}?'
                       f'В данных широтах невозможно\nопределить '
                       f'зманим из-за\nполярного дня/полярной ночи.',
            'English': f'Parshat hashavua: |{parasha}?'
                       f'For this location zmanim is impossible\n'
                       f'to determine because of polar night/day.',
            'Hebrew': f'פרשת השבוע: |{data.parashat_he[parasha]}?'
                      f'לא ניתן לקבוע את הזמן בגלל ליל קוטב/שמש'
                      f'חצות בקווי הרוחב האלו '
        }
        shabos_str = responses.get(lang, '')
        return shabos_str

    # для шаббатов в северных широтах с предупреждением о раннем зажигании
    @staticmethod
    def shabos_with_warning(
            lang: str,
            parasha: str,
            cl: str,
            th: str,
            offset: int
    ) -> str:
        responses = {
            'Russian': f'Недельная глава: |{data.parashat[parasha]}\n'
                       f'Зажигание свечей: |{cl}\n'
                       f'+({offset}/ минут до шкии\n'
                       f'Выход звёзд:  |{th}%'
                       f'Внимание! Необходимо уточнить '
                       f'время \nзажигания свечей у раввина общины!',
            'English': f'Parshat hashavua: |{parasha}\n'
                       f'Candle lighting: |{cl}\n'
                       f'+({offset}/ minutes before shekiah)\n'
                       f'Tzeit hakochavim: |{th}%'
                       f'Notice! You should specify time of candle\n'
                       f'lighting with the rabbi of your community.',
            'Hebrew': f'פרשת השבוע: |{data.parashat_he[parasha]}\n'
                      f'הדלקת נרות: |{cl}\n'
                      f'צאת הכוכבים: |{th}%'
                      f'!לתשומת לבך '
                      f'!יש לעדכן את זמן הדלקת הנרות אצל רב הקהילה'
        }
        shabos_str = responses.get(lang, '')
        return shabos_str

    # для обычных шаббатов
    @staticmethod
    def shabos(
            lang: str,
            parasha: str,
            cl: str,
            th: str,
            offset: int
    ) -> str:
        responses = {
            'Russian': f'Недельная глава:  | {data.parashat[parasha]}\n'
                       f'Зажигание свечей: |{cl}\n'
                       f'+({offset}/ минут до шкии)\n'
                       f'Выход звёзд:  |{th}',
            'English': f'Parshat hashavua: |{parasha}\n'
                       f'Candle lighting: |{cl}\n'
                       f'+({offset}/ minutes before shekiah)\n'
                       f'Tzeit hakochavim: |{th}',
            'Hebrew': f'פרשת השבוע: |{data.parashat_he[parasha]}\n'
                      f'הדלקת נרות: |{cl}\n'
                      #TODO
                      f'צאת הכוכבים: |{th}'
        }
        shabos_str = responses.get(lang, '')
        return shabos_str

    # настройки сдвига зажиганий
    @staticmethod
    def shabos_candle_offset(lang: str) -> str:
        responses = {
            'Russian': 'Выберите, за сколько минут до Шкии '
                       'будет зажигание свечей:',
            'English': '',  # TODO перевод
            'Hebrew': ''  # TODO перевод
        }
        response = responses.get(lang, '')
        return response

    # выбран тот же сдвиг
    @staticmethod
    def same_offset_error(lang: str) -> str:
        responses = {
            'Russian': 'Чтобы изменить сдвиг, выберите другое значение.',
            'English': '',  # TODO перевод
            'Hebrew': ''  # TODO перевод
        }
        response = responses.get(lang, '')
        return response


# ЛОКАЛИЗАЦИЯ ДЛЯ ЗМАНИМ
class Zmanim(object):

    # ошибка полярных широт
    @staticmethod
    def get_polar_error(lang: str) -> str:
        responses = {
            'Russian': 'В данных широтах невозможно определить '
                       'зманим из-за полярного дня/полярной ночи.',
            'English': 'In these latitudes it is impossible to determine'
                       ' because of polar night/day.',
            'Hebrew': 'לא ניתן לקבוע את הזמן בגלל ליל'
                      ' קוטב/שמש חצות בקווי הרוחב האלו'
        }
        error_message = responses.get(lang, '')
        return error_message

    # названия зманим для настроек
    @staticmethod
    def get_zman_name(zman: str, lang: str) -> str:
        zman_names = {
            'Russian': data.zmanim_ru[zman],
            'English': data.zmanim_en[zman],
            'Hebrew': data.zmanim_he[zman]
        }
        zman_name = zman_names.get(lang, '')
        return zman_name


# ЛОКАЛИЗАЦИЯ ДЛЯ ВСПОМОГАТЕЛЬНЫХ ФУНКЦИЙ
class Utils(object):

    # перешли в меню постов
    @staticmethod
    def get_fast_menu(lang: str) -> str:
        responses = {
            'Russian': 'Выберите:',
            'English': 'Choose:',
            'Hebrew': 'בחר:'
        }
        response = responses.get(lang, '')
        return response

    # перешли в основное меню
    @staticmethod
    def get_main_menu(lang: str) -> str:
        responses = {
            'Russian': 'Выберите:',
            'English': 'Choose:',
            'Hebrew': 'בחר:'
        }
        response = responses.get(lang, '')
        return response

    # перешли в меню праздников
    @staticmethod
    def get_holiday_menu(lang: str) -> str:
        responses = {
            'Russian': 'Выберите: (клавиатуру можно скроллить)',
            'English': 'Choose: (scroll keyboard)',
            'Hebrew': 'празднички' #TODO перевод
        }
        response = responses.get(lang, '')
        return response

    # перешли дальше по меню праздников
    @staticmethod
    def get_more_holiday_menu(lang: str) -> str:
        responses = {
            'Russian': 'Выберите:',
            'English': 'Choose:',
            'Hebrew': 'בחר:'
        }
        response = responses.get(lang, '')
        return response

    # координаты получены
    @staticmethod
    def location_received(lang: str) -> str:
        responses = {
            'Russian': 'Координаты получены, теперь вы можете '
                       'начать работать с ботом.',
            'English': 'Location has been received, now you can start '
                       'working with the bot',
            'Hebrew': 'המיקום התקבל, כעת אתם יכולים להתחיל לעבוד עם ה bot.'
        }
        response = responses.get(lang, '')
        return response

    # ошибка определения тз
    @staticmethod
    def failed_check_tz(lang: str) -> str:
        responses = {
            'Russian': 'Не получилось определить часовой пояс. Возможно '
                       'вы находитесь далеко от берега или указали '
                       'неверные координаты. Попробуйте отправить свое'
                       ' местоположение еще раз',
            'English': 'Time zone could not be determined. Рrobably, you'
                       ' аre far from сoast or indicate incorrect '
                       'coordinates. Try to send your location again.',
            'Hebrew': 'אזור הזמן לא ניתן לקביעה. כנראה שהינך רחוק מחוף או '
                      'שמצוינות נקודות ציון שגויות. נסו לשלוח את המיקום מחדש.'

        }
        response = responses.get(lang, '')
        return response

    # некорректный текст
    @staticmethod
    def incorrect_text(lang: str) -> str:
        responses = {
            'Russian': 'Некорректная команда. Пожалуйста, выберите один из '
                       'вариантов на кнопках.',
            'English': 'Incorrect command. Please, choose one of the options '
                       'on the buttons',
            'Hebrew': 'פקודה שגויה. נא לבחור אחת מהאפשרויות שבלחצנים.'
        }
        response = responses.get(lang, '')
        return response

    # запрос координат
    @staticmethod
    def request_location(lang: str) -> str:
        responses = {
            'Russian': 'Пожалуйста, предоставьте новые координаты, нажав на '
                       'кнопку.\n*Внимание*! Telegram на ПК пока что не '
                       'поддерживает отправку координат таким методом. Чтобы '
                       'отправить координаты с ПК, отправьте их в текстовом '
                       'виде через запятую, например "_55.5, 37.7_", либо '
                       'перешлите сюда сообщение с геометкой.',
            'English': 'Please, send new location by tapping the button.\n'
                       '*Notice* that Telegram on PC is not supported yet '
                       'sending locations in this way. In order to send '
                       'location on PC, send it like text, for example, '
                       '"_55.5, 37.7_", or forward message '
                       'with location here.',
            'Hebrew': 'נא לשלוח מיקום חדש ע״י הקשה על הכפתור . שימו לב שגרסת'
                      ' המחשב של טלגרם לא נתמכת בשליחת מיקומים בדרך זו. על '
                      'מנת לשלוח מיקום על מחשב, יש לשלוח אותו בצורה של טקסט, '
                      'לדוגמא: ״_55.5, 37.7_״ , או להעביר הודעה עם המיקום כאן.'

        }
        response = responses.get(lang, '')
        return response

    # сообщить об ошибке
    @staticmethod
    def report(lang: str) -> str:
        responses = {
            'Russian': 'Чтобы сообщить об ошибке, пожалуйста, напишите одному '
                       'из разработчиков: \nt.me/benyomin \nt.me/Meir_Yartzev'
                       '\nt.me/APJIAC \n'
                       'Пожалуйста, убедитесь, что вы ознакомились с часто '
                       'задаваемыми вопросами, доступными по кнопке "ЧаВо" ',
            'English': 'For bug report please write to one of developers: \n'
                       't.me/benyomin \nt.me/Meir_Yartzev \nt.me/APJIAC\n'
                       'Please, make sure that you '
                       'had been read F.A.Q. available by "F.A.Q." button',
            'Hebrew': 'לדיווח על באגים נא לכתוב לאחד המפתחים:'
                      '\nt.me/benyomin\n'
                      't.me/Meir_Y\n'
                      't.me/APJIAC\n'
                      'נא לוודא שקראת את ה FAQ (שאלות ותשובות)'
                      ' שנמצא בכפתור ה FAQ.'
        }
        response = responses.get(lang, '')
        return response

    # запрос даты для зманим
    @staticmethod
    def request_date(lang: str) -> str:
        responses = {
            'Russian': 'Пожалуйста, введите дату, на которую вы '
                       'хотите получить _зманим_ *в формате ДД.ММ.ГГГГ*',
            'English': 'Please enter the date to calculate the _Zmanim_  '
                       'for your selection *in the format DD.MM.YYYY*',
            'Hebres': 'נא להזין תאריך על מנת לחשב את ה_Zmanim_'
                      ' עבור הבחירה שלך ב*פורמט DD.MM.YYY'
        }
        response = responses.get(lang, '')
        return response

    # некорректная дата
    @staticmethod
    def incorrect_date_format(lang: str) -> str:
        responses = {
            'Russian': 'Вы ввели некорректную дату. \nПожалуйста, введите '
                       'дату в *формате ДД.ММ.ГГГГ*',
            'English': 'Incorrect date. \nPlease input date *in '
                       'the format DD.MM.YYYY*',
            'Hebrew': 'התאריך שגוי. נא להזין תאריך ב*פורמט של DD.MM.YYYY'
        }
        response = responses.get(lang, '')
        return response

    # сообщение об ошибке в дате
    @staticmethod
    def incorrect_date_value(lang: str) -> str:
        responses = {
            'Russian': 'Введенная дата не существует. \nПожалуйста, введите '
                       'корректную дату в *формате ДД.ММ.ГГГГ*',
            'English': 'The date that you entered doesn\'t exist, '
                       'please enter the correct date in format DD.MM.YYYY',
            'Hebrew': '' #TODO перевод
        }
        response = responses.get(lang, '')
        return response

    # вкл/откл израильский режим
    @staticmethod
    def diaspora(lang: str, status: bool) -> str:
        if status:
            diaspora_activated = data.diaspora_mode_activated[lang]
        else:
            diaspora_activated = data.diaspora_mode_deactivated[lang]
        responses = {
            'Russian': f'Режим диаспоры {diaspora_activated}\n'
                       f'Чтобы изменить режим, нажмите на кнопку.',
            'English': '',  # TODO перевод
            'Hebrew': ''  # TODO перевод
        }
        response = responses.get(lang, '')
        return response

    @staticmethod
    def diaspora_status_allert(lang: str, status: bool) -> str:
        if status:
            responses = {
                'Russian': 'Режим диаспоры включен!',
                'English': 'Diaspora mode enabled!',  #
                'Hebrew': ''  # TODO перевод
            }
        else:
            responses = {
                'Russian': 'Режим диаспоры выключен!',
                'English': 'Diaspora mode disabled!',  #
                'Hebrew': ''  # TODO перевод
            }
        response = responses.get(lang, '')
        return response



# ЛОКАЛИЗАЦИЯ ДЛЯ ПРАЗДНИКОВ
class Holidays(object):

    # Когда невозможно определить времена
    @staticmethod
    def polar_area(lang: str) -> str:
        responses = {
            'Russian': '\nВ данных широтах невозможно определить'
                       ' зманим из-за полярного дня/полярной ночи',
            'English': '\nIn these latitudes zmanim is impossible'
                       ' to determine because of polar night/day',
            'Hebrew': 'לא ניתן לקבוע את הזמן בגלל ליל'
                      ' קוטב/שמש חצות בקווי הרוחב האלו'
        }
        ra_time = responses.get(lang, '')
        return ra_time

    # Когда один день праздника
    @staticmethod
    def lighting(
            lang: str,
            light_day: str,
            light_month: str,
            light_time: str,
            avdala_day: str,
            avdala_month: str,
            avdala_time: str
    ) -> str:
        responses = {
            'Russian': f'🕯 Зажигание свечей {light_day}'
                       f' {data.gr_months_index[light_month]}:'
                       f' *{light_time:.5s}*\n'
                       f'✨ Авдала {avdala_day}'
                       f' {data.gr_months_index[avdala_month]}:'
                       f' *{avdala_time:.5s}*',
            'English': f'🕯 Candle lighting {light_day}'
                       f' {data.gr_months_index_en[light_month]}:'
                       f' *{light_time:.5s}*\n'
                       f'✨ Avdala {avdala_day}'
                       f' {data.gr_months_index_en[avdala_month]}:'
                       f' *{avdala_time:.5s}*',
            'Hebrew': f'🕯 הדלקת נרות {light_day}'
                      f' {data.gr_months_index_he[light_month]}:'
                      f' *{light_time:.5s}*\n'
                      f'✨ הבדלה {avdala_day}'
                      f' {data.gr_months_index_en[avdala_month]}:'
                      f' *{avdala_time:.5s}*'
            }
        lighting_time = responses.get(lang, '')
        return lighting_time

    # Когда один день праздника и перед ним шаббат
    @staticmethod
    def one_day_shabbat_before(
            lang: str,
            light_shab_day: str,
            light_shab_month: str,
            light_shab_time: str,
            light_day: str,
            light_month: str,
            light_time: str,
            avdala_day: str,
            avdala_month: str,
            avdala_time: str
    ) -> str:
        responses = {
            'Russian': f'🕯 Зажигание свечей (Шаббат) {light_shab_day}'
                       f' {data.gr_months_index[light_shab_month]}:'
                       f' *{light_shab_time:.5s}*\n'
                       f'✨🕯 Авдала и зажигание свечей {light_day}'
                       f' {data.gr_months_index[light_month]}:'
                       f' *{light_time:.5s}*\n'
                       f'✨ Авдала {avdala_day}'
                       f' {data.gr_months_index[avdala_month]}:'
                       f' *{avdala_time:.5s}*',
            'English': f'🕯 Candle lighting (Shabbat) {light_shab_day}'
                       f' {data.gr_months_index_en[light_shab_month]}:'
                       f' *{light_shab_time:.5s}*\n'
                       f'✨🕯 Avdala and candle lighting {light_day}'
                       f' {data.gr_months_index_en[light_month]}:'
                       f' *{light_time:.5s}*\n'
                       f'✨ Avdala {avdala_day}'
                       f' {data.gr_months_index_en[avdala_month]}:'
                       f' *{avdala_time:.5s}*',
            'Hebrew': f'🕯 הדלקת נרות שבת {light_shab_day}'
                      f' {data.gr_months_index_he[light_shab_month]}:'
                      f' *{light_shab_time:.5s}*\n'
                      f'✨🕯 הבדלה והדלקת נרות {light_day}'
                      f' {data.gr_months_index_he[light_month]}:'
                      f' *{light_time:.5s}*\n'
                      f'✨ הבדלה {avdala_day}'
                      f' {data.gr_months_index_he[avdala_month]}:'
                      f' *{avdala_time:.5s}*'
        }
        lighting_time = responses.get(lang, '')
        return lighting_time

    # Для Йом-Кипура
    @staticmethod
    def fast_yom_kippur(
            lang: str,
            light_day: str,
            light_month: str,
            light_time: str,
            avdala_day: str,
            avdala_month: str,
            avdala_time: str
    ) -> str:
        responses = {
            'Russian': f'🕯 Зажигание свечей и начало поста {light_day}'
                       f' {data.gr_months_index[light_month]}:'
                       f' *{light_time:.5s}*\n'
                       f'✨ Авдала и конец поста {avdala_day}'
                       f' {data.gr_months_index[avdala_month]}:'
                       f' *{avdala_time:.5s}*',
            'English': f'🕯 Candle lighting and the fast begins {light_day}'
                       f' {data.gr_months_index[light_month]}:'
                       f' *{light_time:.5s}*\n'
                       f'✨ Avdala and the fast ends {avdala_day}'
                       f' {data.gr_months_index_en[avdala_month]}:'
                       f' *{avdala_time:.5s}*',
            'Hebrew': f'🕯 הדלקת הנרות ותחילת הצום {light_day}'
                      f' {data.gr_months_index_he[light_month]}:'
                      f' *{light_time:.5s}*\n'
                      f'✨ הבדלה ויציאת הצום {avdala_day}'
                      f' {data.gr_months_index_he[avdala_month]}:'
                      f' *{avdala_time:.5s}*'
        }
        ra_time = responses.get(lang, '')
        return ra_time

    # Для обычных постов
    @staticmethod
    def single_fast(
            lang: str,
            day: str,
            month: str,
            time_begin: str,
            time_end: str,
            ben_ashmashot: str,
            nevareshet: str,
            shmirat_shabat: str
    ) -> str:
        responses = {
            'Russian': f'Начало поста {day} {data.gr_months_index[month]}:'
                       f' *{time_begin[:-3:]}*\n'
                       f'Конец поста {day} {data.gr_months_index[month]}'
                       f'\n✨ Выход звезд: *{time_end[:-3:]}*\n'
                       f'🕖 Сефер бен Ашмашот: *{ben_ashmashot[:-3:]}'
                       f'*\n🕘 Неварешет: *{nevareshet[:-3:]}*\n'
                       f'🕑 Шмират шаббат килхата:'
                       f' *{shmirat_shabat[:-3:]}*',
            'English':  f'The fast begins {day} '
                        f'{data.gr_months_index_en[month]}:'
                        f' *{time_begin[:-3:]}*\n'
                        f'Fast ends {day} {data.gr_months_index_en[month]}'
                        f'\n✨ Tzeit akohavim: *{time_end[:-3:]}*\n'
                        f'🕖 Sefer ben Ashmashot:'
                        f' *{ben_ashmashot[:-3:]}*\n'
                        f'🕘 Nevareshet: *{nevareshet[:-3:]}*\n'
                        f'🕑 Shmirat shabbat kelhata:'
                        f' *{shmirat_shabat[:-3:]}*',
            'Hebrew': f'תחילת הצום {day} '
                      f'{data.gr_months_index_he[month]}:'
                      f' *{time_begin[:-3:]}*\n'
                      f'הצום יוצא ב-{day} {data.gr_months_index_he[month]}'
                      f'\n✨ צאת הכוכבים *{time_end[:-3:]}*\n'
                      f'🕖 ספר בין השמשות:'
                      f' *{ben_ashmashot[:-3:]}*\n'
                      f'🕘 נברשת: *{nevareshet[:-3:]}*\n'
                      f'🕑 שמירת שבת כהלכתה:'
                      f' *{shmirat_shabat[:-3:]}*'
        }
        holiday_number = responses.get(lang, '')
        return holiday_number

    # Когда 2 дня праздника и один из них шаббат
    @staticmethod
    def lighting_shabbat(
            lang: str,
            light_day: str,
            light_month: str,
            light_time: str,
            light_shab_day: str,
            light_shab_month: str,
            light_shab_time: str,
            avdala_day: str,
            avdala_month: str,
            avdala_time: str
    ) -> str:
        responses = {
            'Russian': f'🕯 Зажигание свечей {light_day}'
                       f' {data.gr_months_index[light_month]}:'
                       f' *{light_time:.5s}*\n'
                       f'🕯 Зажигание свечей (Шаббат) {light_shab_day} '
                       f'{data.gr_months_index[light_shab_month]}: '
                       f'*{light_shab_time:.5s}*\n'
                       f'✨ Авдала {avdala_day}'
                       f' {data.gr_months_index[avdala_month]}:'
                       f' *{avdala_time:.5s}*',
            'English': f'🕯 Candle lighting {light_day}'
                       f' {data.gr_months_index_en[light_month]}:'
                       f' *{light_time:.5s}*\n'
                       f'🕯 Candle lighting (Shabbat) {light_shab_day} '
                       f'{data.gr_months_index_en[light_shab_month]}: '
                       f'*{light_shab_time:.5s}*\n'
                       f'✨ Avdala {avdala_day}'
                       f' {data.gr_months_index_en[avdala_month]}:'
                       f' *{avdala_time:.5s}*',
            'Hevrew': f'🕯 הדלקת נרות {light_day}'
                      f' {data.gr_months_index_he[light_month]}:'
                      f' *{light_time:.5s}*\n'
                      f'{light_shab_day} הדלקת נרות שבת 🕯'
                      f'{data.gr_months_index_he[light_shab_month]}:'
                      f'*{light_shab_time:.5s}*\n'
                      f'✨ הבדלה {avdala_day}'
                      f' {data.gr_months_index_he[avdala_month]}:'
                      f' *{avdala_time:.5s}*'
        }
        ra_time = responses.get(lang, '')
        return ra_time

    # Когда 2 дня праздника и перед ними шаббат
    @staticmethod
    def shabbat_before_holiday_diaspora(
            lang: str,
            light_shab_day: str,
            light_shab_month: str,
            light_shab_time: str,
            light_1_day: str,
            light_1_month: str,
            light_1_time: str,
            light_2_day: str,
            light_2_month: str,
            light_2_time: str,
            avdala_day: str,
            avdala_month: str,
            avdala_time: str
    ) -> str:
        responses = {
            'Russian': f'🕯 Зажигание свечей (Шаббат) {light_shab_day}'
                       f' {data.gr_months_index[light_shab_month]}:'
                       f' *{light_shab_time:.5s}*\n'
                       f'✨🕯 Авдала и зажигание свечей {light_1_day}'
                       f' {data.gr_months_index[light_1_month]}:'
                       f' *{light_1_time:.5s}*\n'
                       f'🕯 Зажигание свечей {light_2_day}'
                       f' {data.gr_months_index[light_2_month]}:'
                       f' *{light_2_time:.5s}*\n'
                       f'✨ Авдала {avdala_day}'
                       f' {data.gr_months_index[avdala_month]}:'
                       f' *{avdala_time:.5s}*',
            'English': f'🕯 Candle lighting (Shabbat) {light_shab_day}'
                       f' {data.gr_months_index_en[light_shab_month]}:'
                       f' *{light_shab_time:.5s}*\n'
                       f'✨🕯 Avdala and candle lighting {light_1_day}'
                       f' {data.gr_months_index_en[light_1_month]}:'
                       f' *{light_1_time:.5s}*\n'
                       f'🕯 Candle lighting {light_2_day}'
                       f' {data.gr_months_index_en[light_2_month]}: '
                       f'*{light_2_time:.5s}*\n'
                       f'✨ Avdala {avdala_day}'
                       f' {data.gr_months_index_en[avdala_month]}:'
                       f' *{avdala_time:.5s}*',
            'Hebrew': f'🕯 הדלקת נרות שבת {light_shab_day}'
                      f' {data.gr_months_index_he[light_shab_month]}:'
                      f' *{light_shab_time:.5s}*\n'
                      f'✨🕯 הבדלה והדלקת נרות {light_1_day}'
                      f' {data.gr_months_index_he[light_1_month]}:'
                      f' *{light_1_time:.5s}*\n'
                      f'🕯 הדלקת נרות {light_2_day}'
                      f' {data.gr_months_index_he[light_2_month]}: '
                      f'*{light_2_time:.5s}*\n'
                      f'✨ הבדלה {avdala_day}'
                      f' {data.gr_months_index_he[avdala_month]}:'
                      f' *{avdala_time:.5s}*'
        }
        ra_time = responses.get(lang, '')
        return ra_time

    # 2 дня праздника (без шаббата)
    @staticmethod
    def lighting_double(
            lang: str,
            light_1_day: str,
            light_1_month: str,
            light_1_time: str,
            light_2_day: str,
            light_2_month: str,
            light_2_time: str,
            avdala_day: str,
            avdala_month: str,
            avdala_time: str
    ) -> str:
        responses = {
            'Russian': f'🕯 Зажигание свечей {light_1_day}'
                       f' {data.gr_months_index[light_1_month]}:'
                       f' *{light_1_time:.5s}*\n'
                       f'🕯 Зажигание свечей {light_2_day}'
                       f' {data.gr_months_index[light_2_month]}:'
                       f' *{light_2_time:.5s}*\n'
                       f'✨ Авдала {avdala_day}'
                       f' {data.gr_months_index[avdala_month]}:'
                       f' *{avdala_time:.5s}*',
            'English': f'🕯 Candle lighting {light_1_day}'
                       f' {data.gr_months_index_en[light_1_month]}:'
                       f' *{light_1_time:.5s}*\n'
                       f'🕯 Candle lighting {light_2_day}'
                       f' {data.gr_months_index_en[light_2_month]}:'
                       f' *{light_2_time:.5s}*\n'
                       f'✨ Avdala {avdala_day}'
                       f' {data.gr_months_index_en[avdala_month]}:'
                       f' *{avdala_time:.5s}*',
            'Hebrew': f'🕯 הדלקת נרות {light_1_day}'
                      f' {data.gr_months_index_he[light_1_month]}:'
                      f' *{light_1_time:.5s}*\n'
                      f'🕯 הדלקת נרות {light_2_day}'
                      f' {data.gr_months_index_he[light_2_month]}:'
                      f' *{light_2_time:.5s}*\n'
                      f'✨ הבדלה {avdala_day}'
                      f' {data.gr_months_index_he[avdala_month]}:'
                      f' *{avdala_time:.5s}*'
        }
        ra_time = responses.get(lang, '')
        return ra_time

    # 2 дня праздника (с шаббатом)
    @staticmethod
    def shabbat_include(
            lang: str,
            light_1_day: str,
            light_1_month: str,
            light_1_time: str,
            light_2_day: str,
            light_2_month: str,
            light_2_time: str,
            avdala_day: str,
            avdala_month: str,
            avdala_time: str
    ) -> str:
        responses = {
            'Russian': f'🕯 Зажигание свечей {light_1_day}'
                       f' {data.gr_months_index[light_1_month]}:'
                       f' *{light_1_time:.5s}*\n'
                       f'🕯 Зажигание свечей {light_2_day}'
                       f' {data.gr_months_index[light_2_month]}:'
                       f' *{light_2_time:.5s}*\n'
                       f'✨ Авдала {avdala_day}'
                       f' {data.gr_months_index[avdala_month]}:'
                       f' *{avdala_time:.5s}*',
            'English': f'🕯 Candle lighting {light_1_day}'
                       f' {data.gr_months_index_en[light_1_month]}:'
                       f' *{light_1_time:.5s}*\n'
                       f'🕯 Candle lighting {light_2_day}'
                       f' {data.gr_months_index_en[light_2_month]}:'
                       f' *{light_2_time:.5s}*\n'
                       f'✨ Avdala {avdala_day}'
                       f' {data.gr_months_index_en[avdala_month]}:'
                       f' *{avdala_time:.5s}*',
            'Hebrew': f'🕯 הדלקת נרות {light_1_day} '
                      f' {data.gr_months_index_he[light_1_month]}:'
                      f' *{light_1_time:.5s}*\n'
                      f'🕯 הדלקת נרות {light_2_day}'
                      f' {data.gr_months_index_he[light_2_month]}:'
                      f' *{light_2_time:.5s}*\n'
                      f'✨ הבדלה {avdala_day}'
                      f' {data.gr_months_index_he[avdala_month]}:'
                      f' *{avdala_time:.5s}*'
        }
        ra_time = responses.get(lang, '')
        return ra_time

    # 2 дня прадника и после них идет шаббат
    @staticmethod
    def lighting_double_shabbat(
            lang: str,
            light_1_day: str,
            light_1_month: str,
            light_1_time: str,
            light_2_day: str,
            light_2_month: str,
            light_2_time: str,
            light_shab_day: str,
            light_shab_month: str,
            light_shab_time: str,
            avdala_day: str,
            avdala_month: str,
            avdala_time: str
    ) -> str:
        responses = {
            'Russian': f'🕯 Зажигание свечей {light_1_day}'
                       f' {data.gr_months_index[light_1_month]}:'
                       f' *{light_1_time:.5s}*\n'
                       f'🕯 Зажигание свечей {light_2_day}'
                       f' {data.gr_months_index[light_2_month]}:'
                       f' *{light_2_time:.5s}*\n'
                       f'🕯 Зажигание свечей (Шаббат) {light_shab_day}'
                       f' {data.gr_months_index[light_shab_month]}:'
                       f' *{light_shab_time:.5s}*\n'
                       f'✨ Авдала {avdala_day}'
                       f' {data.gr_months_index[avdala_month]}:'
                       f' *{avdala_time:.5s}*',
            'English': f'🕯 Candle lighting {light_1_day}'
                       f' {data.gr_months_index_en[light_1_month]}:'
                       f' *{light_1_time:.5s}*\n'
                       f'🕯 Candle lighting {light_2_day}'
                       f' {data.gr_months_index_en[light_2_month]}:'
                       f' *{light_2_time:.5s}*\n'
                       f'🕯 Candle lighting (Shabbat) {light_shab_day}'
                       f' {data.gr_months_index_en[light_shab_month]}: '
                       f'*{light_shab_time:.5s}*\n'
                       f'✨ Avdala {avdala_day}'
                       f' {data.gr_months_index_en[avdala_month]}:'
                       f' *{avdala_time:.5s}*',
            'Hebrew': f'🕯 הדלקת נרות {light_1_day} '
                      f' {data.gr_months_index_he[light_1_month]}:'
                      f' *{light_1_time:.5s}*\n'
                      f'🕯 הדלקת נרות {light_2_day}'
                      f' {data.gr_months_index_he[light_2_month]}:'
                      f' *{light_2_time:.5s}*\n'
                      f'🕯 הדלקת נרות שבת {light_shab_day}'
                      f' {data.gr_months_index_he[light_shab_month]}: '
                      f'*{light_shab_time:.5s}*\n'
                      f'✨ הבדלה {avdala_day}'
                      f' {data.gr_months_index_he[avdala_month]}:'
                      f' *{avdala_time:.5s}*'
        }
        ra_time = responses.get(lang, '')
        return ra_time

    # Длинные праздники (Пейсах, Ханука; Суккот не входит),
    # даты которых приходят на 1 григорианский месяц
    @staticmethod
    def long_holiday_one_month(
            lang: str,
            day_start: str,
            day_end: str,
            month: str,
            year: int,
            weekday_start: str,
            weekday_end: str
    ) -> str:
        responses = {
            'Russian': f'📅 Дата: {day_start}-'
                       f'{day_end}'
                       f' {data.gr_months_index[month]}'
                       f' {year} годa,'
                       f' {data.hdays_of_7[weekday_start]}-'
                       f'{data.hdays_of_7[weekday_end]}',
            'English': f'📅 Date: {day_start}-'
                       f'{day_end}'
                       f' {data.gr_months_index_en[month]}'
                       f' {year}, '
                       f'{data.hdays_of_7_en[weekday_start]}-'
                       f'{data.hdays_of_7_en[weekday_end]}',
            'Hebrew': f'📅 תאריך:'
                      f' {day_start}-{day_end}'
                      f' {data.gr_months_index_he[month]}'
                      f' {year}, '
                      f'{data.hdays_of_7_he[weekday_start]} - '
                      f'{data.hdays_of_7_he[weekday_end]}'
        }
        holiday_number = responses.get(lang, '')
        return holiday_number

    # Двухдневные праздники, даты которых приходят на 1 григорианский месяц
    @staticmethod
    def two_days_holiday_one_month(
            lang: str,
            day_start: str,
            day_end: str,
            month: str,
            year: int,
            weekday_start: str,
            weekday_end: str
    ) -> str:
        responses = {
            'Russian': f'📅 Дата: {day_start} и '
                       f'{day_end}'
                       f' {data.gr_months_index[month]}'
                       f' {year} годa,'
                       f' {data.hdays_of_7[weekday_start]}-'
                       f'{data.hdays_of_7[weekday_end]}',
            'English': f'📅 Date: {day_start} and '
                       f'{day_end}'
                       f' {data.gr_months_index_en[month]}'
                       f' {year}, '
                       f'{data.hdays_of_7_en[weekday_start]}-'
                       f'{data.hdays_of_7_en[weekday_end]}',
            'Hebrew': f'📅 תאריך: '
                      f'{day_start} ו-' 
                      f'{day_end}'
                      f' {data.gr_months_index_he[month]}'
                      f' {year}, '
                      f'{data.hdays_of_7_he[weekday_start]} - '
                      f'{data.hdays_of_7_he[weekday_end]}'
        }
        holiday_number = responses.get(lang, '')
        return holiday_number

    # Длинные праздники, даты которых приходят на 2 григорианских месяца
    @staticmethod
    def long_holiday_two_months(
            lang: str,
            day_start: str,
            month_start: str,
            day_end: str,
            month_end: str,
            year: int,
            weekday_start: str,
            weekday_end: str
    ) -> str:
        responses = {
            'Russian': f'📅 Дата: {day_start}'
                       f' {data.gr_months_index[month_start]} - '
                       f'{day_end}'
                       f' {data.gr_months_index[month_end]}'
                       f' {year} годa,'
                       f' {data.hdays_of_7[weekday_start]}-'
                       f'{data.hdays_of_7[weekday_end]}',
            'English': f'📅 Date: {day_start}'
                       f' {data.gr_months_index_en[month_start]} - '
                       f'{day_end}'
                       f' {data.gr_months_index_en[month_end]}'
                       f' {year}, '
                       f'{data.hdays_of_7_en[weekday_start]}-'
                       f'{data.hdays_of_7_en[weekday_end]}',
            'Hebrew': f'📅 תאריך: '
                      f'{day_start} {data.gr_months_index_he[month_start]} - '
                      f'{day_end}'
                      f' {data.gr_months_index_he[month_end]}'
                      f' {year}, '
                      f'{data.hdays_of_7_he[weekday_start]} - '
                      f'{data.hdays_of_7_he[weekday_end]}'
        }
        holiday_number = responses.get(lang, '')
        return holiday_number

    @staticmethod
    def long_holiday_two_months_two_years(
            lang: str,
            day_start: str,
            month_start: str,
            year_start: int,
            day_end: str,
            month_end: str,
            year_end: int,
            weekday_start: str,
            weekday_end: str
    ) -> str:

        responses = {
            'Russian': f'📅 Дата: {day_start}'
                       f' {data.gr_months_index[month_start]} '
                       f'{year_start} года - '
                       f'{day_end}'
                       f' {data.gr_months_index[month_end]}'
                       f' {year_end} годa,'
                       f' {data.hdays_of_7[weekday_start]}-'
                       f'{data.hdays_of_7[weekday_end]}',
            'English': f'📅 Date: {day_start}'
                       f' {data.gr_months_index_en[month_start]}'
                       f' {year_start} - '
                       f'{day_end}'
                       f' {data.gr_months_index_en[month_end]}'
                       f' {year_end}, '
                       f'{data.hdays_of_7_en[weekday_start]}-'
                       f'{data.hdays_of_7_en[weekday_end]}',
            'Hebrew': f'📅 תאריך: '
                      f'{day_start} {data.gr_months_index_he[month_start]} '
                      f'{year_start} - '
                      f'{day_end}'
                      f' {data.gr_months_index_he[month_end]}'
                      f' {year_end}, '
                      f'{data.hdays_of_7_he[weekday_start]} - '
                      f'{data.hdays_of_7_he[weekday_end]}'
        }
        holiday_number = responses.get(lang, '')
        return holiday_number

    # Двухдневные праздники, даты которых приходят на 2 григорианских месяца
    @staticmethod
    def two_days_holiday_two_months(
            lang: str,
            day_start: str,
            month_start: str,
            day_end: str,
            month_end: str,
            year: int,
            weekday_start: str,
            weekday_end: str
    ) -> str:
        responses = {
            'Russian': f'📅 Дата: {day_start}'
                       f' {data.gr_months_index[month_start]} и '
                       f'{day_end}'
                       f' {data.gr_months_index[month_end]}'
                       f' {year} годa,'
                       f' {data.hdays_of_7[weekday_start]}-'
                       f'{data.hdays_of_7[weekday_end]}',
            'English': f'📅 Date: {day_start}'
                       f' {data.gr_months_index_en[month_start]} and '
                       f'{day_end}'
                       f' {data.gr_months_index_en[month_end]}'
                       f' {year}, '
                       f'{data.hdays_of_7_en[weekday_start]}-'
                       f'{data.hdays_of_7_en[weekday_end]}',
            'Hebrew': f'📅 תאריך:'
                      f' {day_start} {data.gr_months_index_he[month_start]} ו-'
                      f'{day_end}'
                      f' {data.gr_months_index_he[month_end]}'
                      f' {year}, '
                      f'{data.hdays_of_7_he[weekday_start]}-'
                      f'{data.hdays_of_7_he[weekday_end]}'
        }
        holiday_number = responses.get(lang, '')
        return holiday_number

    # Однодневные праздники
    @staticmethod
    def one_day_holiday(
            lang: str,
            day: str,
            month: str,
            year: int,
            weekday: str
    ) -> str:
        responses = {
            'Russian': f'📅 Дата: {day}'
                       f' {data.gr_months_index[month]}'
                       f' {year} годa,'
                       f' {data.hdays_of_7[weekday]}',
            'English': f'📅 Date: {day}'
                       f' {data.gr_months_index_en[month]}'
                       f' {year},'
                       f' {data.hdays_of_7_en[weekday]}',
            'Hebrew': f'📅 תאריך: '
                      f'{day} {data.gr_months_index_he[month]}'
                      f' {year},'
                      f' {data.hdays_of_7_he[weekday]}'
        }
        holiday_number = responses.get(lang, '')
        return holiday_number

    # Для поста 9 ава
    @staticmethod
    def tisha_av_fast(
            lang: str,
            day_begin: str,
            month_begin: str,
            time_begin: str,
            chatzot: str,
            day_end: str,
            month_end: str,
            time_end: str,
            ben_ashmashot: str,
            nevareshet: str,
            shmirat_shabat: str
    ) -> str:
        responses = {
            'Russian': f'Начало поста {day_begin}'
                       f' {data.gr_months_index[month_begin]}:'
                       f' *{time_begin[:-3:]}*\nХацот: *{chatzot[:-3:]}*\n'
                       f'Конец поста {day_end}'
                       f' {data.gr_months_index[month_end]}\n'
                       f'✨ Выход звезд:'
                       f' *{time_end[:-3:]}*\n'
                       f'🕖 Сефер бен Ашмашот: *{ben_ashmashot[:-3:]}*\n'
                       f'🕘 Неварешет: *{nevareshet[:-3:]}*\n'
                       f'🕑 Шмират шаббат килхата: *{shmirat_shabat[:-3:]}*',
            'English': f'Fast begins {day_begin}'
                       f' {data.gr_months_index_en[month_begin]}:'
                       f' *{time_begin[:-3:]}*\nChatzot: *{chatzot[:-3:]}*\n'
                       f'The fast ends {day_end}'
                       f' {data.gr_months_index_en[month_end]}\n'
                       f'✨ Tzeit akohavim:'
                       f' *{time_end[:-3:]}*\n'
                       f'🕖 Sefer ben Ashmashot: *{ben_ashmashot[:-3:]}*\n'
                       f'🕘 Nevareshet: *{nevareshet[:-3:]}*\n'
                       f'🕑 Shmirat shabbat kelhata: *{shmirat_shabat[:-3:]}*',
        'Hebrew': f'{day_begin} תחילת הצום'
                  f' {data.gr_months_index_en[month_begin]}:'
                       f' *{time_begin[:-3:]}*:חצות\n*{chatzot[:-3:]}*\n'
                       f'יציאת הצום {day_end}'
                       f' {data.gr_months_index_en[month_end]}\n'
                       f' :צאת הכוכבים ✨'
                       f' *{time_end[:-3:]}*\n'
                       f'\n*{ben_ashmashot[:-3:]}* :ספר בין השמשות 🕖'
                       f'\n*{nevareshet[:-3:]}* :נברשת 🕘'
                       f'*{shmirat_shabat[:-3:]}* :שמירת שבת כהלכתה 🕑'
        }
        holiday_number = responses.get(lang, '')
        return holiday_number


# ЛОКАЛИЗАЦИЯ ДЛЯ КОНВЕРТЕРА
class Converter(object):

    @staticmethod
    def welcome_to_converter(lang: str) -> str:
        responses = {
            'Russian': 'Здесь вы можете сконвертировать даты из '
                       'григорианского календаря в еврейский и обратно, а '
                       'также получить зманим на сконвертированную дату.\n'
                       'Выберите подходящий вам вариант:',
            'English': 'W',  # TODO перевод
            'Hebrew': ''  # TODO перевод
        }
        response = responses.get(lang, '')
        return response

    # запрос даты для григ конвертера
    @staticmethod
    def request_date_for_converter_greg(lang: str) -> str:
        responses = {
            'Russian': 'Пожалуйста, введите дату грегорианского календаря, '
                       'которую вы хотите сконвертировать '
                       '*в формате ДД.ММ.ГГГГ*',
            'English': 'Please enter the gregorian date to convert '
                       'for your selection *in the format DD.MM.YYYY*',
            'Hebrew': ''  # TODO перевод
        }
        response = responses.get(lang, '')
        return response

    # запрос даты для евр конвертера
    @staticmethod
    def request_date_for_converter_heb(lang: str) -> str:
        responses = {
            'Russian': 'Пожалуйста, введите дату еврейского календаря, '
                       'которую вы хотите сконвертировать '
                       '*в формате ДД месяц ГГГГ* (например: `4 ияр 5778)`\n\n'
                       '_Обратите внимание на правильные названия '
                       'еврейских месяцев!_\nнисан, ияр, сиван, тамуз, ав, '
                       'элуль, тишрей, хешван, кислев, тевет, шват, адар, '
                       'адар 1, адар 2',
            'English': 'Please enter the hebrew date to convert '
                       'for your selection *in the format DD month YYYY* '
                       '(For example: `4 iyar 5778`)\n\n'
                       '_Pay attention to the correct names of hebrew '
                       'months!_\nnisan, iyar, sivan, tamuz, av, elul, '
                       'tishrei, cheshvan, kislev, tevet, shevat, adar, adar 1'
                       ', adar 2',
            'Hebrew': ''  # TODO перевод
        }
        response = responses.get(lang, '')
        return response

    # конвертирование грегорианской даты
    @staticmethod
    def convert_greg_to_heb(
            greg_date: tuple,
            day_of_week: int,
            heb_date: tuple,
            lang: str
    ) -> str:
        responses = {
            'Russian': f'Грегорианская дата: *{greg_date[2]} '
                       f'{data.gr_months_index[greg_date[1]]} '
                       f'{greg_date[0]}* года, {data.days_ru[day_of_week]}\n'
                       f'Еврейская дата: *{heb_date[2]} '
                       f'{data.jewish_months_a[heb_date[1]]} {heb_date[0]}*',
            'English': f'Gregorian date: *{greg_date[2]} '
                       f'{data.gr_months_index_en[greg_date[1]]} '
                       f'{greg_date[0]}*, {data.days_en[day_of_week]}\n'
                       f'Hebrew date: *{heb_date[2]} '
                       f'{heb_date[1]} {heb_date[0]}*',
            'Hebrew': f''  # TODO перевод
        }
        response = responses.get(lang, '')
        return response

    # конвертирование еврейской даты
    @staticmethod
    def convert_heb_to_greg(
            heb_date: tuple,
            day_of_week: int,
            greg_date: tuple,
            lang: str
    ) -> str:
        responses = {
            'Russian': f'Еврейская дата: *{heb_date[2]} '
                       f'{data.heb_months_codes_ru[heb_date[1]]} '
                       f'{heb_date[0]}*\nГрегорианская дата: *{greg_date[2]} '
                       f'{data.gr_months_index[greg_date[1]]} '
                       f'{greg_date[0]}* года, {data.days_ru[day_of_week]}',
            'English': f'Hebrew date: *{heb_date[2]} '
                       f'{data.heb_months_codes_en[heb_date[1]]} '
                       f'{heb_date[0]}*\nGregorian date: *{greg_date[2]} '
                       f'{data.gr_months_index_en[greg_date[1]]} '
                       f'{greg_date[0]}*, {data.days_en[day_of_week]}',
            'Hebrew': f''  # TODO перевод
        }
        response = responses.get(lang, '')
        return response

    # выдать название месяца
    @staticmethod
    def get_month_name(lang:str, name:str) -> str:
        responses = {
            'Russian': data.heb_months_names_ru[name],
            'English': data.heb_months_names_en[name],
            'Hebrew': data.heb_months_names_he[name]
        }
        response = responses.get(lang, '')
        return response

    # некорректная дата
    @staticmethod
    def incorrect_heb_date_format(lang: str) -> str:
        responses = {
            'Russian': 'Вы ввели некорректную дату. \nПожалуйста, введите '
                       'дату в *формате ДД месяц ГГГГ*\n\n'
                       '_Обратите внимание на правильные названия '
                       'еврейских месяцев!_\nнисан, ияр, сиван, таммуз, ав, '
                       'элуль, тишрей, хешван, кислев, тевет, шват, адар, '
                       'адар 1, адар 2',
            'English': 'Incorrect date. \nPlease input date *in '
                       'the format DD month YYYY*_pay attention to the '
                       'correct names of hebrew months!_\nnisan, iyar, sivan, '
                       'tammuz, av, elul, tishrei, cheshvan, kislev, tevet, '
                       'shevat, adar, adar 1, adar 2',
            'Hebrew': ''  # TODO перевод
        }
        response = responses.get(lang, '')
        return response

    # сообщение об ошибке в дате
    @staticmethod
    def incorrect_heb_date_value(lang: str) -> str:
        responses = {
            'Russian': 'Введенная дата не существует! \nПожалуйста, введите '
                       'дату в *формате ДД месяц ГГГГ*\n\n'
                       '_Обратите внимание на правильные названия '
                       'еврейских месяцев!_\nнисан, ияр, сиван, таммуз, ав, '
                       'элуль, тишрей, хешван, кислев, тевет, шват, адар, '
                       'адар 1, адар 2',
            'English': 'The date that you entered doesn\'t exist. \n'
                       'Please input date *in the format DD month YYYY*\n'
                       '_pay attention to the correct names of hebrew '
                       'months!_\nnisan, iyar, sivan, tammuz, av, elul, '
                       'tishrei, cheshvan, kislev, tevet, shevat, adar, '
                       'adar 1, adar 2',
            'Hebrew': ''  # TODO перевод
        }
        response = responses.get(lang, '')
        return response

# -*- coding: utf-8 -*-
import data


# ЛОКАЛИЗАЦИЯ ДЛЯ ДАФ ЙОМИ
class DafYomi(object):

    @staticmethod
    def get_str(lang: str, masechta: str, daf: str) -> str:
        daf_str = ''
        if lang == 'Russian':
            daf_str = f'*Даф Йоми*\n\n📗 *Трактат:* {data.talmud[masechta]} ' \
                      f'\n📄 *Лист:* {daf}'
        elif lang == 'English':
            daf_str = f'*Daf Yomi*\n\n📗 *Masechta:* {masechta}\n ' \
                      f'📄 *Daf:* {daf}'
        return daf_str


# ЛОКАЛИЗАЦИЯ ДЛЯ РОШ ХОДЕША
class RoshHodesh(object):

    # если два дня РХ в разных годах
    @staticmethod
    def two_days_in_different_years(
            lang: str,
            first_year: int,
            second_year: int
    ) -> str:
        rh_days = ''
        if lang == 'Russian':
            rh_days = f'31 декабря {first_year} года и 1 ' \
                      f'января {second_year} года'
        elif lang == 'English':
            rh_days = f'31 December {first_year} and 1 ' \
                      f'January {second_year}'
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
        rh_days = ''
        if lang == 'Russian':
            rh_days = f'{first_day} и 1 {data.gr_months_index[first_month]} ' \
                      f'и {data.gr_months_index[second_month]} {year} года'
        elif lang == 'English':
            rh_days = f'{first_day} and 1 ' \
                      f'{data.gr_months_index_en[first_month]}' \
                      f' and {data.gr_months_index_en[second_month]} {year}'
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
        rh_days = ''
        if lang == 'Russian':
            rh_days = f'{first_day} и {second_day} ' \
                      f'{data.gr_months_index[month]} {year} года'
        elif lang == 'English':
            rh_days = f'{first_day} and {second_day} ' \
                      f'{data.gr_months_index_en[month]} {year}'
        return rh_days

    # если в РХ 1 день выпадает на 1 января
    @staticmethod
    def one_day_first_day_of_jan(lang: str, year: int) -> str:
        rh_days = ''
        if lang == 'Russian':
            rh_days = f'1 января {year} года'
        elif lang == 'English':
            rh_days = f'1 January {year}'
        return rh_days

    # если в РХ 1 день выпадает на начало месяца
    @staticmethod
    def one_day_first_day_of_month(
            lang: str,
            month: int,
            year: int
    ) -> str:
        rh_days = ''
        if lang == 'Russian':
            rh_days = f'1 {data.gr_months_index[month]} {year} года'
        elif lang == 'English':
            rh_days = f'1 {data.gr_months_index_en[month]} {year}'
        return rh_days

    # если в РХ 1 день
    @staticmethod
    def one_day(
            lang: str,
            day: int,
            month: int,
            year: int
    ) -> str:
        rh_days = ''
        if lang == 'Russian':
            rh_days = f'{day} {data.gr_months_index[month]} {year} года'
        elif lang == 'English':
            rh_days = f'{day} {data.gr_months_index_en[month]} {year}'
        return rh_days

    # определяем день недели
    @staticmethod
    def get_rh_day_of_week(
            lang: str,
            first_day: int,
            second_day=None
    ) -> str:
        day_of_week = ''
        if second_day:
            if lang == 'Russian':
                day_of_week = f'{data.days_ru[first_day]}-' \
                              f'{data.days_ru[second_day]}'
            elif lang == 'English':
                day_of_week = f'{data.days_en[first_day]}-' \
                              f'{data.days_en[second_day]}'
        elif not second_day:
            if lang == 'Russian':
                day_of_week = f'{data.days_ru[first_day]}'
            elif lang == 'English':
                day_of_week = f'{data.days_en[first_day]}'
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
            # minutes: str,
            nchalakim: int,
            chalakim: str
    ) -> str:
        molad_str = ''
        if lang == 'Russian':
            molad_str = f'{day} {data.gr_months[month]}, ' \
                        f'{data.gr_dayofweek[day_of_week]}, ' \
                        f'{nhours} {data.hours.get(hours[-1:], "часов")} ' \
                        f'{nminutes} ' \
                        f'{data.minutes.get(nminutes, "минут")} и ' \
                        f'{nchalakim} {data.chalakim.get(chalakim, "частей")}'
        elif lang == 'English':
            molad_str = f'{day} {month}, {day_of_week}, ' \
                        f'{nhours} {data.hours_e.get(hours, "hours")} ' \
                        f'{nminutes} ' \
                        f'{data.minutes_e.get(nminutes, "minutes")} and ' \
                        f'{nchalakim} ' \
                        f'{data.chalakim_e.get(chalakim, "chalakim")}'
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
        rh = ''
        if lang == 'Russian':
            rh = f'*Рош ходеш* 🌒\n\n' \
                 f'*Месяц:* {data.jewish_months[month]}\n' \
                 f'*Продолжительность Рош Ходеша:* {length}' \
                 f' {data.length_r[f"{length}"]}\n' \
                 f'*Рош Ходеш:* {rosh_hodesh}\n*Молад:* {molad}'
        elif lang == 'English':
            rh = f'*Rosh Chodesh* 🌒\n\n*Month:* {month}\n' \
                 f'*Rosh Chodesh duration:* {length}' \
                 f' {data.length_e[f"{length}"]}\n' \
                 f'*Rosh Chodesh:* {rosh_hodesh}\n*Molad:* {molad}'
        return rh


# ЛОКАЛИЗАЦИЯ ДЛЯ ШАББАТА
class Shabos(object):

    # для шаббатов, в которых невозможно вычислить зманим
    @staticmethod
    def shabos_with_latitude_error(lang: str, parasha: str) -> str:
        shabos_str = ''
        if lang == 'Russian':
            shabos_str = f'*Шаббат*\n\n📜 *Недельная глава:* ' \
                         f'{data.parashat[parasha]}\n\n' \
                         f'В данных широтах невозможно определить ' \
                         f'зманим из-за полярного дня/полярной ночи.'
        elif lang == 'English':
            shabos_str = f'*Shabbos*\n\n📜 *Parshat hashavua:* {parasha}\n\n' \
                         f'In these latitudes zmanim is impossible' \
                         f' to determine because of polar night/day.'
        return shabos_str

    # для шаббатов в северных широтах с предупреждением о раннем зажигании
    @staticmethod
    def shabos_with_warning(
            lang: str,
            parasha: str,
            cl: str,
            th: str
    ) -> str:
        shabos_str = ''
        if lang == 'Russian':
            shabos_str = f'*Шаббат*\n\n📜 *Недельная глава:* ' \
                         f'{data.parashat[parasha]}\n' \
                         f'🕯 *Зажигание свечей:* {cl}\n' \
                         f'✨ *Выход звёзд:* {th}\n\n' \
                         f'*Внимание!* Необходимо уточнить' \
                         f' время зажигания свечей у раввина общины!'
        elif lang == 'English':
            shabos_str = f'*Shabbos*\n\n📜 *Parshat hashavua:* {parasha}\n' \
                         f'🕯 *Candle lighting:* {cl}\n' \
                         f'✨ *Tzeit hakochavim:* {th}\n\n' \
                         f'*Notice!* You should specify time of candle' \
                         f' lighting with the rabbi of your community.'
        return shabos_str

    # для обычных шаббатов
    @staticmethod
    def shabos(
            lang: str,
            parasha: str,
            cl: str,
            th: str
    ) -> str:
        shabos_str = ''
        if lang == 'Russian':
            shabos_str = f'*Шаббат*\n\n📜 *Недельная глава:* ' \
                         f'{data.parashat[parasha]}\n' \
                         f'🕯 *Зажигание свечей:* {cl}\n' \
                         f'✨ *Выход звёзд:* {th}'
        elif lang == 'English':
            if parasha == 'PESACH_VIII':
                parasha = 'PESACH'
            shabos_str = f'*Shabbos*\n\n📜 *Parshat hashavua:* {parasha}\n' \
                         f'🕯 *Candle lighting:* {cl}\n' \
                         f'✨ *Tzeit hakochavim:* {th}'
        return shabos_str

    # для шаббатов в израиле
    @staticmethod
    def shabos_in_israel(
            lang: str,
            parasha: str,
            cl_eighteen: str,
            cl_thirty: str,
            cl_forty: str,
            th: str
    ):
        shabos_str = ''
        if lang == 'Russian':
            shabos_str = f'*Шаббат*\n\n📜 *Недельная глава:* ' \
                         f'{data.parashat[parasha]}\n' \
                         f'🕯 *Зажигание свечей:*\n' \
                         f'*18* минут до шкии: {cl_eighteen}\n' \
                         f'*30* минут до шкии: {cl_thirty}\n' \
                         f'*40* минут до шкии: {cl_forty}\n\n' \
                         f'✨ *Выход звёзд:* {th}'
        elif lang == 'English':
            shabos_str = f'*Shabbos*\n\n📜 *Parshat hashavua:* {parasha}\n' \
                         f'🕯 *Candle lighting:*\n' \
                         f'*18* minutes before sunset: {cl_eighteen}\n' \
                         f'*30* minutes before sunset: {cl_thirty}\n' \
                         f'*40* minutes before sunset: {cl_forty}\n\n' \
                         f'✨ *Tzeit hakochavim:* {th}'
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
        error_message = ''
        if lang == 'Russian':
            error_message = 'В данных широтах невозможно определить ' \
                            'зманим из-за полярного дня/полярной ночи.'
        elif lang == 'English':
            error_message = 'In these latitudes it is impossible to determine'\
                            ' because of polar night/day.'
        return error_message

    # названия зманим для настроек
    @staticmethod
    def get_zman_name(zman: str, lang: str) -> str:
        zman_name = ''
        if lang == 'Russian':
            zman_name = data.zmanim_ru[zman]
        elif lang == 'English':
            zman_name = ''
        return zman_name


# ЛОКАЛИЗАЦИЯ ДЛЯ ВСПОМОГАТЕЛЬНЫХ ФУНКЦИЙ
class Utils(object):
    # координаты получены
    @staticmethod
    def location_received(lang: str) -> str:
        response = ''
        if lang == 'Russian':
            response = 'Координаты получены, теперь вы можете ' \
                       'начать работать с ботом.'
        elif lang == 'English':
            response = 'Location has been received, now you can start ' \
                       'working with the bot'
        return response

    # ошибка определения тз
    @staticmethod
    def failed_check_tz(lang: str) -> str:
        response = ''
        if lang == 'Russian':
            response = 'Не получилось определить часовой пояс. Возможно ' \
                       'вы находитесь далеко от берега или указали ' \
                       'неверные координаты. Попробуйте отправить свое' \
                       ' местоположение еще раз'
        elif lang == 'English':
            response = 'Time zone could not be determined. Рrobably, you' \
                       ' аre far from сoast or indicate incorrect ' \
                       'coordinates. Try to send your location again.'
        return response

    # некорректный текст
    @staticmethod
    def incorrect_text(lang: str) -> str:
        responses = {
            'Russian': 'Некорректная команда. Пожалуйста, выберите один из '
                       'вариантов на кнопках.',
            'English': 'Incorrect command. Please, choose one of the options '
                       'on the buttons'
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
                       '"_55.5, 37.7_", or forward message with location here.'
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
                       'had been read F.A.Q. available by "F.A.Q." button'
        }
        response = responses.get(lang, '')
        return response

    # запрос даты для зманим
    @staticmethod
    def request_date_for_zmanim(lang: str) -> str:
        responses = {
            'Russian': 'Пожалуйста, введите дату, на которую вы '
                       'хотите получить _зманим_ *в формате ДД.ММ.ГГГГ*',
            'English': 'Please enter the date to calculate the _Zmanim_  '
                       'for your selection *in the format DD.MM.YYYY*'
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
                       '*в формате ДД.ММ.ГГГГ*\n_Первый месяц — Нисан!_',
            'English': 'Please enter the hebrew date to convert '
                       'for your selection *in the format DD.MM.YYYY*\n'
                       '_First month is Nissan!_',
            'Hebrew': ''  # TODO перевод
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
                       'the format DD.MM.YYYY*'
        }
        response = responses.get(lang, '')
        return response

    @staticmethod
    def incorrect_date_value(lang: str) -> str:
        responses = {
            'Russian': 'Введенная дата не существует. \nПожалуйста, введите '
                       'корректную дату в *формате ДД.ММ.ГГГГ*',
            'English': 'The date that you entered doesn\'t exist, '
                       'please enter the correct date in format DD.MM.YYYY'
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

# ЛОКАЛИЗАЦИЯ ДЛЯ ПРАЗДНИКОВ
class Holidays(object):

    # Когда невозможно определить времена
    @staticmethod
    def polar_area(lang: str) -> str:
        ra_time = ''
        if lang == 'Russian':
            ra_time = '\nВ данных широтах невозможно определить' \
                         ' зманим из-за полярного дня/полярной ночи'
        elif lang == 'English':
            ra_time = '\nIn these latitudes zmanim is impossible' \
                        ' to determine because of polar night/day'

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
        lighting_time = ''
        if lang == 'Russian':
            lighting_time = '🕯 Зажигание свечей {}' \
                             ' {}:' \
                             ' *{:.5s}*\n' \
                             '✨ Авдала {}' \
                             ' {}:' \
                             ' *{:.5s}*'\
                             .format(light_day,
                                     data.gr_months_index[light_month],
                                     light_time, avdala_day,
                                     data.gr_months_index[avdala_month],
                                     avdala_time)
        elif lang == 'English':
            lighting_time = '🕯 Candle lighting {}' \
                             ' {}:' \
                             ' *{:.5s}*\n' \
                             '✨ Avdala {}' \
                             ' {}:' \
                             ' *{:.5s}*' \
                             .format(light_day,
                                     data.gr_months_index_en[light_month],
                                     light_time, avdala_day,
                                     data.gr_months_index_en[avdala_month],
                                     avdala_time)

        return lighting_time
    
    # Когда один день праздника и перед ним шаббат
    @staticmethod
    def shabbat_before_holiday_israel(
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
        lighting_time = ''
        if lang == 'Russian':
            lighting_time = '🕯 Зажигание свечей (Шаббат) {}' \
                            ' {}:' \
                            ' *{:.5s}*\n' \
                            '✨🕯 Авдала и зажигание свечей {}' \
                            ' {}:' \
                            ' *{:.5s}*\n' \
                            '✨ Авдала {}' \
                            ' {}:' \
                            ' *{:.5s}*' \
                .format(light_shab_day,
                        data.gr_months_index[light_shab_month],
                        light_shab_time,
                        light_day,
                        data.gr_months_index[light_month],
                        light_time, avdala_day,
                        data.gr_months_index[avdala_month],
                        avdala_time)
        elif lang == 'English':
            lighting_time = '🕯 Candle lighting (Shabbat) {}' \
                            ' {}:' \
                            ' *{:.5s}*\n' \
                            '✨🕯 Avdala and candle lighting {}' \
                            ' {}:' \
                            ' *{:.5s}*\n' \
                            '✨ Avdala {}' \
                            ' {}:' \
                            ' *{:.5s}*' \
                .format(light_shab_day,
                        data.gr_months_index_en[light_shab_month],
                        light_shab_time,
                        light_day,
                        data.gr_months_index_en[light_month],
                        light_time, avdala_day,
                        data.gr_months_index_en[avdala_month],
                        avdala_time)

        return lighting_time
    
    # Для Йом-Кипура
    @staticmethod
    def lighting_fast(
            lang: str,
            light_day: str,
            light_month: str,
            light_time: str,
            avdala_day: str,
            avdala_month: str,
            avdala_time: str
    ) -> str:
        fast_time = ''
        if lang == 'Russian':
            fast_time = '🕯 Зажигание свечей и начало поста {}' \
                        ' {}:' \
                        ' *{:.5s}*\n' \
                        '✨ Авдала и конец поста {}' \
                        ' {}:' \
                        ' *{:.5s}*' \
                .format(light_day, data.gr_months_index[light_month],
                        light_time, avdala_day,
                        data.gr_months_index[avdala_month], avdala_time)
        elif lang == 'English':
            fast_time = '🕯 Candle lighting and the fast begins {}' \
                        ' {}:' \
                        ' *{:.5s}*\n' \
                        '✨ Avdala and the fast ends {}' \
                        ' {}:' \
                        ' *{:.5s}*' \
                .format(light_day, data.gr_months_index_en[light_month],
                        light_time, avdala_day,
                        data.gr_months_index_en[avdala_month], avdala_time)

        return fast_time

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
        ra_time = ''
        if lang == 'Russian':
            ra_time = '🕯 Зажигание свечей {}' \
                      ' {}:' \
                      ' *{:.5s}*\n' \
                      '🕯 Зажигание свечей (Шаббат) {} {}: *{:.5s}*\n' \
                      '✨ Авдала {}' \
                      ' {}:' \
                      ' *{:.5s}*' \
                .format(light_day, data.gr_months_index[light_month],
                        light_time, light_shab_day,
                        data.gr_months_index[light_shab_month],
                        light_shab_time, avdala_day,
                        data.gr_months_index[avdala_month],
                        avdala_time)
        elif lang == 'English':
            ra_time = '🕯 Candle lighting {}' \
                      ' {}:' \
                      ' *{:.5s}*\n' \
                      '🕯 Candle lighting (Shabbat) {} {}: *{:.5s}*\n' \
                      '✨ Avdala {}' \
                      ' {}:' \
                      ' *{:.5s}*' \
                .format(light_day, data.gr_months_index_en[light_month],
                        light_time, light_shab_day,
                        data.gr_months_index_en[light_shab_month],
                        light_shab_time, avdala_day,
                        data.gr_months_index_en[avdala_month],
                        avdala_time)

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
        ra_time = ''
        if lang == 'Russian':
            ra_time = '🕯 Зажигание свечей (Шаббат) {}' \
                      ' {}:' \
                      ' *{:.5s}*\n' \
                      '✨🕯 Авдала и зажигание свечей {}' \
                      ' {}:' \
                      ' *{:.5s}*\n' \
                      '🕯 Зажигание свечей {}' \
                      ' {}:' \
                      ' *{:.5s}*\n' \
                      '✨ Авдала {}' \
                      ' {}:' \
                      ' *{:.5s}*' \
                .format(light_shab_day, data.gr_months_index[light_shab_month],
                        light_shab_time, light_1_day,
                        data.gr_months_index[light_1_month],
                        light_1_time, light_2_day,
                        data.gr_months_index[light_2_month],
                        light_2_time, avdala_day,
                        data.gr_months_index[avdala_month], avdala_time)
        elif lang == 'English':
            ra_time = '🕯 Candle lighting (Shabbat) {}' \
                      ' {}:' \
                      ' *{:.5s}*\n' \
                      '✨🕯 Avdala and candle lighting {}' \
                      ' {}:' \
                      ' *{:.5s}*\n' \
                      '🕯 Candle lighting {}' \
                      ' {}: ' \
                      '*{:.5s}*\n' \
                      '✨ Avdala {}' \
                      ' {}:' \
                      ' *{:.5s}*' \
                .format(light_shab_day,
                        data.gr_months_index_en[light_shab_month],
                        light_shab_time,
                        light_1_day, data.gr_months_index_en[light_1_month],
                        light_1_time, light_2_day,
                        data.gr_months_index_en[light_2_month], light_2_time,
                        avdala_day,
                        data.gr_months_index_en[avdala_month], avdala_time)

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
        ra_time = ''
        if lang == 'Russian':
            ra_time = '🕯 Зажигание свечей {}' \
                      ' {}:' \
                      ' *{:.5s}*\n' \
                      '🕯 Зажигание свечей {}' \
                      ' {}:' \
                      ' *{:.5s}*\n' \
                      '✨ Авдала {}' \
                      ' {}:' \
                      ' *{:.5s}*' \
                .format(light_1_day, data.gr_months_index[light_1_month],
                        light_1_time, light_2_day,
                        data.gr_months_index[light_2_month],
                        light_2_time, avdala_day,
                        data.gr_months_index[avdala_month], avdala_time)
        elif lang == 'English':
            ra_time = '🕯 Candle lighting {}' \
                      ' {}:' \
                      ' *{:.5s}*\n' \
                      '🕯 Candle lighting {}' \
                      ' {}:' \
                      ' *{:.5s}*\n' \
                      '✨ Avdala {}' \
                      ' {}:' \
                      ' *{:.5s}*' \
                .format(light_1_day, data.gr_months_index_en[light_1_month],
                        light_1_time, light_2_day,
                        data.gr_months_index_en[light_2_month],
                        light_2_time, avdala_day,
                        data.gr_months_index_en[avdala_month], avdala_time)

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
        ra_time = ''
        if lang == 'Russian':
            ra_time = '🕯 Зажигание свечей {}' \
                      ' {}:' \
                      ' *{:.5s}*\n' \
                      '🕯 Зажигание свечей {}' \
                      ' {}:' \
                      ' *{:.5s}*\n' \
                      '🕯 Зажигание свечей (Шаббат) {}' \
                      ' {}:' \
                      ' *{:.5s}*\n' \
                      '✨ Авдала {}' \
                      ' {}:' \
                      ' *{:.5s}*' \
                .format(light_1_day, data.gr_months_index[light_1_month],
                        light_1_time, light_2_day,
                        data.gr_months_index[light_2_month], light_2_time,
                        light_shab_day, data.gr_months_index[light_shab_month],
                        light_shab_time, avdala_day,
                        data.gr_months_index[avdala_month], avdala_time)
        elif lang == 'English':
            ra_time = '🕯 Candle lighting {}' \
                      ' {}:' \
                      ' *{:.5s}*\n' \
                      '🕯 Candle lighting {}' \
                      ' {}:' \
                      ' *{:.5s}*\n' \
                      '🕯 Candle lighting (Shabbat) {}' \
                      ' {}: ' \
                      '*{:.5s}*\n' \
                      '✨ Avdala {}' \
                      ' {}:' \
                      ' *{:.5s}*' \
                .format(light_1_day, data.gr_months_index_en[light_1_month],
                        light_1_time, light_2_day,
                        data.gr_months_index_en[light_2_month], light_2_time,
                        light_shab_day,
                        data.gr_months_index_en[light_shab_month],
                        light_shab_time, avdala_day,
                        data.gr_months_index_en[avdala_month], avdala_time)

        return ra_time

    # Длинные праздники (Пейсах, Ханука; Суккот не входит),
    # даты которых приходят на 1 григорианский месяц
    @staticmethod
    def long_holiday(
            lang: str,
            day_start: str,
            day_end: str,
            month: str,
            year: int,
            weekday_start: str,
            weekday_end: str
    ) -> str:
        holiday_number = ''
        if lang == 'Russian':
            holiday_number = f'📅 Дата: {day_start}-' \
                             f'{day_end}' \
                             f' {data.holi_month[month]}' \
                             f' {year} годa,' \
                             f' {data.hdays_of_7[weekday_start]}-' \
                             f'{data.hdays_of_7[weekday_end]}'
        elif lang == 'English':
            holiday_number = f'📅 Date: {day_start}-' \
                             f'{day_end}' \
                             f' {data.holi_month_en[month]}' \
                             f' {year}, ' \
                             f'{data.hdays_of_7_en[weekday_start]}-' \
                             f'{data.hdays_of_7_en[weekday_end]}'

        return holiday_number

    # Двухдневные праздники, даты которых приходят на 1 григорианский месяц
    @staticmethod
    def long_holiday_and(
            lang: str,
            day_start: str,
            day_end: str,
            month: str,
            year: int,
            weekday_start: str,
            weekday_end: str
    ) -> str:
        holiday_number = ''
        if lang == 'Russian':
            holiday_number = f'📅 Дата: {day_start} и ' \
                             f'{day_end}' \
                             f' {data.holi_month[month]}' \
                             f' {year} годa,' \
                             f' {data.hdays_of_7[weekday_start]}-' \
                             f'{data.hdays_of_7[weekday_end]}'
        elif lang == 'English':
            holiday_number = f'📅 Date: {day_start} and ' \
                             f'{day_end}' \
                             f' {data.holi_month_en[month]}' \
                             f' {year}, ' \
                             f'{data.hdays_of_7_en[weekday_start]}-' \
                             f'{data.hdays_of_7_en[weekday_end]}'

        return holiday_number

    # Длинные праздники, даты которых приходят на 2 григорианских месяца
    @staticmethod
    def long_holiday_jump(
            lang: str,
            day_start: str,
            month_start: str,
            day_end: str,
            month_end: str,
            year: int,
            weekday_start: str,
            weekday_end: str
    ) -> str:
        holiday_number = ''
        if lang == 'Russian':
            holiday_number = f'📅 Дата: {day_start}' \
                             f' {data.holi_month[month_start]} - ' \
                             f'{day_end}' \
                             f' {data.holi_month[month_end]}' \
                             f' {year} годa,' \
                             f' {data.hdays_of_7[weekday_start]}-' \
                             f'{data.hdays_of_7[weekday_end]}'
        elif lang == 'English':
            holiday_number = f'📅 Date: {day_start}' \
                             f' {data.holi_month_en[month_start]} - ' \
                             f'{day_end}' \
                             f' {data.holi_month_en[month_end]}' \
                             f' {year}, ' \
                             f'{data.hdays_of_7_en[weekday_start]}-' \
                             f'{data.hdays_of_7_en[weekday_end]}'

        return holiday_number

    # Двухдневные праздники, даты которых приходят на 2 григорианских месяца
    @staticmethod
    def long_holiday_jump_and(
            lang: str,
            day_start: str,
            month_start: str,
            day_end: str,
            month_end: str,
            year: int,
            weekday_start: str,
            weekday_end: str
    ) -> str:
        holiday_number = ''
        if lang == 'Russian':
            holiday_number = f'📅 Дата: {day_start}' \
                             f' {data.holi_month[month_start]} и ' \
                             f'{day_end}' \
                             f' {data.holi_month[month_end]}' \
                             f' {year} годa,' \
                             f' {data.hdays_of_7[weekday_start]}-' \
                             f'{data.hdays_of_7[weekday_end]}'
        elif lang == 'English':
            holiday_number = f'📅 Date: {day_start}' \
                             f' {data.holi_month_en[month_start]} and ' \
                             f'{day_end}' \
                             f' {data.holi_month_en[month_end]}' \
                             f' {year}, ' \
                             f'{data.hdays_of_7_en[weekday_start]}-' \
                             f'{data.hdays_of_7_en[weekday_end]}'

        return holiday_number

    # Однодневные праздники
    @staticmethod
    def short_holiday(
            lang: str,
            day: str,
            month: str,
            year: int,
            weekday: str
    ) -> str:
        holiday_number = ''
        if lang == 'Russian':
            holiday_number = f'📅 Дата: {day}' \
                             f' {data.holi_month[month]}' \
                             f' {year} годa,' \
                             f' {data.hdays_of_7[weekday]}'
        elif lang == 'English':
            holiday_number = f'📅 Date: {day}' \
                             f' {data.holi_month_en[month]}' \
                             f' {year},' \
                             f' {data.hdays_of_7_en[weekday]}'

        return holiday_number


class Converter(object):

    # конвертирование грегорианской даты
    @staticmethod
    def convert_greg_to_heb(
            greg_date: tuple,
            day_of_week: int,
            heb_date: tuple,
            lang: str
    ) -> str:
        response = ''
        if lang == 'Russian':
            response = f'Грегорианская дата: *{greg_date[2]} ' \
                       f'{data.gr_months_index[greg_date[1]]} ' \
                       f'{greg_date[0]}* года, {data.days_ru[day_of_week]}\n' \
                       f'Еврейская дата: *{heb_date[2]} ' \
                       f'{data.jewish_months_a[heb_date[1]]} {heb_date[0]}*'
        elif lang == 'English':
            response = f'Gregorian date: *{greg_date[2]} ' \
                       f'{data.greg_months_en[greg_date[1]]} ' \
                       f'{greg_date[0]}*, {data.days_en[day_of_week]}\n' \
                       f'Hebrew date: *{heb_date[2]} ' \
                       f'{heb_date[1]} {heb_date[0]}*'
        elif lang == 'Hebrew':
            response = f''  # TODO перевод
        return response

    # конвертирование еврейской даты
    @staticmethod
    def convert_heb_to_greg(
            heb_date: tuple,
            day_of_week: int,
            greg_date: tuple,
            lang: str
    ) -> str:
        response = ''
        if lang == 'Russian':
            response = f'Еврейская дата: *{heb_date[2]} ' \
                       f'{data.heb_months_codes_ru[heb_date[1]]} ' \
                       f'{heb_date[0]}*\nГрегорианская дата: *{greg_date[2]} '\
                       f'{data.gr_months_index[greg_date[1]]} ' \
                       f'{greg_date[0]}* года, {data.days_ru[day_of_week]}'

        elif lang == 'English':
            response = f'Hebrew date: *{heb_date[2]} ' \
                       f'{data.heb_months_codes_en[heb_date[1]]} ' \
                       f'{heb_date[0]}*\nGregorian date: *{greg_date[2]} ' \
                       f'{data.greg_months_en[greg_date[1]]} ' \
                       f'{greg_date[0]}*, {data.days_en[day_of_week]}' \

        elif lang == 'Hebrew':
            response = f''  # TODO перевод
        return response

    # выдать название месяца
    @staticmethod
    def get_month_name(lang:str, name:str) -> str:
        response = ''
        if lang == 'Russian':
            response = data.heb_months_names_ru[name]
        elif lang == 'English':
            response = data.heb_months_names_en[name]
        elif lang == 'Hebrew':
            response = data.heb_months_names_he[name]
        return response



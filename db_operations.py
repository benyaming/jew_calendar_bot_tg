import psycopg2
import redis

import localization
import settings

from utils import get_tz_by_location


def check_id_in_db(user):
    with psycopg2.connect(settings.db_parameters_string) as conn:
        cur = conn.cursor()
        query = f'SELECT id FROM public.users WHERE id = {user.id}'
        cur.execute(query)
        status = cur.fetchone()
        if not status:
            if not user.first_name:
                user.first_name = 'NULL'
            if not user.last_name:
                user.last_name = 'NULL'
            query = f'INSERT INTO public.users (id, first_name, last_name)' \
                    f'VALUES (\'{user.id}\', \'{user.first_name}\', ' \
                    f'\'{user.last_name}\')'
            cur.execute(query)
            conn.commit()


def check_location(user, lat, long, bot):
    with psycopg2.connect(settings.db_parameters_string) as conn:
        cur = conn.cursor()
        lang = get_lang_from_redis(user)
        query = f'SELECT latitude, longitude FROM locations ' \
                f'WHERE id = {user}'
        cur.execute(query)
        locations_in_db = cur.fetchone()
        response = ''
        if not locations_in_db:

            tz = get_tz_by_location([lat, long])
            if tz != '':
                query = f'INSERT INTO locations (id, latitude, longitude) ' \
                        f'VALUES (\'{user}\', \'{lat}\', \'{long}\')'
                cur.execute(query)
                conn.commit()
                check_tz(user, tz)
                response = localization.Utils.location_received(lang)
                bot.send_message(user, response)
                response = True
                if tz in ['Asia/Jerusalem', 'Asia/Tel_Aviv', 'Asia/Hebron']:
                    diaspora = False
                else:
                    diaspora = True
                set_diaspora_status(user, diaspora)
            else:
                response = localization.Utils.failed_check_tz(lang)
                bot.send_message(user, response)

        # если координаты в бд отличаются от присланных, обновляем бд
        elif lat != locations_in_db[0] or long != locations_in_db[1]:
            loc = [lat, long]
            tz = get_tz_by_location(loc)
            lang = get_lang_from_redis(user)
            if tz != '':
                check_tz(user, tz)
                query = f'UPDATE locations SET ' \
                        f'latitude = \'{lat}\', longitude = \'{long}\'' \
                        f'WHERE id = {user}'
                if lang == 'Russian':
                    response = 'Координаты обновлены'
                elif lang == 'English':
                    response = 'Location updated'
                cur.execute(query)
                conn.commit()

                bot.send_message(user, response)
                response = True
            else:
                response = localization.Utils.failed_check_tz(lang)
                bot.send_message(user, response)
                response = False
        return response


def get_location_by_id(user_id):
    with psycopg2.connect(settings.db_parameters_string) as conn:
        cur = conn.cursor()
        query = f'SELECT latitude, longitude FROM locations ' \
                f'WHERE id = {user_id}'
        cur.execute(query)
        location = cur.fetchone()
        response = location
        return response


def check_tz(user, tz):
    with psycopg2.connect(settings.db_parameters_string) as conn:
        cur = conn.cursor()
        query = f'SELECT tz FROM public.tz WHERE id = {user}'
        cur.execute(query)
        time_zone = cur.fetchone()
        if not time_zone:
            query = f'INSERT INTO public.tz (id, tz) VALUES ({user}, \'{tz}\')'
            cur.execute(query)
            conn.commit()
        elif time_zone != tz:
            query = f'UPDATE public.tz SET tz = \'{tz}\' WHERE id = {user}'
            cur.execute(query)
            conn.commit()
            # set diaspora
            if tz in ['Asia/Jerusalem', 'Asia/Tel_Aviv', 'Asia/Hebron']:
                diaspora = False
            else:
                diaspora = True
            set_diaspora_status(user, diaspora)


def get_tz_by_id(user_id):
    with psycopg2.connect(settings.db_parameters_string) as conn:
        cur = conn.cursor()
        query = f'SELECT public.tz.tz FROM public.tz WHERE id = {user_id}'
        cur.execute(query)
        tz = cur.fetchone()
        response = tz[0]
        return response


def set_lang(user, lang):
    with psycopg2.connect(settings.db_parameters_string) as conn:
        cur = conn.cursor()
        query = f'SELECT lang FROM lang WHERE id = {user}'
        cur.execute(query)
        lang_in_db = cur.fetchone()
        if not lang_in_db:
            query = f'INSERT INTO lang VALUES ({user}, \'{lang}\')'
            cur.execute(query)
            conn.commit()
            if settings.IS_SERVER:
                r = redis.StrictRedis(
                    host=settings.r_host,
                    port=settings.r_port
                )
                r.set(f'{user}', lang)
                r.expire(f'{user}', 31536000)
        elif lang_in_db[0] != lang:
            query = f'UPDATE lang SET lang = \'{lang}\' WHERE id = {user}'
            cur.execute(query)
            conn.commit()
            if settings.IS_SERVER:
                r = redis.StrictRedis(
                    host=settings.r_host,
                    port=settings.r_port
                )
                r.set(f'{user}', lang)
                r.expire(f'{user}', 31536000)


def get_lang_by_id(user):
    with psycopg2.connect(settings.db_parameters_string) as conn:
        cur = conn.cursor()
        query = f'SELECT lang FROM lang WHERE id = {user}'
        cur.execute(query)
        lang_in_bd = cur.fetchone()
        if lang_in_bd:
            response = lang_in_bd[0]
        else:
            response = None
        return response


def get_lang_from_redis(user):
    if settings.IS_SERVER:
        r = redis.StrictRedis(host=settings.r_host, port=settings.r_port)
        lang_in_redis = r.get(user)
        if not lang_in_redis:
            lang_in_db = get_lang_by_id(user)
            r.set(user, lang_in_db)
            r.expire(user, 31536000)
            response = lang_in_db
        else:
            lang = r.get(user).decode('unicode_escape')
            response = lang
    else:
        response = get_lang_by_id(user)
    return response


def get_candle_offset(user_id: int) -> int:
    with psycopg2.connect(settings.db_parameters_string) as conn:
        cur = conn.cursor()
        query = f'SELECT candle_offset FROM shabos_settings ' \
                f'WHERE user_id = {user_id}'
        cur.execute(query)
        offset = cur.fetchone()
        if offset:
            return offset[0]
        else:
            query = f'INSERT INTO shabos_settings VALUES ({user_id}, DEFAULT)'
            cur.execute(query)
            conn.commit()
            return get_candle_offset(user_id)


def update_candle_offset(user_id: int, new_offset: int) -> bool:
    with psycopg2.connect(settings.db_parameters_string) as conn:
        result = True
        old_offset = get_candle_offset(user_id)
        if new_offset == old_offset:
            result = None
        cur = conn.cursor()
        query = f'UPDATE shabos_settings SET candle_offset = {new_offset} ' \
                f'WHERE user_id = {user_id}'
        cur.execute(query)
        conn.commit()
        return result


def get_zmanim_set(user: int) -> str:
    with psycopg2.connect(settings.db_parameters_string) as conn:
        cur = conn.cursor()
        query = f'SELECT zmanim_set FROM zmanim_settings WHERE ' \
                f'user_id = {user}'
        cur.execute(query)
        zmanim_set = cur.fetchone()
        if not zmanim_set:
            query = f'INSERT INTO zmanim_settings VALUES ({user}, DEFAULT)'
            cur.execute(query)
            conn.commit()
            return get_zmanim_set(user)
        else:
            return zmanim_set[0]


def update_zmanim_set(user: int, zmanim_set: str) -> None:
    with psycopg2.connect(settings.db_parameters_string) as conn:
        cur = conn.cursor()
        query = f'UPDATE zmanim_settings SET zmanim_set = \'{zmanim_set}\' ' \
                f'WHERE user_id = {user}'
        cur.execute(query)
        conn.commit()


def get_diaspora_status(user: int) -> bool:
    with psycopg2.connect(settings.db_parameters_string) as conn:
        cur = conn.cursor()
        query = f'SELECT diaspora_status FROM diaspora_settings WHERE ' \
                f'user_id = {user}'
        cur.execute(query)
        diaspora_status = cur.fetchone()
        if diaspora_status:
            return diaspora_status[0]
        else:
            tz = get_tz_by_id(user)
            if tz in ['Asia/Jerusalem', 'Asia/Tel_Aviv', 'Asia/Hebron']:
                diaspora = False
            else:
                diaspora = True
            set_diaspora_status(user, diaspora)

            return diaspora


def set_diaspora_status(user: int, status) -> None:
    with psycopg2.connect(settings.db_parameters_string) as conn:
        cur = conn.cursor()
        query = f'SELECT diaspora_status FROM diaspora_settings ' \
                f'WHERE user_id = {user}'
        cur.execute(query)
        current_status = cur.fetchone()
        if current_status:
            query = f'UPDATE diaspora_settings ' \
                    f'SET diaspora_status = {status} ' \
                    f'WHERE user_id = {user}'
        else:
            query = f'INSERT INTO diaspora_settings ' \
                    f'VALUES ({user}, \'{status}\')'
        cur.execute(query)
        conn.commit()


def subscribe_to_omer(user_id: int, lang: str) -> None:
    with psycopg2.connect(settings.db_parameters_string) as conn:
        cur = conn.cursor()
        query = 'INSERT INTO omer_subscriptions (user_id, lang) ' \
                'VALUES (%s, %s) ON CONFLICT DO NOTHING/UPDATE'
        cur.execute(query, (user_id, lang))
        conn.commit()

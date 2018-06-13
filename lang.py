import psycopg2
import redis
import settings
import text_handler


def set_lang(user, lang):
    conn = psycopg2.connect(dbname='jcalendarbot',
                            user='cloud-user',
                            host=config.HOST,
                            password='qwerty',
                            port=5432
                            )
    cur = conn.cursor()
    query = f'SELECT lang FROM lang WHERE id = {user}'
    cur.execute(query)
    lang_in_db = cur.fetchone()
    if not lang_in_db:
        query = f'INSERT INTO lang VALUES ({user}, \'{lang}\')'
        cur.execute(query)
        conn.commit()
    elif lang_in_db[0] != lang:
        query = f'UPDATE lang SET lang = \'{lang}\' WHERE id = {user}'
        cur.execute(query)
        conn.commit()
    r = redis.StrictRedis()
    r.set(f'{user}', lang)
    r.expire(f'{user}', 31536000)


def get_lang_by_id(user):
    conn = psycopg2.connect(dbname='jcalendarbot',
                            user='cloud-user',
                            host=config.HOST,
                            password='qwerty',
                            port=5432
                            )
    cur = conn.cursor()
    query = f'SELECT lang FROM lang WHERE id = {user}'
    cur.execute(query)
    lang_in_bd = cur.fetchone()[0]
    if not lang_in_bd:
        return False
    else:
        r = redis.StrictRedis()
        r.set(f'{user}', lang_in_bd[0])
        r.expire(f'{user}', 31536000)
        return lang_in_bd


def get_lang_from_redis(user):
    with redis.StrictRedis(host=settings.r_host, port=settings.r_port) as r:
        lang_in_redis = r.get(user)
        if not lang_in_redis:
            print('ЯЗЫКА НЕТУ')
            lang_in_db = get_lang_by_id(user)
            if not lang_in_db:
                return text_handler.change_lang(user)
            else:
                r.set(user, lang_in_db)
                r.expire(user, 31536000)
                lang = r.get(user).decode('unicode_escape')
        else:
            lang = r.get(user).decode('unicode_escape')
        return lang

from os import environ


TOKEN = environ.get('TOKEN')


DB_HOST = environ.get('DB_HOST')
DB_PORT = environ.get('DB_PORT')
DB_USER = environ.get('DB_USER')
DB_PASS = environ.get('DB_PASS')
DB_NAME = environ.get('DB_NAME')
DB_PARAMS = f'dbname={DB_NAME} user={DB_USER} password={DB_PASS} ' \
            f'host={DB_HOST} port={DB_PORT}'


ru_message = '*Кошерного и веселого Песаха!* Спасибо что продолжаете пользоваться ботом. ' \
             'Для того чтобы вам было легче выполнять заповедь счета омера, я добавил функцию ' \
             'напоминания о счёте омера. Чтобы получать эти напоминания, нажмите на кнопку ниже. ' \
             'Хаг самеах!\n— Беньямин Гинзбург'

en_message = '*Kosher and joyous Passover!*\nThank you for continuing to use the bot. ' \
             'In order to make it easier for you to fulfill the commandment of Sfirat haOmer, ' \
             'I\'ve added the reminder function of the count of the Omer. To receive these ' \
             'reminders, click the button below. Hag Sameach!\n- Benyamin Ginzburg'
ru_button = 'Подписаться'
en_button = 'Subscribe'


url = 'https://yasobe.ru/na/jcb'


messages = {'Russian': ru_message, 'English': en_message}
button_texts = {'Russian': ru_button, 'English': en_button}


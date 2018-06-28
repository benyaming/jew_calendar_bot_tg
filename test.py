from PIL import Image, ImageDraw, ImageFont
import rosh_hodesh
import os
from io import BytesIO
import telebot

lang = {
    'r': 'Russian',
    'e': 'English',
    'h': 'Hebrew'
}

'''
text example:

Месяц:|Ав
Число дней:|1 день
Дата:|13 Июля 2018 года, Пятница
Молад:|13 Июля, Пятница,^6 часов 49 минут и 8 частей
'''

# opening background
background = Image.open('res/backgrounds/rh.png')

# define bold and regular fonts
thin_font_path = os.path.join(
    'C:\\Users\Benyomin\PycharmProjects\\'
    'jew_calendar_bot_tg\\res\\fonts\\',
    'gothic.ttf'
)
bold_font_path = os.path.join(
    'C:\\Users\Benyomin\PycharmProjects\\'
    'jew_calendar_bot_tg\\res\\fonts\\',
    'gothic-bold.ttf'
)

# define draw object
draw = ImageDraw.Draw(background)
# get rh string
text = rosh_hodesh.get_rh((55.56, 38.17), lang['e'], (2006, 2, 25))

# split text to lines
text_lines = text.split('\n')

# draw title
draw.text(
    (250, 90),
    'РОШ ХОДЕШ',
    font=ImageFont.truetype(bold_font_path, size=60)
)

# define coordinates for main block
start_position_y = 370
start_position_x = 100

x_offset = 300
y_offset = 80

font_size = 46


bold_font = ImageFont.truetype(bold_font_path, size=font_size)
regular_font = ImageFont.truetype(thin_font_path, size=font_size)

regular_font_offset = regular_font.getsize
bold_font_offset = bold_font.getsize



# draw main block line-by-line
for line in text_lines:
    # definition part separetes from value part by '|' symbol
    line_parts = line.split('|')
    # draw definitions with bold font
    draw.text(
        (start_position_x, start_position_y),  # coordinates
        line_parts[0] + ' ',
        font=bold_font
    )

    # draw values with regular font and x-offsets
    if '^' not in line_parts[1]:
        # if value is too long
        if '*' in line_parts[1]:
            value_parts = line_parts[1].split('*')
            for value_part in value_parts:
                if value_part[0] == ',':
                    value_part = value_part.replace(', ', '')
                draw.text(
                    (
                        start_position_x + regular_font_offset(
                            line_parts[0]
                        )[0],
                        start_position_y
                    ),
                    value_part,
                    font=regular_font
                )
                start_position_y += 65
            start_position_y -= 65
        else:
            draw.text(
                (
                    start_position_x + regular_font_offset(line_parts[0])[0],
                    start_position_y
                ),
                line_parts[1],
                font=regular_font
            )
    else:
        # molad is too long, so it separeted by '^' symbol
        molad_parts = line_parts[1].split('^')
        for molad_part in molad_parts:
            # draw two lines of molad with offsets
            draw.text(
                (
                    start_position_x + regular_font_offset(line_parts[0])[0],
                    start_position_y
                ),
                molad_part,
                font=regular_font
            )
            start_position_y += 65
    # increasing y-offset
    start_position_y += y_offset
print(type(background))


bytes_io = BytesIO()
# saving the image
background.save(bytes_io, 'png')
print(type(bytes_io))
bytes_io.seek(0)
bot = telebot.TeleBot('496817539:AAE1MHP4NKLrG2D1QDh3d6wmuGwx1fl7ySI')
telebot.apihelper.proxy = {
    'https': 'socks5://tg_user_356:qrx59Opri@188.42.54.74:5185'
}
#bot.send_photo(5979588, bytes_io)
# bot.send_message('5979588', 123)


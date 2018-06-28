from PIL import Image, ImageDraw, ImageFont
import rosh_hodesh
import os

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
background = Image.open('res/backgrounds/rosh_hodesh.jpeg')

# define bold and regular fonts
thin_font_path = os.path.join(
    'C:\\Users\Benyomin\PycharmProjects'
    'jew_calendar_bot_tgres\\fonts\\',
    'Roboto-Light.ttf'
)
bold_font_path = os.path.join(
    'C:\\Users\Benyomin\PycharmProjects'
    'jew_calendar_bot_tgres\\fonts\\',
    'Roboto-Bold.ttf'
)

# define draw object
draw = ImageDraw.Draw(background)
# get rh string
text = rosh_hodesh.get_rh((55.56, 38.17), lang['r'])
# split text to lines
text_lines = text.split('\n')

# draw title
draw.text(
    (145, 50),
    'РОШ ХОДЕШ',
    font=ImageFont.truetype(bold_font_path, size=40)
)

# define coordinates for main block
start_position_y = 120
start_position_x = 35

x_offset = 150
y_offset = 40

# draw main block line-by-line
for line in text_lines:
    # definition part separetes from value part by '|' symbol
    line_parts = line.split('|')
    # draw definitions with bold font
    draw.text(
        (start_position_x, start_position_y),  # coordinates
        line_parts[0],
        font=ImageFont.truetype(bold_font_path, size=20)
    )
    # draw values with regular font and x-offsets
    if '^' not in line_parts[1]:
        draw.text(
            (start_position_x + x_offset, start_position_y),
            line_parts[1],
            font=ImageFont.truetype(thin_font_path, size=20)
        )
    else:
        # molad is too long, so it separeted by '^' symbol
        molad_parts = line_parts[1].split('^')
        for molad_part in molad_parts:
            # draw two lines of molad with offsets
            draw.text(
                (start_position_x + x_offset, start_position_y),
                molad_part,
                font=ImageFont.truetype(thin_font_path, size=20)
            )
            start_position_y += y_offset - 15
    # increasing y-offset
    start_position_y += y_offset

# saving the image
background.save('test.jpeg')

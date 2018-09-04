from PIL import Image, ImageDraw, ImageFont, PngImagePlugin

import os
from io import BytesIO

import localization


class PictureSender(object):

    _regular_font_path = os.path.join(
        os.path.abspath(os.getcwd()),
        'res/fonts/gothic.TTF'
    )
    _bold_font_path = os.path.join(
        os.path.abspath(os.getcwd()),
        'res/fonts/gothic-bold.TTF'
    )
    _title_font = ImageFont.truetype(
        _bold_font_path,
        60
    )

    @staticmethod
    def _convert_img_to_bytes_io(
            img: PngImagePlugin.PngImageFile
    ) -> BytesIO:
        bytes_io = BytesIO()
        img.save(bytes_io, 'png')
        bytes_io.seek(0)
        return bytes_io

    def _get_image(self, background_path) -> Image:
        self._image = Image.open(background_path)
        return self._image

    def _get_draw(self, background_path: str) -> ImageDraw:
        background = self._get_image(background_path)
        draw = ImageDraw.Draw(background)
        return draw

    def _draw_title(self, draw: ImageDraw, title: str, lang: str) -> None:
        draw.text(
            (250, 90),
            title,
            font=self._title_font
        )


class RoshHodeshSender(PictureSender):

    def __init__(self, lang: str):
        self._lang = lang
        self._data_font_size = 46
        self._regular_font = ImageFont.truetype(
            self._regular_font_path,
            size=self._data_font_size
        )
        self._bold_font = ImageFont.truetype(
            self._bold_font_path,
            size=self._data_font_size
        )
        self._bold_font_offset = self._bold_font.getsize
        self._background_path = 'res/backgrounds/rosh_hodesh.png'
        self._draw = self._get_draw(self._background_path)

    def _regular_font_offset(self, text):
        offset = self._regular_font.getsize(text)[0]
        return offset

    def _draw_rh_data(self, data: str):
        start_position_y = 370
        start_position_x = 100
        y_offset = 80
        text_lines = data.split('\n')
        draw = self._draw

        for line in text_lines:
            # definition part separetes from value part by '|' symbol
            line_parts = line.split('|')
            # draw definitions with bold font
            draw.text(
                (start_position_x, start_position_y),  # coordinates
                line_parts[0] + ' ',
                font=self._bold_font
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
                                start_position_x + self._regular_font_offset(
                                    line_parts[0]
                                ),
                                start_position_y
                            ),
                            value_part,
                            font=self._regular_font
                        )
                        start_position_y += 65
                    start_position_y -= 65
                else:
                    draw.text(
                        (
                            start_position_x +
                            self._regular_font_offset(line_parts[0]),
                            start_position_y
                        ),
                        line_parts[1],
                        font=self._regular_font
                    )
            else:
                # molad is too long, so it separeted by '^' symbol
                molad_parts = line_parts[1].split('^')
                for molad_part in molad_parts:
                    # draw two lines of molad with offsets
                    draw.text(
                        (
                            start_position_x +
                            self._regular_font_offset(line_parts[0]),
                            start_position_y
                        ),
                        molad_part,
                        font=self._regular_font
                    )
                    start_position_y += 65
            # increasing y-offset
            start_position_y += y_offset

    def get_rh_picture(
            self,
            text: str,
    ) -> BytesIO:
        self._draw_title(
            self._draw,
            localization.RoshHodesh.titles[self._lang],
            self._lang
        )
        self._draw_rh_data(text)
        pic = self._convert_img_to_bytes_io(self._image)
        return pic


class DafYomiSender(PictureSender):
    def __init__(self, lang: str):
        self._lang = lang
        self._data_font_size = 90
        self._regular_font = ImageFont.truetype(
            self._regular_font_path,
            size=self._data_font_size
        )
        self._bold_font = ImageFont.truetype(
            self._bold_font_path,
            size=self._data_font_size
        )
        self._bold_font_offset = self._bold_font.getsize
        self._background_path = 'res/backgrounds/daf_yomi.png'
        self._draw = self._get_draw(self._background_path)

    def _regular_font_offset(self, text):
        offset = self._regular_font.getsize(text)[0]
        return offset

    def _draw_daf_data(self, data: str):
        start_position_y = 470
        start_position_x = 100
        y_offset = 100
        text_lines = data.split('\n')
        draw = self._draw

        for line in text_lines:
            # definition part separetes from value part by '|' symbol
            line_parts = line.split('|')
            draw.text(
                (start_position_x, start_position_y),  # coordinates
                line_parts[0] + ' ',
                font=self._bold_font
            )
            draw.text(
                (
                    start_position_x +
                    self._regular_font_offset(line_parts[0]),
                    start_position_y
                ),
                line_parts[1],
                font=self._regular_font
            )
            start_position_y += y_offset

    def get_daf_picture(self, text: str) -> BytesIO:
        self._draw_title(
            self._draw,
            localization.DafYomi.titles[self._lang],
            self._lang
        )
        self._draw_daf_data(text)
        pic = self._convert_img_to_bytes_io(self._image)
        return pic


class ShabbosSender(PictureSender):

    def __init__(self, lang: str):
        self._lang = lang
        self._data_font_size = 60
        self._warning_font_size_s = 48
        self._regular_font = ImageFont.truetype(
            self._regular_font_path,
            size=self._data_font_size
        )
        self._bold_font = ImageFont.truetype(
            self._bold_font_path,
            size=self._data_font_size
        )
        self._warning_font = ImageFont.truetype(
            self._bold_font_path,
            size=self._warning_font_size_s
        )
        self._background_path = 'res/backgrounds/shabbos.png'
        self._draw = self._get_draw(self._background_path)

    def _bold_font_offset(self, text):
        offset = self._bold_font.getsize(text)[0]
        return offset

    def _draw_shabbos_data(self, data: str, shabbos_warning: bool):
        start_position_y = 400
        start_position_x = 100
        y_offset = 80
        draw = self._draw
        if shabbos_warning:
            if '%' in data:
                text_lines = data.split('%')[0].split('\n')
            else:
                text_lines = data.split('?')[0].split('\n')
                start_position_y = 470
        else:
            text_lines = data.split('\n')
        for line in text_lines:
            if '+' in line:
                # draw candle offset line
                line = line.split('+')[1]
                draw.text(
                    (start_position_x, start_position_y),
                    line,
                    font=self._regular_font,
                )
                start_position_y += y_offset
            else:
                # definition part separetes from value part by '|' symbol
                line_parts = line.split('|')
                draw.text(
                    (start_position_x, start_position_y),  # coordinates
                    line_parts[0] + ' ',
                    font=self._bold_font
                )
                draw.text(
                    (
                        start_position_x +
                        self._bold_font_offset(line_parts[0]),
                        start_position_y
                    ),
                    line_parts[1],
                    font=self._regular_font
                )
                start_position_y += y_offset

        if shabbos_warning:
            if '?' in data:
                start_position_y = 810
                if self._lang == 'English':
                    start_position_y = 830
                warning_lines = data.split('?')[1].split('\n')
            else:
                warning_lines = data.split('%')[1].split('\n')
                start_position_y = 830
            start_position_x = 100
            y_offset = 50
            for line in warning_lines:
                draw.text(
                    (start_position_x, start_position_y),  # coordinates
                    line,
                    font=self._warning_font,
                    fill='#ff5959'
                )
                start_position_y += y_offset

    def get_shabbos_picture(self, text: str) -> BytesIO:
        shabbos_warning = False
        if '%' in text or '?' in text:
            shabbos_warning = True
            self._background_path = 'res/backgrounds/shabbos_attention.png'
            self._draw = self._get_draw(self._background_path)
        self._draw_title(
            self._draw,
            localization.Shabos.titles[self._lang],
            self._lang
        )
        self._draw_shabbos_data(text, shabbos_warning)
        pic = self._convert_img_to_bytes_io(self._image)
        return pic


class ZmanimSender(PictureSender):

    def __init__(self, lang):
        self._lang = lang
        self._background_path = 'res/backgrounds/zmanim.png'
        self._draw = self._get_draw(self._background_path)

    def _regular_font_offset(self, text):
        offset = self._regular_font.getsize(text)[0]
        return offset

    def _get_font_properties(self, number_of_lines: int) -> dict:
        p = {
            # [font_size, y_offset, start_y_offset, start_x_offset
            1: [58, 68,300],
            2: [58, 68, 270],
            3: [58, 68, 220],
            4: [58, 68, 180],
            5: [58, 68, 160],
            6: [58, 68, 140],
            7: [58, 68, 100],
            8: [58, 68, 85],
            9: [58, 68, 85],
            10: [59, 68, 40],
            11: [57, 66, 20],
            12: [55, 64, 20],
            13: [52, 58, 20],
            14: [45, 52, 20],
            15: [43, 50, 10],
            16: [41, 48, 10],
            17: [39, 46, 0],
            18: [37, 44, 0],
            19: [35, 42, 0]
        }

        self._data_font_size = p.get(number_of_lines)[0]
        self._regular_font = ImageFont.truetype(
            self._regular_font_path,
            size=self._data_font_size
        )
        self._bold_font = ImageFont.truetype(
            self._bold_font_path,
            size=self._data_font_size
        )
        self._bold_font_offset = self._bold_font.getsize
        font_params = {
            'y_offset': p.get(number_of_lines)[1],
            'start_y_offset': p.get(number_of_lines)[2]
        }
        return font_params

    def _draw_zmanim(self, text: str):
        start_position_y = 210
        start_position_x = 100
        draw = self._draw

        lines = text.split('\n')

        number_of_lines = len(lines)
        font_params = self._get_font_properties(number_of_lines)
        y_offset = font_params['y_offset']
        start_position_y += font_params['start_y_offset']

        for line in lines:
            line_parts = line.split('—')
            # draw zman name
            draw.text(
                (start_position_x, start_position_y),  # coordinates
                line_parts[0],
                font=self._bold_font
            )

            # draw zman value
            draw.text(
                (
                    start_position_x +
                    self._bold_font_offset(line_parts[0])[0],
                    start_position_y
                ),  # coordinates
                line_parts[1],
                font=self._regular_font
            )
            start_position_y += y_offset

    def get_zmanim_picture(self, text: str) -> BytesIO:
        self._draw_title(
            self._draw,
            localization.Zmanim.titles[self._lang],
            self._lang
        )
        self._draw_zmanim(text)
        pic = self._convert_img_to_bytes_io(self._image)
        return pic


class FastSender(PictureSender):

    def __init__(self, lang):
        self._lang = lang
        self._background_path = 'res/backgrounds/fast.png'
        self._draw = self._get_draw(self._background_path)
        self._data_font_size = 60
        self._regular_font = ImageFont.truetype(
            self._regular_font_path,
            size=self._data_font_size
        )
        self._bold_font = ImageFont.truetype(
            self._bold_font_path,
            size=self._data_font_size
        )
        self._bold_font_offset = self._bold_font.getsize

    def _draw_fast_data(self, text: str):
        start_position_y = 290
        start_position_x = 100
        y_offset = 80
        draw = self._draw
        lines = text.split('\n')

        for line in lines:
            # separate the fast's end block
            if line.startswith('%'):
                line = line.split('%')[1]
                start_position_y += y_offset
            # separate the chatzot
            if line.startswith('$'):
                line = line.split('$')[1]
                start_position_y += 40
            line_parts = line.split('|')
            # draw parameter name
            draw.text(
                (start_position_x, start_position_y),  # coordinates
                line_parts[0],
                font=self._bold_font
            )
            for sub_part in line_parts[1].split('^'):
                draw.text(
                    (
                        start_position_x +
                        self._bold_font_offset(line_parts[0])[0],
                        start_position_y
                    ),
                    sub_part,
                    font=self._regular_font
                )
                if '^' in line:
                    start_position_y += y_offset - 15
                else:
                    start_position_y += y_offset

    def get_image(self, text: str) -> BytesIO:
        title = text.split('\n\n')[0]
        self._draw_title(self._draw, title, self._lang)
        self._draw_fast_data(text.split('\n\n')[1])
        pic = self._convert_img_to_bytes_io(self._image)
        return pic


class IsraelHolidaysSender(PictureSender):

    def __init__(self, lang):
        self._lang = lang
        self._background_path = 'res/backgrounds/israel_holidays.png'
        self._draw = self._get_draw(self._background_path)
        self._data_font_size = 60
        self._regular_font = ImageFont.truetype(
class TuBiShvatSnder(PictureSender):

    def __init__(self, lang):
        self._lang = lang
        self._background_path = 'res/backgrounds/tubishvat.png'
        self._draw = self._get_draw(self._background_path)
        self._data_font_size = 70
        self._regular_font = ImageFont.truetype(
            self._regular_font_path,
            size=self._data_font_size
        )
        self._bold_font = ImageFont.truetype(
            self._bold_font_path,
            size=self._data_font_size
        )
        self._bold_font_offset = self._bold_font.getsize

    def _draw_tubishvat_data(self, text: str):
        start_position_y = 450
        start_position_x = 100
        y_offset = 90
        draw = self._draw

        # holiday_name
        holiday_name_text = text.split('|')[0]
        draw.text(
            (start_position_x, start_position_y),  # coordinates
            holiday_name_text,
            font=self._bold_font
        )
        # date
        date_text = text.split('|')[1].split('^')[0]
        draw.text(
            (
                start_position_x +
                self._bold_font_offset(holiday_name_text)[0],
                start_position_y
            ),
            date_text,
            font=self._regular_font
        )

        start_position_y += y_offset

        # day of week
        day_text = text.split('|')[1].split('^')[1]
        draw.text(
            (
                start_position_x +
                self._bold_font_offset(holiday_name_text)[0],
                start_position_y
            ),
            day_text,
            font=self._regular_font
        )

    def get_image(self, text: str) -> BytesIO:
        title = localization.Holidays.titles['tubishvat'][self._lang]
        self._draw_title(self._draw, title, self._lang)
        self._draw_tubishvat_data(text)
        pic = self._convert_img_to_bytes_io(self._image)
        return pic


# lang = 'Russian'
# FastSender(lang).get_fast_image(text)

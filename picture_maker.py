from PIL import Image, ImageDraw, ImageFont, PngImagePlugin

import os
from io import BytesIO

import localization


class PictureSender(object):

    _regular_font_path = os.path.join(os.path.abspath(os.getcwd()), 'res/fonts/gothic.ttf'
    )
    _bold_font_path = os.path.join(os.path.abspath(os.getcwd()), 'res/fonts/gothic-bold.ttf'
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
        self._bold_font_offset = self._bold_font.getsize
        self._background_path = 'res/backgrounds/shabbos.png'
        self._draw = self._get_draw(self._background_path)

    def _regular_font_offset(self, text):
        offset = self._regular_font.getsize(text)[0]
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
        if '%' or '?' in text:
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
        self._image.save('test.png')
        return pic

import data, localization, converter


def handle_heb_date(text, lang):
    year, month, day = None, None, None
    input_data = text.split()
    if len(input_data) in [3, 4]:
        # check day
        if input_data[0].isdigit():
            day = int(input_data[0])
            if not 0 < day < 31:
                return 'incorrect_date_value'
        # check month
        if len(input_data) == 3:
            # all exept adar ii
            if input_data[1] in data.heb_months_names_ru or \
                  input_data[1] in data.heb_months_names_en or \
                      input_data[1] in data.heb_months_names_he:
                month = localization.Converter.get_month_name(
                    lang,
                    input_data[1]
                )
            else:
                return 'incorrect_date_format'
        elif len(input_data) == 4 \
            and input_data[1] in ['adar', 'адар', 'qqqq'] \
                and input_data[2] == ['1']:
            month = localization.Converter.get_month_name(
                    lang,
                    f'{input_data[1]} 2'
            )
        else:
            return 'incorrect_date_format'
        # check year
        if input_data[-1].isdigit():
            year = int(input_data[-1])
            if year < 0:
                return 'incorrect_date_value'
            # final calculation
            else:
                hebrew_date = (year, month, day)
                response = converter.convert_heb_to_greg(hebrew_date, lang)
                if response:
                    message_text = response['response']
                    return message_text
                else:
                    return 'incorrect_date_value'
    else:
        return 'incorrect_date_format'


while(True):
    text = input('#')
    print(handle_heb_date(text, 'English'))

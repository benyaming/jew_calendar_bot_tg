from telebot import TeleBot
from telebot.types import CallbackQuery

import settings, data, keyboards, db_operations, localization

from db_operations import get_zmanim_set, update_zmanim_set


def update_zmanim_set(zmanim_set: str, zman_code: int) -> str:
    zmanim_set_list = list(zmanim_set)
    zmanim_set_list[zman_code] = str(1 - int(zmanim_set_list[zman_code]))
    new_zmanim_set = ''.join(zmanim_set_list)
    return new_zmanim_set


def edit_zman_status():
    zman_name = call.data.split('-')[1]
    zman_code = data.zmanim_names_to_codes[zman_name]
    old_set = get_zmanim_set(user)
    new_set = update_zmanim_set(old_set, zman_code)
    update_zmanim_set(user, new_set)
    bot.answer_callback_query(call.id)
    edited_reply_markup = keyboards.get_zmanim_callback_menu(lang, user)
    bot.edit_message_reply_markup(
        call.message.chat.id,
        call.message.message_id,
        reply_markup=edited_reply_markup
    )


def edit_candle_offset():
    new_offset = int(call.data.split('-')[1].split(' ')[-1])
    offset_canged = db_operations.update_candle_offset(user, new_offset)
    if offset_canged:
        bot.answer_callback_query(call.id)
        edited_markup = keyboards.get_candle_offset_callback_menu(user)
        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=edited_markup
        )
    else:
        allert_text = localization.Shabos.same_offset_error(lang)
        bot.answer_callback_query(call.id, allert_text)


def edit_diaspora():
    status = bool(int(call.data.split('-')[1]))
    db_operations.toggle_diaspora_status(user)
    allert_text = localization.Utils.diaspora_status_allert(lang, status)
    bot.answer_callback_query(call.id, allert_text, show_alert=True)
    new_message_text = localization.Utils.diaspora(lang, status)
    new_markup = keyboards.get_diaspora_callback_menu(lang, user)
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=new_message_text,
        reply_markup=new_markup,
        parse_mode='Markdown'
    )


def handle_callback(user_id: int, callback: CallbackQuery) -> None:
    global bot, user, call, lang
    bot = TeleBot(settings.TOKEN)
    user = user_id
    call = callback
    lang = db_operations.get_lang_from_redis(user)
    payload_prefix = call.data.split('-')[0]
    prefixes = {
        'zmanim': edit_zman_status,
        'candle_offset': edit_candle_offset,
        'diaspora': edit_diaspora,

    }
    func = prefixes.get(payload_prefix, '')
    func()

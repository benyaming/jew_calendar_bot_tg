from telebot import TeleBot
from telebot.types import CallbackQuery

import jcb_chatbase

import settings
import data
import keyboards as kbrd
import db_operations
import localization
import zmanim


class CallbackHandler(object):

    def __init__(self, user_id: int, call: CallbackQuery):
        self._bot = TeleBot(settings.TOKEN)
        self._user_id = user_id
        self._call = call
        self._lang = db_operations.get_lang_from_redis(self._user_id)

    def _chatbase(
            self,
            intent: str,
            text=None,
            agent='bot'
    ):
        if agent == 'user':
            jcb_chatbase.chatbase_user_msg_handler(
                self._user_id,
                text,
                intent
            )
        elif agent == 'bot':
            jcb_chatbase.chatbase_bot_handler(self._user_id, intent)

    def handle_call(self):
        payload_prefix = self._call.data.split('-')[0]
        func = self._call_prefixes.get(payload_prefix, '')
        func(self)

    @staticmethod
    def _update_zmanim_set(zmanim_set: str, zman_code: int) -> str:
        zmanim_set_list = list(zmanim_set)
        zmanim_set_list[zman_code] = str(1 - int(zmanim_set_list[zman_code]))
        new_zmanim_set = ''.join(zmanim_set_list)
        return new_zmanim_set

    def _edit_zman_status(self):
        zman_name = self._call.data.split('-')[1]
        zman_code = data.zmanim_names_to_codes[zman_name]
        old_set = db_operations.get_zmanim_set(self._user_id)
        new_set = self._update_zmanim_set(old_set, zman_code)
        db_operations.update_zmanim_set(self._user_id, new_set)
        self._bot.answer_callback_query(self._call.id)
        edited_reply_markup = kbrd.get_zmanim_callback_menu(
            self._lang,
            self._user_id
        )
        self._bot.edit_message_reply_markup(
            self._call.message.chat.id,
            self._call.message.message_id,
            reply_markup=edited_reply_markup
        )

    def _edit_candle_offset(self):
        new_offset = int(self._call.data.split('-')[1].split(' ')[-1])
        offset_canged = db_operations.update_candle_offset(
            self._user_id,
            new_offset
        )
        if offset_canged:
            self._bot.answer_callback_query(self._call.id)
            edited_markup = kbrd.get_candle_offset_callback_menu(self._user_id)
            self._bot.edit_message_reply_markup(
                self._call.message.chat.id,
                self._call.message.message_id,
                reply_markup=edited_markup
            )
        else:
            allert_text = localization.Shabos.same_offset_error(self._lang)
            self._bot.answer_callback_query(self._call.id, allert_text)

    def _get_zmanim_by_date(self):
        self._chatbase(
            'zmanim from the callback button',
            'Callback button pressed',
            'user'
        )
        self._bot.answer_callback_query(self._call.id)
        self._bot.send_chat_action(self._user_id, 'upload_photo')
        raw_date = self._call.data.split('-')[1]
        custom_date = (
            int(raw_date.split('.')[0]),
            int(raw_date.split('.')[1]),
            int(raw_date.split('.')[2])
        )
        response = zmanim.get_zmanim(self._user_id, self._lang, custom_date)
        if response['polar_error']:
            self._bot.send_chat_action(self._user_id, 'typing')
            response_message = response['polar_error']
            self._bot.send_message(self._user_id, response_message)
            self._chatbase('zmanim polar error')
        elif response['zmanim_set_error']:
            self._bot.send_chat_action(self._user_id, 'typing')
            response_message = response['zmanim_set_error']
            user_markup = kbrd.get_zmanim_callback_menu(
                self._lang,
                self._user_id
            )
            self._bot.send_message(
                self._user_id,
                response_message,
                reply_markup=user_markup
            )
            self._chatbase('zmanim set error')
        else:
            self._bot.send_chat_action(self._user_id, 'upload_photo')
            response_pic = response['zmanim_pic']
            self._bot.send_photo(self._user_id, response_pic)
            response_pic.close()
            self._chatbase('zmanim from callback button sent')

    def _edit_diaspora(self):
        status = bool(int(self._call.data.split('-')[1]))
        db_operations.toggle_diaspora_status(self._user_id)
        allert_text = localization.Utils.diaspora_status_allert(
            self._lang,
            status
        )
        self._bot.answer_callback_query(
            self._call.id,
            allert_text,
            show_alert=True
        )
        new_message_text = localization.Utils.diaspora(self._lang, status)
        new_markup = kbrd.get_diaspora_callback_menu(self._lang, self._user_id)
        self._bot.edit_message_text(
            chat_id=self._call.message.chat.id,
            message_id=self._call.message.message_id,
            text=new_message_text,
            reply_markup=new_markup,
            parse_mode='Markdown'
        )

    _call_prefixes = {
        'zmanim': _edit_zman_status,
        'candle_offset': _edit_candle_offset,
        'diaspora': _edit_diaspora,
        'get_zmanim': _get_zmanim_by_date,
    }

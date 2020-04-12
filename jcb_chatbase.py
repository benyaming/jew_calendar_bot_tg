# from chatbase import Message, MessageTypes
import time
import settings


API_KEY = settings.CHATBASE_TOKEN
PLATFORM = 'Telegram'
VERSION = '2.0'
TIME_STAMP = int(round(time.time() * 1e3))


def chatbase_user_msg_handler(
        user_id: int,
        message: str,
        intent_message: str,
        not_handled=False
) -> None:
    # user_message = Message(
    #     api_key=API_KEY,
    #     platform=PLATFORM,
    #     version=VERSION,
    #     time_stamp=TIME_STAMP,
    #     type=MessageTypes.USER,
    #     user_id=user_id,
    #     message=message,
    #     intent=intent_message,
    #     not_handled=not_handled
    # )
    # user_message.send()
    ...


# Handler for bot's message
def chatbase_bot_handler(user_id: int, message: str) -> None:
    # set_bot_message = Message(
    #     api_key=API_KEY,
    #     platform=PLATFORM,
    #     version=VERSION,
    #     time_stamp=TIME_STAMP,
    #     type=MessageTypes.AGENT,
    #     user_id=user_id,
    #     message=message
    # )
    # set_bot_message.send()
    ...

import os
from time import sleep

from max_client import (
    ApiClient,
    BotsApi,
    CallbackButton,
    ChatsApi,
    Configuration,
    InlineKeyboardAttachment,
    InlineKeyboardAttachmentRequest,
    InlineKeyboardAttachmentRequestPayload,
    Intent,
    LinkButton,
    Message,
    MessageCreatedUpdate,
    MessagesApi,
    NewMessageBody,
    Recipient,
    RequestContactButton,
    RequestGeoLocationButton,
    SubscriptionsApi,
    Update,
    UploadApi,
)
from max_client.rest import ApiException


def main_menu_buttons():
    # type: () -> []
    return [
        {[CallbackButton("About bot", "start_test", intent=Intent.POSITIVE)]},
        [
            CallbackButton(
                "All chat bots", "list_all_chats_show", intent=Intent.POSITIVE
            )
        ],
        [LinkButton("API documentation for Max-bots", "https://dev.max.ru/docs")],
        [
            LinkButton(
                "JSON Diagram API Max Bots",
                "https://github.com/max-messenger/max-bot-api-schema",
            )
        ],
        [RequestContactButton("Report your contact details")],
        [RequestGeoLocationButton("Report your location", True)],
    ]


def add_buttons_to_message_body(message_body, buttons):
    # type: (NewMessageBody, list) -> NewMessageBody
    prev_attachments = message_body.attachments
    message_body.attachments = [
        InlineKeyboardAttachmentRequest(InlineKeyboardAttachmentRequestPayload(buttons))
    ]
    if prev_attachments:
        for it in prev_attachments:
            if not isinstance(it, InlineKeyboardAttachment):
                message_body.attachments.append(it)
    return message_body


def handle_message_created_update(update):
    if hasattr(update, "message") and isinstance(update.message, Message):
        message = update.message

    if isinstance(message, Message):
        if isinstance(message.recipient, Recipient):
            recipient = message.recipient
            #               return msg.send_message(NewMessageBody("отредактировал сообщение"), chat_id=recipient.chat_id)
            return msg.send_message(
                add_buttons_to_message_body(
                    NewMessageBody("Гланое menu"), main_menu_buttons()
                ),
                chat_id=recipient.chat_id,
            )
    return None


#               return msg.send_message(NewMessageBody("Гланое menu"), chat_id=recipient.chat_id)


def handle_update(update):
    # type: (Update) -> bool
    # noinspection PyBroadException
    try:
        if isinstance(update, MessageCreatedUpdate):
            res = handle_message_created_update(update)
        else:
            res = False
        return res
    except Exception as e:
        print(f"Exception when calling handle_update: {e}\n")


conf = Configuration()
conf.api_key["access_token"] = os.environ.get("MAX_BOT_API_TOKEN")
# conf.api_key['access_token'] = os.environ.get('TT_BOT_API_TOKEN')
client = ApiClient(conf)
api = BotsApi(client)
info = api.get_my_info()
print(info)


subscriptions = SubscriptionsApi(client)
msg = MessagesApi(client)
api = BotsApi(client)
chats = ChatsApi(client)
upload = UploadApi(client)

stop_polling = False
polling_sleep_time = 5
polling_error_sleep_time = 5

marker = None
while not stop_polling:
    try:
        if marker:
            ul = subscriptions.get_updates(
                marker=marker, types=Update.update_types, _request_timeout=45
            )
        else:
            ul = subscriptions.get_updates(
                types=Update.update_types, _request_timeout=45
            )
            marker = ul.marker
        if ul.updates:
            for update in ul.updates:
                handle_update(update)
                stop_polling = True
        else:
            sleep(polling_sleep_time)
    except ApiException as err:
        if str(err.body).lower().find("Invalid access_token"):
            raise
    except Exception:
        sleep(polling_error_sleep_time)
        # raise

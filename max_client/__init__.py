# coding: utf-8

# flake8: noqa

"""
    Max Bot API

    # About Bot API allows bots to interact with Max. Methods are called by sending HTTPS requests to [botapi.max.ru](https://botapi.max.ru) domain. Bots are third-party applications that use Max features. A bot can legitimately take part in a conversation. It can be achieved through HTTP requests to the Max Bot API.  ## Features Max bots of the current version are able to: - Communicate with users and respond to requests - Recommend users complete actions via programmed buttons - Request personal data from users (name, short reference, phone number) We'll keep working on expanding bot capabilities in the future.  ## Examples Bots can be used for the following purposes: - Providing support, answering frequently asked questions - Sending typical information - Voting - Likes/dislikes - Following external links - Forwarding a user to a chat/channel  ## @MasterBot [MasterBot](https://max.ru/MasterBot) is the main bot in Max, all bots creator. Use MasterBot to create and edit your bots. Feel free to contact us for any questions, [@support](https://max.ru/support) or [help@max.ru](mailto:help@max.ru).  ## HTTP verbs `GET` &mdash; getting resources, parameters are transmitted via URL  `POST` &mdash; creation of resources (for example, sending new messages)  `PUT` &mdash; editing resources  `DELETE` &mdash; deleting resources  `PATCH` &mdash; patching resources  ## HTTP response codes `200` &mdash; successful operation  `400` &mdash; invalid request  `401` &mdash; authentication error  `404` &mdash; resource not found  `405` &mdash; method is not allowed  `429` &mdash; the number of requests is exceeded  `503` &mdash; service unavailable  ## Resources format For content requests (PUT and POST) and responses, the API uses the JSON format. All strings are UTF-8 encoded. Date/time fields are represented as the number of milliseconds that have elapsed since 00:00 January 1, 1970 in the long format. To get it, you can simply multiply the UNIX timestamp by 1000. All date/time fields have a UTC timezone. ## Error responses In case of an error, the API returns a response with the corresponding HTTP code and JSON with the following fields:  `code` - the string with the error key  `message` - a string describing the error </br>  For example: ```bash > http https://botapi.max.ru/chats?access_token={EXAMPLE_TOKEN} HTTP / 1.1 403 Forbidden Cache-Control: no-cache Connection: Keep-Alive Content-Length: 57 Content-Type: application / json; charset = utf-8 Set-Cookie: web_ui_lang = ru; Path = /; Domain = .max.ru; Expires = 2019-03-24T11: 45: 36.500Z {    \"code\": \"verify.token\",    \"message\": \"Invalid access_token\" } ``` ## Receiving notifications Max Bot API supports 2 options of receiving notifications on new events for bots: - Push notifications via WebHook. To receive data via WebHook, you'll have to [add subscription](https://dev.max.ru/#operation/subscribe); - Notifications upon request via [long polling](#operation/getUpdates) API. All data can be received via long polling **by default** after creating the bot.  Both methods **cannot** be used simultaneously. Refer to the response schema of [/updates](https://dev.max.ru/#operation/getUpdates) method to check all available types of updates.  ### Webhook There is some notes about how we handle webhook subscription: 1. Sometimes webhook notification cannot be delivered in case when bot server or network is down.    In such case we well retry delivery in a short period of time (from 30 to 60 seconds) and will do this until get   `200 OK` status code from your server, but not longer than **8 hours** (*may change over time*) since update happened.    We also consider any non `200`-response from server as failed delivery.  2. To protect your bot from unexpected high load we send **no more than 100** notifications per second by default.   If you want increase this limit, contact us at [@support](https://max.ru/support).   It should be from one of the following subnets: ``` 5.101.42.200/31 31.177.104.200/31 89.221.230.200/31 ```   ## Message buttons You can program buttons for users answering a bot. Max supports the following types of buttons:  `callback` &mdash; sends a notification with payload to a bot (via WebHook or long polling)  `link` &mdash; makes a user to follow a link  `request_contact` &mdash; requests the user permission to access contact information (phone number, short link, email)  `request_geo_location` &mdash; asks user to provide current geo location  `chat` &mdash; creates chat associated with message  To start create buttons [send message](#operation/sendMessage) with `InlineKeyboardAttachment`: ```json {   \"text\": \"It is message with inline keyboard\",   \"attachments\": [     {       \"type\": \"inline_keyboard\",       \"payload\": {         \"buttons\": [           [             {               \"type\": \"callback\",               \"text\": \"Press me!\",               \"payload\": \"button1 pressed\"             }           ],           [             {               \"type\": \"chat\",               \"text\": \"Discuss\",               \"chat_title\": \"Message discussion\"             }           ]         ]       }     }   ] } ``` ### Chat button Chat button is a button that starts chat assosiated with the current message. It will be **private** chat with a link, bot will be added as administrator by default.  Chat will be created as soon as the first user taps on button. Bot will receive `message_chat_created` update.  Bot can set title and description of new chat by setting `chat_title` and `chat_description` properties.  Whereas keyboard can contain several `chat`-buttons there is `uuid` property to distinct them between each other. In case you do not pass `uuid` we will generate it. If you edit message, pass `uuid` so we know that this button starts the same chat as before.  Chat button also can contain `start_payload` that will be sent to bot as part of `message_chat_created` update.  ## Deep linking Max supports deep linking mechanism for bots. It allows passing additional payload to the bot on startup. Deep link can contain any data encoded into string up to **128** characters long. Longer strings will be omitted and **not** passed to the bot.  Each bot has start link that looks like: ``` https://max.ru/%BOT_USERNAME%/start/%PAYLOAD% ``` As soon as user clicks on such link we open dialog with bot and send this payload to bot as part of `bot_started` update: ```json {     \"update_type\": \"bot_started\",     \"timestamp\": 1573226679188,     \"chat_id\": 1234567890,     \"user\": {         \"user_id\": 1234567890,         \"name\": \"Boris\",         \"username\": \"borisd84\"     },     \"payload\": \"any data meaningful to bot\" } ```  Deep linking mechanism is supported for iOS version 2.7.0 and Android 2.9.0 and higher.  ## Text formatting  Message text can be improved with basic formatting such as: **strong**, *emphasis*, ~strikethough~,  <ins>underline</ins>, `code` or link. You can use either markdown-like or HTML formatting.  To enable text formatting set the `format` property of [NewMessageBody](#tag/new_message_model).  ### Max flavored Markdown To enable [Markdown](https://spec.commonmark.org/0.29/) parsing, set the `format` property of [NewMessageBody](#tag/new_message_model) to `markdown`.  We currently support only the following syntax:  `*empasized*` or `_empasized_` for *italic* text  `**strong**` or `__strong__` for __bold__ text  `~~strikethough~~`  for ~strikethough~ text  `++underline++`  for <ins>underlined</ins> text  ``` `code` ``` or ` ```code``` ` for `monospaced` text  `^^important^^` for highlighted text (colored in red, by default)  `[Inline URL](https://dev.max.ru/)` for inline URLs  `[User mention](max://user/%user_id%)` for user mentions without username  `# Header` for header  ### HTML support  To enable HTML parsing, set the `format` property of [NewMessageBody](#tag/new_message_model) to `html`.  Only the following HTML tags are supported. All others will be stripped:  Emphasized: `<i>` or `<em>`  Strong: `<b>` or `<strong>`  Strikethrough: `<del>` or `<s>`  Underlined: `<ins>` or `<u>`  Link: `<a href=\"https://dev.max.ru\">Docs</a>`  Monospaced text: `<pre>` or `<code>`  Highlighted text: `<mark>`  Header: `<h1>`  Text formatting is supported for iOS since version 3.1 and Android since 2.20.0.  # Versioning API models and interface may change over time. To make sure your bot will get the right info, we strongly recommend adding API version number to each request. You can add it as `v` parameter to each HTTP-request. For instance, `v=0.1.2`. To specify the data model version you are getting through WebHook subscription, use the `version` property in the request body of the [subscribe](https://dev.max.ru/#operation/subscribe) request.  # Libraries We have developed the official [Java client](https://github.com/max-messenger/max-bot-api-client-java) and [SDK](https://github.com/max-messenger/max-bot-sdk-java).  # Changelog To see changelog for older versions visit our [GitHub](https://github.com/max-messenger/max-bot-api-schema/releases).  # noqa: E501

    OpenAPI spec version: 0.0.10
"""


from __future__ import absolute_import

__version__ = "1.0.0"

# import apis into sdk package
from max_client.api.bots_api import BotsApi
from max_client.api.chats_api import ChatsApi
from max_client.api.messages_api import MessagesApi
from max_client.api.subscriptions_api import SubscriptionsApi
from max_client.api.upload_api import UploadApi

# import ApiClient
from max_client.api_client import ApiClient
from max_client.configuration import Configuration
# import models into sdk package
from max_client.models.action_request_body import ActionRequestBody
from max_client.models.attachment import Attachment
from max_client.models.attachment_payload import AttachmentPayload
from max_client.models.attachment_request import AttachmentRequest
from max_client.models.audio_attachment import AudioAttachment
from max_client.models.audio_attachment_request import AudioAttachmentRequest
from max_client.models.bot_added_to_chat_update import BotAddedToChatUpdate
from max_client.models.bot_command import BotCommand
from max_client.models.bot_info import BotInfo
from max_client.models.bot_patch import BotPatch
from max_client.models.bot_removed_from_chat_update import BotRemovedFromChatUpdate
from max_client.models.bot_started_update import BotStartedUpdate
from max_client.models.button import Button
from max_client.models.callback import Callback
from max_client.models.callback_answer import CallbackAnswer
from max_client.models.callback_button import CallbackButton
from max_client.models.chat import Chat
from max_client.models.chat_admin import ChatAdmin
from max_client.models.chat_admin_permission import ChatAdminPermission
from max_client.models.chat_admins_list import ChatAdminsList
from max_client.models.chat_button import ChatButton
from max_client.models.chat_list import ChatList
from max_client.models.chat_member import ChatMember
from max_client.models.chat_members_list import ChatMembersList
from max_client.models.chat_patch import ChatPatch
from max_client.models.chat_status import ChatStatus
from max_client.models.chat_title_changed_update import ChatTitleChangedUpdate
from max_client.models.chat_type import ChatType
from max_client.models.contact_attachment import ContactAttachment
from max_client.models.contact_attachment_payload import ContactAttachmentPayload
from max_client.models.contact_attachment_request import ContactAttachmentRequest
from max_client.models.contact_attachment_request_payload import ContactAttachmentRequestPayload
from max_client.models.data_attachment import DataAttachment
from max_client.models.emphasized_markup import EmphasizedMarkup
from max_client.models.error import Error
from max_client.models.file_attachment import FileAttachment
from max_client.models.file_attachment_payload import FileAttachmentPayload
from max_client.models.file_attachment_request import FileAttachmentRequest
from max_client.models.get_pinned_message_result import GetPinnedMessageResult
from max_client.models.get_subscriptions_result import GetSubscriptionsResult
from max_client.models.heading_markup import HeadingMarkup
from max_client.models.highlighted_markup import HighlightedMarkup
from max_client.models.image import Image
from max_client.models.inline_keyboard_attachment import InlineKeyboardAttachment
from max_client.models.inline_keyboard_attachment_request import InlineKeyboardAttachmentRequest
from max_client.models.inline_keyboard_attachment_request_payload import InlineKeyboardAttachmentRequestPayload
from max_client.models.intent import Intent
from max_client.models.keyboard import Keyboard
from max_client.models.link_button import LinkButton
from max_client.models.link_markup import LinkMarkup
from max_client.models.linked_message import LinkedMessage
from max_client.models.location_attachment import LocationAttachment
from max_client.models.location_attachment_request import LocationAttachmentRequest
from max_client.models.markup_element import MarkupElement
from max_client.models.media_attachment_payload import MediaAttachmentPayload
from max_client.models.message import Message
from max_client.models.message_body import MessageBody
from max_client.models.message_button import MessageButton
from max_client.models.message_callback_update import MessageCallbackUpdate
from max_client.models.message_chat_created_update import MessageChatCreatedUpdate
from max_client.models.message_created_update import MessageCreatedUpdate
from max_client.models.message_edited_update import MessageEditedUpdate
from max_client.models.message_link_type import MessageLinkType
from max_client.models.message_list import MessageList
from max_client.models.message_removed_update import MessageRemovedUpdate
from max_client.models.message_stat import MessageStat
from max_client.models.monospaced_markup import MonospacedMarkup
from max_client.models.new_message_body import NewMessageBody
from max_client.models.new_message_link import NewMessageLink
from max_client.models.photo_attachment import PhotoAttachment
from max_client.models.photo_attachment_payload import PhotoAttachmentPayload
from max_client.models.photo_attachment_request import PhotoAttachmentRequest
from max_client.models.photo_attachment_request_payload import PhotoAttachmentRequestPayload
from max_client.models.photo_token import PhotoToken
from max_client.models.photo_tokens import PhotoTokens
from max_client.models.pin_message_body import PinMessageBody
from max_client.models.recipient import Recipient
from max_client.models.reply_button import ReplyButton
from max_client.models.reply_keyboard_attachment import ReplyKeyboardAttachment
from max_client.models.reply_keyboard_attachment_request import ReplyKeyboardAttachmentRequest
from max_client.models.request_contact_button import RequestContactButton
from max_client.models.request_geo_location_button import RequestGeoLocationButton
from max_client.models.send_contact_button import SendContactButton
from max_client.models.send_geo_location_button import SendGeoLocationButton
from max_client.models.send_message_button import SendMessageButton
from max_client.models.send_message_result import SendMessageResult
from max_client.models.sender_action import SenderAction
from max_client.models.share_attachment import ShareAttachment
from max_client.models.share_attachment_payload import ShareAttachmentPayload
from max_client.models.share_attachment_request import ShareAttachmentRequest
from max_client.models.simple_query_result import SimpleQueryResult
from max_client.models.sticker_attachment import StickerAttachment
from max_client.models.sticker_attachment_payload import StickerAttachmentPayload
from max_client.models.sticker_attachment_request import StickerAttachmentRequest
from max_client.models.sticker_attachment_request_payload import StickerAttachmentRequestPayload
from max_client.models.strikethrough_markup import StrikethroughMarkup
from max_client.models.strong_markup import StrongMarkup
from max_client.models.subscription import Subscription
from max_client.models.subscription_request_body import SubscriptionRequestBody
from max_client.models.text_format import TextFormat
from max_client.models.underline_markup import UnderlineMarkup
from max_client.models.update import Update
from max_client.models.update_list import UpdateList
from max_client.models.upload_endpoint import UploadEndpoint
from max_client.models.upload_type import UploadType
from max_client.models.uploaded_info import UploadedInfo
from max_client.models.user import User
from max_client.models.user_added_to_chat_update import UserAddedToChatUpdate
from max_client.models.user_ids_list import UserIdsList
from max_client.models.user_mention_markup import UserMentionMarkup
from max_client.models.user_removed_from_chat_update import UserRemovedFromChatUpdate
from max_client.models.user_with_photo import UserWithPhoto
from max_client.models.video_attachment import VideoAttachment
from max_client.models.video_attachment_details import VideoAttachmentDetails
from max_client.models.video_attachment_request import VideoAttachmentRequest
from max_client.models.video_thumbnail import VideoThumbnail
from max_client.models.video_urls import VideoUrls

# coding: utf-8

# noinspection SpellCheckingInspection
"""
Max Bot API

# About Bot API allows bots to interact with Max. Methods are called by sending HTTPS requests to [botapi.max.ru](https://botapi.max.ru) domain. Bots are third-party applications that use Max features. A bot can legitimately take part in a conversation. It can be achieved through HTTP requests to the Max Bot API.  ## Features Max bots of the current version are able to: - Communicate with users and respond to requests - Recommend users complete actions via programmed buttons - Request personal data from users (name, short reference, phone number) We'll keep working on expanding bot capabilities in the future.  ## Examples Bots can be used for the following purposes: - Providing support, answering frequently asked questions - Sending typical information - Voting - Likes/dislikes - Following external links - Forwarding a user to a chat/channel  ## @MasterBot [MasterBot](https://max.ru/MasterBot) is the main bot in Max, all bots creator. Use MasterBot to create and edit your bots. Feel free to contact us for any questions, [@support](https://max.ru/support) or [help@max.ru](mailto:help@max.ru).  ## HTTP verbs `GET` &mdash; getting resources, parameters are transmitted via URL  `POST` &mdash; creation of resources (for example, sending new messages)  `PUT` &mdash; editing resources  `DELETE` &mdash; deleting resources  `PATCH` &mdash; patching resources  ## HTTP response codes `200` &mdash; successful operation  `400` &mdash; invalid request  `401` &mdash; authentication error  `404` &mdash; resource not found  `405` &mdash; method is not allowed  `429` &mdash; the number of requests is exceeded  `503` &mdash; service unavailable  ## Resources format For content requests (PUT and POST) and responses, the API uses the JSON format. All strings are UTF-8 encoded. Date/time fields are represented as the number of milliseconds that have elapsed since 00:00 January 1, 1970 in the long format. To get it, you can simply multiply the UNIX timestamp by 1000. All date/time fields have a UTC timezone. ## Error responses In case of an error, the API returns a response with the corresponding HTTP code and JSON with the following fields:  `code` - the string with the error key  `message` - a string describing the error </br>  For example: ```bash > http https://botapi.max.ru/chats?access_token={EXAMPLE_TOKEN} HTTP / 1.1 403 Forbidden Cache-Control: no-cache Connection: Keep-Alive Content-Length: 57 Content-Type: application / json; charset = utf-8 Set-Cookie: web_ui_lang = ru; Path = /; Domain = .max.ru; Expires = 2019-03-24T11: 45: 36.500Z {    \"code\": \"verify.token\",    \"message\": \"Invalid access_token\" } ``` ## Receiving notifications Max Bot API supports 2 options of receiving notifications on new events for bots: - Push notifications via WebHook. To receive data via WebHook, you'll have to [add subscription](https://dev.max.ru/#operation/subscribe); - Notifications upon request via [long polling](#operation/getUpdates) API. All data can be received via long polling **by default** after creating the bot.  Both methods **cannot** be used simultaneously. Refer to the response schema of [/updates](https://dev.max.ru/#operation/getUpdates) method to check all available types of updates.  ### Webhook There is some notes about how we handle webhook subscription: 1. Sometimes webhook notification cannot be delivered in case when bot server or network is down.    In such case we well retry delivery in a short period of time (from 30 to 60 seconds) and will do this until get   `200 OK` status code from your server, but not longer than **8 hours** (*may change over time*) since update happened.    We also consider any non `200`-response from server as failed delivery.  2. To protect your bot from unexpected high load we send **no more than 100** notifications per second by default.   If you want increase this limit, contact us at [@support](https://max.ru/support).   It should be from one of the following subnets: ``` 5.101.42.200/31 31.177.104.200/31 89.221.230.200/31 ```   ## Message buttons You can program buttons for users answering a bot. Max supports the following types of buttons:  `callback` &mdash; sends a notification with payload to a bot (via WebHook or long polling)  `link` &mdash; makes a user to follow a link  `request_contact` &mdash; requests the user permission to access contact information (phone number, short link, email)  `request_geo_location` &mdash; asks user to provide current geo location  `chat` &mdash; creates chat associated with message  To start create buttons [send message](#operation/sendMessage) with `InlineKeyboardAttachment`: ```json {   \"text\": \"It is message with inline keyboard\",   \"attachments\": [     {       \"type\": \"inline_keyboard\",       \"payload\": {         \"buttons\": [           [             {               \"type\": \"callback\",               \"text\": \"Press me!\",               \"payload\": \"button1 pressed\"             }           ],           [             {               \"type\": \"chat\",               \"text\": \"Discuss\",               \"chat_title\": \"Message discussion\"             }           ]         ]       }     }   ] } ``` ### Chat button Chat button is a button that starts chat assosiated with the current message. It will be **private** chat with a link, bot will be added as administrator by default.  Chat will be created as soon as the first user taps on button. Bot will receive `message_chat_created` update.  Bot can set title and description of new chat by setting `chat_title` and `chat_description` properties.  Whereas keyboard can contain several `chat`-buttons there is `uuid` property to distinct them between each other. In case you do not pass `uuid` we will generate it. If you edit message, pass `uuid` so we know that this button starts the same chat as before.  Chat button also can contain `start_payload` that will be sent to bot as part of `message_chat_created` update.  ## Deep linking Max supports deep linking mechanism for bots. It allows passing additional payload to the bot on startup. Deep link can contain any data encoded into string up to **128** characters long. Longer strings will be omitted and **not** passed to the bot.  Each bot has start link that looks like: ``` https://max.ru/%BOT_USERNAME%/start/%PAYLOAD% ``` As soon as user clicks on such link we open dialog with bot and send this payload to bot as part of `bot_started` update: ```json {     \"update_type\": \"bot_started\",     \"timestamp\": 1573226679188,     \"chat_id\": 1234567890,     \"user\": {         \"user_id\": 1234567890,         \"name\": \"Boris\",         \"username\": \"borisd84\"     },     \"payload\": \"any data meaningful to bot\" } ```  Deep linking mechanism is supported for iOS version 2.7.0 and Android 2.9.0 and higher.  ## Text formatting  Message text can be improved with basic formatting such as: **strong**, *emphasis*, ~strikethough~,  <ins>underline</ins>, `code` or link. You can use either markdown-like or HTML formatting.  To enable text formatting set the `format` property of [NewMessageBody](#tag/new_message_model).  ### Max flavored Markdown To enable [Markdown](https://spec.commonmark.org/0.29/) parsing, set the `format` property of [NewMessageBody](#tag/new_message_model) to `markdown`.  We currently support only the following syntax:  `*empasized*` or `_empasized_` for *italic* text  `**strong**` or `__strong__` for __bold__ text  `~~strikethough~~`  for ~strikethough~ text  `++underline++`  for <ins>underlined</ins> text  ``` `code` ``` or ` ```code``` ` for `monospaced` text  `^^important^^` for highlighted text (colored in red, by default)  `[Inline URL](https://dev.max.ru/)` for inline URLs  `[User mention](max://user/%user_id%)` for user mentions without username  `# Header` for header  ### HTML support  To enable HTML parsing, set the `format` property of [NewMessageBody](#tag/new_message_model) to `html`.  Only the following HTML tags are supported. All others will be stripped:  Emphasized: `<i>` or `<em>`  Strong: `<b>` or `<strong>`  Strikethrough: `<del>` or `<s>`  Underlined: `<ins>` or `<u>`  Link: `<a href=\"https://dev.max.ru\">Docs</a>`  Monospaced text: `<pre>` or `<code>`  Highlighted text: `<mark>`  Header: `<h1>`  Text formatting is supported for iOS since version 3.1 and Android since 2.20.0.  # Versioning API models and interface may change over time. To make sure your bot will get the right info, we strongly recommend adding API version number to each request. You can add it as `v` parameter to each HTTP-request. For instance, `v=0.1.2`. To specify the data model version you are getting through WebHook subscription, use the `version` property in the request body of the [subscribe](https://dev.max.ru/#operation/subscribe) request.  # Libraries We have developed the official [Java client](https://github.com/max-messenger/max-bot-api-client-java) and [SDK](https://github.com/max-messenger/max-bot-sdk-java).  # Changelog To see changelog for older versions visit our [GitHub](https://github.com/max-messenger/max-bot-api-schema/releases).  # noqa: E501

OpenAPI spec version: 0.0.10
"""

import pprint
import re  # noqa: F401
import sys

import six

from ..utl import OacUtils


# noinspection PyShadowingBuiltins
class MarkupElement(object):
    """NOTE:"""

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        "type": "str",
        "_from": "int",
        "length": "int",
    }

    attribute_map = {
        "type": "type",
        "_from": "from",
        "length": "length",
    }

    discriminator_value_class_map = {
        "heading": "HeadingMarkup",
        "strikethrough": "StrikethroughMarkup",
        "underline": "UnderlineMarkup",
        "link": "LinkMarkup",
        "emphasized": "EmphasizedMarkup",
        "strong": "StrongMarkup",
        "user_mention": "UserMentionMarkup",
        "highlighted": "HighlightedMarkup",
        "monospaced": "MonospacedMarkup",
    }

    def __init__(self, type=None, _from=None, length=None):  # noqa: E501
        """MarkupElement - a model defined in OpenAPI"""  # noqa: E501

        self._type = None
        self.__from = None
        self._length = None
        self.discriminator = "type"

        self.type = type
        self._from = _from
        self.length = length

        self._id_attrs = (self.type, self._from, self.length)

    @property
    def type(self):
        """Gets the type of this MarkupElement.  # noqa: E501

        Type of the markup element. Can be **strong**, *emphasized*, ~strikethrough~, ++underline++, `monospaced`, link or user_mention  # noqa: E501

        :return: The type of this MarkupElement.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this MarkupElement.

        Type of the markup element. Can be **strong**, *emphasized*, ~strikethrough~, ++underline++, `monospaced`, link or user_mention  # noqa: E501

        :param type: The type of this MarkupElement.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def _from(self):
        """Gets the _from of this MarkupElement.  # noqa: E501

        Element start index (zero-based) in text  # noqa: E501

        :return: The _from of this MarkupElement.  # noqa: E501
        :rtype: int
        """
        return self.__from

    @_from.setter
    def _from(self, _from):
        """Sets the _from of this MarkupElement.

        Element start index (zero-based) in text  # noqa: E501

        :param _from: The _from of this MarkupElement.  # noqa: E501
        :type: int
        """
        if _from is None:
            raise ValueError("Invalid value for `_from`, must not be `None`")  # noqa: E501

        self.__from = _from

    @property
    def length(self):
        """Gets the length of this MarkupElement.  # noqa: E501

        Length of the markup element  # noqa: E501

        :return: The length of this MarkupElement.  # noqa: E501
        :rtype: int
        """
        return self._length

    @length.setter
    def length(self, length):
        """Sets the length of this MarkupElement.

        Length of the markup element  # noqa: E501

        :param length: The length of this MarkupElement.  # noqa: E501
        :type: int
        """
        if length is None:
            raise ValueError("Invalid value for `length`, must not be `None`")  # noqa: E501

        self._length = length

    def markup_apply(self, text, format):
        # type: (str, TextFormat) -> str
        return text

    # noinspection PyProtectedMember
    @classmethod
    def get_markup_text(cls, text, markup):
        # type: (str, MarkupElement) -> str
        res = ""
        if text:
            if sys.maxunicode != 0xFFFF:
                try:
                    entity_text = text.encode("utf-16-le")
                    entity_text = entity_text[
                        markup._from * 2 : (markup._from + markup.length) * 2
                    ]
                    res = entity_text.decode("utf-16-le")
                except Exception as e:
                    print(e)
            if not res:
                res = text[markup._from : markup._from + markup.length]
        return res

    @classmethod
    def parse_markups(cls, text, markups, types=None):
        # type: (str, [MarkupElement], [str]) -> {MarkupElement, str}
        if types is None:
            types = MarkupElement.discriminator_value_class_map.keys()

        return {
            entity: cls.get_markup_text(text, entity)
            for entity in (markups or [])
            if entity.type in types
        }

    # noinspection PyProtectedMember,SpellCheckingInspection
    @classmethod
    def get_formated_markup_text(
        cls,
        message_text,
        markups,
        format,
        # urled: bool = False,
        _from=0,
    ):
        # type: (str, [MarkupElement], TextFormat, int) -> {MarkupElement, str}
        if message_text is None:
            return ""

        if sys.maxunicode != 0xFFFF:
            message_text = message_text.encode("utf-16-le")  # type: ignore

        formated_text = ""
        last__from = 0

        sorted_markups = sorted(markups.items(), key=(lambda item: item[0]._from))
        parsed_markups = []

        for markup, text in sorted_markups:
            assert isinstance(markup, MarkupElement)
            if markup not in parsed_markups:
                nested_markups = {
                    e: t
                    for (e, t) in sorted_markups
                    if (
                        e._from >= markup._from
                        and e._from + e.length <= markup._from + markup.length
                        and e != markup
                    )
                }
                parsed_markups.extend(list(nested_markups.keys()))

                orig_text = text
                text = OacUtils.escape(text)

                if nested_markups:
                    text = cls.get_formated_markup_text(
                        orig_text,
                        nested_markups,
                        format,
                        # urled=urled,
                        _from=markup._from,
                    )

                insert = markup.markup_apply(text, format)

                if _from == 0:
                    if sys.maxunicode == 0xFFFF:
                        formated_text += (
                            OacUtils.escape(
                                message_text[last__from : markup._from - _from]
                            )
                            + insert
                        )
                    else:
                        formated_text += (
                            OacUtils.escape(
                                message_text[
                                    last__from * 2 : (markup._from - _from) * 2
                                ].decode("utf-16-le")
                            )
                            + insert
                        )
                else:
                    if sys.maxunicode == 0xFFFF:
                        formated_text += (
                            message_text[last__from : markup._from - _from] + insert
                        )
                    else:
                        formated_text += (
                            message_text[
                                last__from * 2 : (markup._from - _from) * 2
                            ].decode("utf-16-le")
                            + insert
                        )

                last__from = markup._from - _from + markup.length

        if _from == 0:
            if sys.maxunicode == 0xFFFF:
                formated_text += OacUtils.escape(message_text[last__from:])
            else:
                formated_text += OacUtils.escape(
                    message_text[last__from * 2 :].decode("utf-16-le")  # type: ignore
                )
        else:
            if sys.maxunicode == 0xFFFF:
                formated_text += message_text[last__from:]
            else:
                formated_text += message_text[last__from * 2 :].decode("utf-16-le")  # type: ignore

        return formated_text

    def get_real_child_model(self, data):
        """Returns the real base class specified by the discriminator"""
        if self.discriminator:
            discriminator_value = data[self.discriminator]
            return self.discriminator_value_class_map.get(discriminator_value)

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (
                            (item[0], item[1].to_dict())
                            if hasattr(item[1], "to_dict")
                            else item
                        ),
                        value.items(),
                    )
                )
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, MarkupElement):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

    def __hash__(self):
        if self._id_attrs:
            return hash((self.__class__, self._id_attrs))
        return super().__hash__()

# coding: utf-8

"""
    Max Bot API

    # About Bot API allows bots to interact with Max. Methods are called by sending HTTPS requests to [botapi.max.ru](https://botapi.max.ru) domain. Bots are third-party applications that use Max features. A bot can legitimately take part in a conversation. It can be achieved through HTTP requests to the Max Bot API.  ## Features Max bots of the current version are able to: - Communicate with users and respond to requests - Recommend users complete actions via programmed buttons - Request personal data from users (name, short reference, phone number) We'll keep working on expanding bot capabilities in the future.  ## Examples Bots can be used for the following purposes: - Providing support, answering frequently asked questions - Sending typical information - Voting - Likes/dislikes - Following external links - Forwarding a user to a chat/channel  ## @MasterBot [MasterBot](https://max.ru/MasterBot) is the main bot in Max, all bots creator. Use MasterBot to create and edit your bots. Feel free to contact us for any questions, [@support](https://max.ru/support) or [help@max.ru](mailto:help@max.ru).  ## HTTP verbs `GET` &mdash; getting resources, parameters are transmitted via URL  `POST` &mdash; creation of resources (for example, sending new messages)  `PUT` &mdash; editing resources  `DELETE` &mdash; deleting resources  `PATCH` &mdash; patching resources  ## HTTP response codes `200` &mdash; successful operation  `400` &mdash; invalid request  `401` &mdash; authentication error  `404` &mdash; resource not found  `405` &mdash; method is not allowed  `429` &mdash; the number of requests is exceeded  `503` &mdash; service unavailable  ## Resources format For content requests (PUT and POST) and responses, the API uses the JSON format. All strings are UTF-8 encoded. Date/time fields are represented as the number of milliseconds that have elapsed since 00:00 January 1, 1970 in the long format. To get it, you can simply multiply the UNIX timestamp by 1000. All date/time fields have a UTC timezone. ## Error responses In case of an error, the API returns a response with the corresponding HTTP code and JSON with the following fields:  `code` - the string with the error key  `message` - a string describing the error </br>  For example: ```bash > http https://botapi.max.ru/chats?access_token={EXAMPLE_TOKEN} HTTP / 1.1 403 Forbidden Cache-Control: no-cache Connection: Keep-Alive Content-Length: 57 Content-Type: application / json; charset = utf-8 Set-Cookie: web_ui_lang = ru; Path = /; Domain = .max.ru; Expires = 2019-03-24T11: 45: 36.500Z {    \"code\": \"verify.token\",    \"message\": \"Invalid access_token\" } ``` ## Receiving notifications Max Bot API supports 2 options of receiving notifications on new events for bots: - Push notifications via WebHook. To receive data via WebHook, you'll have to [add subscription](https://dev.max.ru/#operation/subscribe); - Notifications upon request via [long polling](#operation/getUpdates) API. All data can be received via long polling **by default** after creating the bot.  Both methods **cannot** be used simultaneously. Refer to the response schema of [/updates](https://dev.max.ru/#operation/getUpdates) method to check all available types of updates.  ### Webhook There is some notes about how we handle webhook subscription: 1. Sometimes webhook notification cannot be delivered in case when bot server or network is down.    In such case we well retry delivery in a short period of time (from 30 to 60 seconds) and will do this until get   `200 OK` status code from your server, but not longer than **8 hours** (*may change over time*) since update happened.    We also consider any non `200`-response from server as failed delivery.  2. To protect your bot from unexpected high load we send **no more than 100** notifications per second by default.   If you want increase this limit, contact us at [@support](https://max.ru/support).   It should be from one of the following subnets: ``` 5.101.42.200/31 31.177.104.200/31 89.221.230.200/31 ```   ## Message buttons You can program buttons for users answering a bot. Max supports the following types of buttons:  `callback` &mdash; sends a notification with payload to a bot (via WebHook or long polling)  `link` &mdash; makes a user to follow a link  `request_contact` &mdash; requests the user permission to access contact information (phone number, short link, email)  `request_geo_location` &mdash; asks user to provide current geo location  `chat` &mdash; creates chat associated with message  To start create buttons [send message](#operation/sendMessage) with `InlineKeyboardAttachment`: ```json {   \"text\": \"It is message with inline keyboard\",   \"attachments\": [     {       \"type\": \"inline_keyboard\",       \"payload\": {         \"buttons\": [           [             {               \"type\": \"callback\",               \"text\": \"Press me!\",               \"payload\": \"button1 pressed\"             }           ],           [             {               \"type\": \"chat\",               \"text\": \"Discuss\",               \"chat_title\": \"Message discussion\"             }           ]         ]       }     }   ] } ``` ### Chat button Chat button is a button that starts chat assosiated with the current message. It will be **private** chat with a link, bot will be added as administrator by default.  Chat will be created as soon as the first user taps on button. Bot will receive `message_chat_created` update.  Bot can set title and description of new chat by setting `chat_title` and `chat_description` properties.  Whereas keyboard can contain several `chat`-buttons there is `uuid` property to distinct them between each other. In case you do not pass `uuid` we will generate it. If you edit message, pass `uuid` so we know that this button starts the same chat as before.  Chat button also can contain `start_payload` that will be sent to bot as part of `message_chat_created` update.  ## Deep linking Max supports deep linking mechanism for bots. It allows passing additional payload to the bot on startup. Deep link can contain any data encoded into string up to **128** characters long. Longer strings will be omitted and **not** passed to the bot.  Each bot has start link that looks like: ``` https://max.ru/%BOT_USERNAME%/start/%PAYLOAD% ``` As soon as user clicks on such link we open dialog with bot and send this payload to bot as part of `bot_started` update: ```json {     \"update_type\": \"bot_started\",     \"timestamp\": 1573226679188,     \"chat_id\": 1234567890,     \"user\": {         \"user_id\": 1234567890,         \"name\": \"Boris\",         \"username\": \"borisd84\"     },     \"payload\": \"any data meaningful to bot\" } ```  Deep linking mechanism is supported for iOS version 2.7.0 and Android 2.9.0 and higher.  ## Text formatting  Message text can be improved with basic formatting such as: **strong**, *emphasis*, ~strikethough~,  <ins>underline</ins>, `code` or link. You can use either markdown-like or HTML formatting.  To enable text formatting set the `format` property of [NewMessageBody](#tag/new_message_model).  ### Max flavored Markdown To enable [Markdown](https://spec.commonmark.org/0.29/) parsing, set the `format` property of [NewMessageBody](#tag/new_message_model) to `markdown`.  We currently support only the following syntax:  `*empasized*` or `_empasized_` for *italic* text  `**strong**` or `__strong__` for __bold__ text  `~~strikethough~~`  for ~strikethough~ text  `++underline++`  for <ins>underlined</ins> text  ``` `code` ``` or ` ```code``` ` for `monospaced` text  `^^important^^` for highlighted text (colored in red, by default)  `[Inline URL](https://dev.max.ru/)` for inline URLs  `[User mention](max://user/%user_id%)` for user mentions without username  `# Header` for header  ### HTML support  To enable HTML parsing, set the `format` property of [NewMessageBody](#tag/new_message_model) to `html`.  Only the following HTML tags are supported. All others will be stripped:  Emphasized: `<i>` or `<em>`  Strong: `<b>` or `<strong>`  Strikethrough: `<del>` or `<s>`  Underlined: `<ins>` or `<u>`  Link: `<a href=\"https://dev.max.ru\">Docs</a>`  Monospaced text: `<pre>` or `<code>`  Highlighted text: `<mark>`  Header: `<h1>`  Text formatting is supported for iOS since version 3.1 and Android since 2.20.0.  # Versioning API models and interface may change over time. To make sure your bot will get the right info, we strongly recommend adding API version number to each request. You can add it as `v` parameter to each HTTP-request. For instance, `v=0.1.2`. To specify the data model version you are getting through WebHook subscription, use the `version` property in the request body of the [subscribe](https://dev.max.ru/#operation/subscribe) request.  # Libraries We have developed the official [Java client](https://github.com/max-messenger/max-bot-api-client-java) and [SDK](https://github.com/max-messenger/max-bot-sdk-java).  # Changelog To see changelog for older versions visit our [GitHub](https://github.com/max-messenger/max-bot-api-schema/releases).  # noqa: E501

    OpenAPI spec version: 0.0.10
"""

import pprint
import re  # noqa: F401

import six

from .user_with_photo import UserWithPhoto


class ChatMember(UserWithPhoto):
    """NOTE: 
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'description': 'str',
        'user_id': 'int',
        'name': 'str',
        'username': 'str',
        'is_bot': 'bool',
        'last_activity_time': int,
        'avatar_url': 'str',
        'full_avatar_url': 'str',
        'last_access_time': 'int',
        'is_owner': 'bool',
        'is_admin': 'bool',
        'join_time': 'int',
        'permissions': 'list[ChatAdminPermission]',
        'alias': 'str'
    }

    attribute_map = {
        'description': 'description',
        'user_id': 'user_id',
        'name': 'name',
        'username': 'username',
        'is_bot': 'is_bot',
        'last_activity_time': 'last_activity_time',
        'avatar_url': 'avatar_url',
        'full_avatar_url': 'full_avatar_url',
        'last_access_time': 'last_access_time',
        'is_owner': 'is_owner',
        'is_admin': 'is_admin',
        'join_time': 'join_time',
        'permissions': 'permissions',
        'alias': 'alias'
    }

    def __init__(self, description=None, user_id=None, name=None, username=None, is_bot=None, last_activity_time=None, avatar_url=None, full_avatar_url=None, last_access_time=None, is_owner=None, is_admin=None, join_time=None,
                 permissions=None):  # noqa: E501
        """ChatMember - a model defined in OpenAPI"""  # noqa: E501

        super(ChatMember, self).__init__(description, user_id, name, username, is_bot, last_activity_time, avatar_url, full_avatar_url)
        self._last_access_time = None
        self._is_owner = None
        self._is_admin = None
        self._join_time = None
        self._permissions = None
        self._alias = None
        self.discriminator = None

        self.last_access_time = last_access_time
        self.is_owner = is_owner
        self.is_admin = is_admin
        self.join_time = join_time
        self.permissions = permissions
        self.alias = alias

    @property
    def last_access_time(self):
        """Gets the last_access_time of this ChatMember.  # noqa: E501

        User last activity time in chat. Can be outdated for super chats and channels (equals to `join_time`)  # noqa: E501

        :return: The last_access_time of this ChatMember.  # noqa: E501
        :rtype: int
        """
        return self._last_access_time

    @last_access_time.setter
    def last_access_time(self, last_access_time):
        """Sets the last_access_time of this ChatMember.

        User last activity time in chat. Can be outdated for super chats and channels (equals to `join_time`)  # noqa: E501

        :param last_access_time: The last_access_time of this ChatMember.  # noqa: E501
        :type: int
        """
        if last_access_time is None:
            raise ValueError("Invalid value for `last_access_time`, must not be `None`")  # noqa: E501

        self._last_access_time = last_access_time

    @property
    def is_owner(self):
        """Gets the is_owner of this ChatMember.  # noqa: E501


        :return: The is_owner of this ChatMember.  # noqa: E501
        :rtype: bool
        """
        return self._is_owner

    @is_owner.setter
    def is_owner(self, is_owner):
        """Sets the is_owner of this ChatMember.


        :param is_owner: The is_owner of this ChatMember.  # noqa: E501
        :type: bool
        """
        if is_owner is None:
            raise ValueError("Invalid value for `is_owner`, must not be `None`")  # noqa: E501

        self._is_owner = is_owner

    @property
    def is_admin(self):
        """Gets the is_admin of this ChatMember.  # noqa: E501


        :return: The is_admin of this ChatMember.  # noqa: E501
        :rtype: bool
        """
        return self._is_admin

    @is_admin.setter
    def is_admin(self, is_admin):
        """Sets the is_admin of this ChatMember.


        :param is_admin: The is_admin of this ChatMember.  # noqa: E501
        :type: bool
        """
        if is_admin is None:
            raise ValueError("Invalid value for `is_admin`, must not be `None`")  # noqa: E501

        self._is_admin = is_admin

    @property
    def join_time(self):
        """Gets the join_time of this ChatMember.  # noqa: E501


        :return: The join_time of this ChatMember.  # noqa: E501
        :rtype: int
        """
        return self._join_time

    @join_time.setter
    def join_time(self, join_time):
        """Sets the join_time of this ChatMember.


        :param join_time: The join_time of this ChatMember.  # noqa: E501
        :type: int
        """
        if join_time is None:
            raise ValueError("Invalid value for `join_time`, must not be `None`")  # noqa: E501

        self._join_time = join_time

    @property
    def permissions(self):
        """Gets the permissions of this ChatMember.  # noqa: E501

        Permissions in chat if member is admin. `null` otherwise  # noqa: E501

        :return: The permissions of this ChatMember.  # noqa: E501
        :rtype: list[ChatAdminPermission]
        """
        return self._permissions

    @permissions.setter
    def permissions(self, permissions):
        """Sets the permissions of this ChatMember.

        Permissions in chat if member is admin. `null` otherwise  # noqa: E501

        :param permissions: The permissions of this ChatMember.  # noqa: E501
        :type: list[ChatAdminPermission]
        """

        self._permissions = permissions

    @property
    def alias(self):
        """Gets the alias of this ChatMember.  # noqa: E501

        Alias in chat if member is admin. By default, `null`  # noqa: E501

        :return: The alias of this ChatMember.  # noqa: E501
        :rtype: str
        """
        return self._alias

    @alias.setter
    def alias(self, alias):
        """Sets the alias of this ChatMember.

        Alias in chat if member is admin. By default, `null`  # noqa: E501

        :param alias: The alias of this ChatMember.  # noqa: E501
        :type: str
        """
        if alias is None:
            raise ValueError("Invalid value for `alias`, must not be `None`")  # noqa: E501

        self._alias = alias

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
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
        if not isinstance(other, ChatMember):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

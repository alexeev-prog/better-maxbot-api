
r"""
Max Bot API.

# About Bot API allows bots to interact with Max. Methods are called by sending HTTPS requests to [botapi.max.ru](https://botapi.max.ru) domain. Bots are third-party applications that use Max features. A bot can legitimately take part in a conversation. It can be achieved through HTTP requests to the Max Bot API.  ## Features Max bots of the current version are able to: - Communicate with users and respond to requests - Recommend users complete actions via programmed buttons - Request personal data from users (name, short reference, phone number) We'll keep working on expanding bot capabilities in the future.  ## Examples Bots can be used for the following purposes: - Providing support, answering frequently asked questions - Sending typical information - Voting - Likes/dislikes - Following external links - Forwarding a user to a chat/channel  ## @MasterBot [MasterBot](https://max.ru/MasterBot) is the main bot in Max, all bots creator. Use MasterBot to create and edit your bots. Feel free to contact us for any questions, [@support](https://max.ru/support) or [help@max.ru](mailto:help@max.ru).  ## HTTP verbs `GET` &mdash; getting resources, parameters are transmitted via URL  `POST` &mdash; creation of resources (for example, sending new messages)  `PUT` &mdash; editing resources  `DELETE` &mdash; deleting resources  `PATCH` &mdash; patching resources  ## HTTP response codes `200` &mdash; successful operation  `400` &mdash; invalid request  `401` &mdash; authentication error  `404` &mdash; resource not found  `405` &mdash; method is not allowed  `429` &mdash; the number of requests is exceeded  `503` &mdash; service unavailable  ## Resources format For content requests (PUT and POST) and responses, the API uses the JSON format. All strings are UTF-8 encoded. Date/time fields are represented as the number of milliseconds that have elapsed since 00:00 January 1, 1970 in the long format. To get it, you can simply multiply the UNIX timestamp by 1000. All date/time fields have a UTC timezone. ## Error responses In case of an error, the API returns a response with the corresponding HTTP code and JSON with the following fields:  `code` - the string with the error key  `message` - a string describing the error </br>  For example: ```bash > http https://botapi.max.ru/chats?access_token={EXAMPLE_TOKEN} HTTP / 1.1 403 Forbidden Cache-Control: no-cache Connection: Keep-Alive Content-Length: 57 Content-Type: application / json; charset = utf-8 Set-Cookie: web_ui_lang = ru; Path = /; Domain = .max.ru; Expires = 2019-03-24T11: 45: 36.500Z {    \"code\": \"verify.token\",    \"message\": \"Invalid access_token\" } ``` ## Receiving notifications Max Bot API supports 2 options of receiving notifications on new events for bots: - Push notifications via WebHook. To receive data via WebHook, you'll have to [add subscription](https://dev.max.ru/#operation/subscribe); - Notifications upon request via [long polling](#operation/getUpdates) API. All data can be received via long polling **by default** after creating the bot.  Both methods **cannot** be used simultaneously. Refer to the response schema of [/updates](https://dev.max.ru/#operation/getUpdates) method to check all available types of updates.  ### Webhook There is some notes about how we handle webhook subscription: 1. Sometimes webhook notification cannot be delivered in case when bot server or network is down.    In such case we well retry delivery in a short period of time (from 30 to 60 seconds) and will do this until get   `200 OK` status code from your server, but not longer than **8 hours** (*may change over time*) since update happened.    We also consider any non `200`-response from server as failed delivery.  2. To protect your bot from unexpected high load we send **no more than 100** notifications per second by default.   If you want increase this limit, contact us at [@support](https://max.ru/support).   It should be from one of the following subnets: ``` 5.101.42.200/31 31.177.104.200/31 89.221.230.200/31 ```   ## Message buttons You can program buttons for users answering a bot. Max supports the following types of buttons:  `callback` &mdash; sends a notification with payload to a bot (via WebHook or long polling)  `link` &mdash; makes a user to follow a link  `request_contact` &mdash; requests the user permission to access contact information (phone number, short link, email)  `request_geo_location` &mdash; asks user to provide current geo location  `chat` &mdash; creates chat associated with message  To start create buttons [send message](#operation/sendMessage) with `InlineKeyboardAttachment`: ```json {   \"text\": \"It is message with inline keyboard\",   \"attachments\": [     {       \"type\": \"inline_keyboard\",       \"payload\": {         \"buttons\": [           [             {               \"type\": \"callback\",               \"text\": \"Press me!\",               \"payload\": \"button1 pressed\"             }           ],           [             {               \"type\": \"chat\",               \"text\": \"Discuss\",               \"chat_title\": \"Message discussion\"             }           ]         ]       }     }   ] } ``` ### Chat button Chat button is a button that starts chat assosiated with the current message. It will be **private** chat with a link, bot will be added as administrator by default.  Chat will be created as soon as the first user taps on button. Bot will receive `message_chat_created` update.  Bot can set title and description of new chat by setting `chat_title` and `chat_description` properties.  Whereas keyboard can contain several `chat`-buttons there is `uuid` property to distinct them between each other. In case you do not pass `uuid` we will generate it. If you edit message, pass `uuid` so we know that this button starts the same chat as before.  Chat button also can contain `start_payload` that will be sent to bot as part of `message_chat_created` update.  ## Deep linking Max supports deep linking mechanism for bots. It allows passing additional payload to the bot on startup. Deep link can contain any data encoded into string up to **128** characters long. Longer strings will be omitted and **not** passed to the bot.  Each bot has start link that looks like: ``` https://max.ru/%BOT_USERNAME%/start/%PAYLOAD% ``` As soon as user clicks on such link we open dialog with bot and send this payload to bot as part of `bot_started` update: ```json {     \"update_type\": \"bot_started\",     \"timestamp\": 1573226679188,     \"chat_id\": 1234567890,     \"user\": {         \"user_id\": 1234567890,         \"name\": \"Boris\",         \"username\": \"borisd84\"     },     \"payload\": \"any data meaningful to bot\" } ```  Deep linking mechanism is supported for iOS version 2.7.0 and Android 2.9.0 and higher.  ## Text formatting  Message text can be improved with basic formatting such as: **strong**, *emphasis*, ~strikethough~,  <ins>underline</ins>, `code` or link. You can use either markdown-like or HTML formatting.  To enable text formatting set the `format` property of [NewMessageBody](#tag/new_message_model).  ### Max flavored Markdown To enable [Markdown](https://spec.commonmark.org/0.29/) parsing, set the `format` property of [NewMessageBody](#tag/new_message_model) to `markdown`.  We currently support only the following syntax:  `*empasized*` or `_empasized_` for *italic* text  `**strong**` or `__strong__` for __bold__ text  `~~strikethough~~`  for ~strikethough~ text  `++underline++`  for <ins>underlined</ins> text  ``` `code` ``` or ` ```code``` ` for `monospaced` text  `^^important^^` for highlighted text (colored in red, by default)  `[Inline URL](https://dev.max.ru/)` for inline URLs  `[User mention](max://user/%user_id%)` for user mentions without username  `# Header` for header  ### HTML support  To enable HTML parsing, set the `format` property of [NewMessageBody](#tag/new_message_model) to `html`.  Only the following HTML tags are supported. All others will be stripped:  Emphasized: `<i>` or `<em>`  Strong: `<b>` or `<strong>`  Strikethrough: `<del>` or `<s>`  Underlined: `<ins>` or `<u>`  Link: `<a href=\"https://dev.max.ru\">Docs</a>`  Monospaced text: `<pre>` or `<code>`  Highlighted text: `<mark>`  Header: `<h1>`  Text formatting is supported for iOS since version 3.1 and Android since 2.20.0.  # Versioning API models and interface may change over time. To make sure your bot will get the right info, we strongly recommend adding API version number to each request. You can add it as `v` parameter to each HTTP-request. For instance, `v=0.1.2`. To specify the data model version you are getting through WebHook subscription, use the `version` property in the request body of the [subscribe](https://dev.max.ru/#operation/subscribe) request.  # Libraries We have developed the official [Java client](https://github.com/max-messenger/max-bot-api-client-java) and [SDK](https://github.com/max-messenger/max-bot-sdk-java).  # Changelog To see changelog for older versions visit our [GitHub](https://github.com/max-messenger/max-bot-api-schema/releases).  # noqa: E501

OpenAPI spec version: 0.0.10
"""


import re

# python 2 and python 3 compatibility library
import six

from max_client.api_client import ApiClient


class MessagesApi:
    """NOTE:"""

    MAX_MESSAGE_COUNT = 100

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def answer_on_callback(self, callback_id, callback_answer, **kwargs):
        """
        Answer on callback  # noqa: E501.

        This method should be called to send an answer after a user has clicked the button. The answer may be an updated message or/and a one-time user notification.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.answer_on_callback(
        ...     callback_id, callback_answer, async_req=True
        ... )
        >>> result = thread.get()

        :param async_req bool
        :param str callback_id: Identifies a button clicked by user. Bot receives this identifier after user pressed button as part of `MessageCallbackUpdate` (required)
        :param CallbackAnswer callback_answer: (required)
        :return: SimpleQueryResult
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        if kwargs.get("async_req"):
            return self.answer_on_callback_with_http_info(
                callback_id, callback_answer, **kwargs
            )
        return self.answer_on_callback_with_http_info(
            callback_id, callback_answer, **kwargs
        )

    def answer_on_callback_with_http_info(self, callback_id, callback_answer, **kwargs):
        """
        Answer on callback  # noqa: E501.

        This method should be called to send an answer after a user has clicked the button. The answer may be an updated message or/and a one-time user notification.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.answer_on_callback_with_http_info(
        ...     callback_id, callback_answer, async_req=True
        ... )
        >>> result = thread.get()

        :param async_req bool
        :param str callback_id: Identifies a button clicked by user. Bot receives this identifier after user pressed button as part of `MessageCallbackUpdate` (required)
        :param CallbackAnswer callback_answer: (required)
        :return: SimpleQueryResult
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()

        all_params = ["callback_id", "callback_answer"]
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise TypeError(
                    f"Got an unexpected keyword argument '{key}'"
                    " to method answer_on_callback"
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'callback_id' is set
        if (
            "callback_id" not in local_var_params
            or local_var_params["callback_id"] is None
        ):
            raise ValueError(
                "Missing the required parameter `callback_id` when calling `answer_on_callback`"
            )
        # verify the required parameter 'callback_answer' is set
        if (
            "callback_answer" not in local_var_params
            or local_var_params["callback_answer"] is None
        ):
            raise ValueError(
                "Missing the required parameter `callback_answer` when calling `answer_on_callback`"
            )

        if (
            "callback_id" in local_var_params
            and len(local_var_params["callback_id"]) < 1
        ):
            raise ValueError(
                "Invalid value for parameter `callback_id` when calling `answer_on_callback`, length must be greater than or equal to `1`"
            )
        if "callback_id" in local_var_params and not re.search(
            r"^(?!\\s*$).+", local_var_params["callback_id"]
        ):
            raise ValueError(
                "Invalid value for parameter `callback_id` when calling `answer_on_callback`, must conform to the pattern `/^(?!\\s*$).+/`"
            )
        collection_formats = {}

        path_params = {}

        query_params = []
        if "callback_id" in local_var_params:
            query_params.append(("callback_id", local_var_params["callback_id"]))

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "callback_answer" in local_var_params:
            body_params = local_var_params["callback_answer"]
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )

        # HTTP header `Content-Type`
        header_params["Content-Type"] = self.api_client.select_header_content_type(
            ["application/json"]
        )

        # Authentication setting
        auth_settings = ["access_token"]

        return self.api_client.call_api(
            "/answers",
            "POST",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="SimpleQueryResult",
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def construct(self, session_id, constructor_answer, **kwargs):
        """
        Construct message  # noqa: E501.

        Sends answer on construction request. Answer can contain any prepared message and/or keyboard to help user interact with bot.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.construct(session_id, constructor_answer, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str session_id: Constructor session identifier (required)
        :param ConstructorAnswer constructor_answer: (required)
        :return: SimpleQueryResult
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        if kwargs.get("async_req"):
            return self.construct_with_http_info(
                session_id, constructor_answer, **kwargs
            )
        return self.construct_with_http_info(
            session_id, constructor_answer, **kwargs
        )

    def construct_with_http_info(self, session_id, constructor_answer, **kwargs):
        """
        Construct message  # noqa: E501.

        Sends answer on construction request. Answer can contain any prepared message and/or keyboard to help user interact with bot.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.construct_with_http_info(
        ...     session_id, constructor_answer, async_req=True
        ... )
        >>> result = thread.get()

        :param async_req bool
        :param str session_id: Constructor session identifier (required)
        :param ConstructorAnswer constructor_answer: (required)
        :return: SimpleQueryResult
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()

        all_params = ["session_id", "constructor_answer"]
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise TypeError(
                    f"Got an unexpected keyword argument '{key}' to method construct"
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'session_id' is set
        if (
            "session_id" not in local_var_params
            or local_var_params["session_id"] is None
        ):
            raise ValueError(
                "Missing the required parameter `session_id` when calling `construct`"
            )
        # verify the required parameter 'constructor_answer' is set
        if (
            "constructor_answer" not in local_var_params
            or local_var_params["constructor_answer"] is None
        ):
            raise ValueError(
                "Missing the required parameter `constructor_answer` when calling `construct`"
            )

        collection_formats = {}

        path_params = {}

        query_params = []
        if "session_id" in local_var_params:
            query_params.append(("session_id", local_var_params["session_id"]))

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "constructor_answer" in local_var_params:
            body_params = local_var_params["constructor_answer"]
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )

        # HTTP header `Content-Type`
        header_params["Content-Type"] = self.api_client.select_header_content_type(
            ["application/json"]
        )

        # Authentication setting
        auth_settings = ["access_token"]

        return self.api_client.call_api(
            "/answers/constructor",
            "POST",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="SimpleQueryResult",
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def delete_message(self, message_id, **kwargs):
        """
        Delete message  # noqa: E501.

        Deletes message in a dialog or in a chat if bot has permission to delete messages.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_message(message_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str message_id: Deleting message identifier (required)
        :return: SimpleQueryResult
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        if kwargs.get("async_req"):
            return self.delete_message_with_http_info(message_id, **kwargs)
        return self.delete_message_with_http_info(message_id, **kwargs)

    def delete_message_with_http_info(self, message_id, **kwargs):
        """
        Delete message  # noqa: E501.

        Deletes message in a dialog or in a chat if bot has permission to delete messages.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_message_with_http_info(message_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str message_id: Deleting message identifier (required)
        :return: SimpleQueryResult
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()

        all_params = ["message_id"]
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise TypeError(
                    f"Got an unexpected keyword argument '{key}'"
                    " to method delete_message"
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'message_id' is set
        if (
            "message_id" not in local_var_params
            or local_var_params["message_id"] is None
        ):
            raise ValueError(
                "Missing the required parameter `message_id` when calling `delete_message`"
            )

        if "message_id" in local_var_params and len(local_var_params["message_id"]) < 1:
            raise ValueError(
                "Invalid value for parameter `message_id` when calling `delete_message`, length must be greater than or equal to `1`"
            )
        collection_formats = {}

        path_params = {}

        query_params = []
        if "message_id" in local_var_params:
            query_params.append(("message_id", local_var_params["message_id"]))

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )

        # Authentication setting
        auth_settings = ["access_token"]

        return self.api_client.call_api(
            "/messages",
            "DELETE",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="SimpleQueryResult",
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def edit_message(self, message_id, new_message_body, **kwargs):
        """
        Edit message  # noqa: E501.

        Updated message should be sent as `NewMessageBody` in a request body. In case `attachments` field is `null`, the current message attachments won’t be changed. In case of sending an empty list in this field, all attachments will be deleted.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.edit_message(message_id, new_message_body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str message_id: Editing message identifier (required)
        :param NewMessageBody new_message_body: (required)
        :return: SimpleQueryResult
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        if kwargs.get("async_req"):
            return self.edit_message_with_http_info(
                message_id, new_message_body, **kwargs
            )
        return self.edit_message_with_http_info(
            message_id, new_message_body, **kwargs
        )

    def edit_message_with_http_info(self, message_id, new_message_body, **kwargs):
        """
        Edit message  # noqa: E501.

        Updated message should be sent as `NewMessageBody` in a request body. In case `attachments` field is `null`, the current message attachments won’t be changed. In case of sending an empty list in this field, all attachments will be deleted.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.edit_message_with_http_info(
        ...     message_id, new_message_body, async_req=True
        ... )
        >>> result = thread.get()

        :param async_req bool
        :param str message_id: Editing message identifier (required)
        :param NewMessageBody new_message_body: (required)
        :return: SimpleQueryResult
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()

        all_params = ["message_id", "new_message_body"]
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise TypeError(
                    f"Got an unexpected keyword argument '{key}'"
                    " to method edit_message"
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'message_id' is set
        if (
            "message_id" not in local_var_params
            or local_var_params["message_id"] is None
        ):
            raise ValueError(
                "Missing the required parameter `message_id` when calling `edit_message`"
            )
        # verify the required parameter 'new_message_body' is set
        if (
            "new_message_body" not in local_var_params
            or local_var_params["new_message_body"] is None
        ):
            raise ValueError(
                "Missing the required parameter `new_message_body` when calling `edit_message`"
            )

        if "message_id" in local_var_params and len(local_var_params["message_id"]) < 1:
            raise ValueError(
                "Invalid value for parameter `message_id` when calling `edit_message`, length must be greater than or equal to `1`"
            )
        collection_formats = {}

        path_params = {}

        query_params = []
        if "message_id" in local_var_params:
            query_params.append(("message_id", local_var_params["message_id"]))

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "new_message_body" in local_var_params:
            body_params = local_var_params["new_message_body"]
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )

        # HTTP header `Content-Type`
        header_params["Content-Type"] = self.api_client.select_header_content_type(
            ["application/json"]
        )

        # Authentication setting
        auth_settings = ["access_token"]

        return self.api_client.call_api(
            "/messages",
            "PUT",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="SimpleQueryResult",
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def get_message_by_id(self, message_id, **kwargs):
        """
        Get message  # noqa: E501.

        Returns single message by its identifier.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_message_by_id(message_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str message_id: Message identifier (`mid`) to get single message in chat (required)
        :return: Message
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        if kwargs.get("async_req"):
            return self.get_message_by_id_with_http_info(message_id, **kwargs)
        return self.get_message_by_id_with_http_info(message_id, **kwargs)

    def get_message_by_id_with_http_info(self, message_id, **kwargs):
        """
        Get message  # noqa: E501.

        Returns single message by its identifier.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_message_by_id_with_http_info(message_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str message_id: Message identifier (`mid`) to get single message in chat (required)
        :return: Message
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()

        all_params = ["message_id"]
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise TypeError(
                    f"Got an unexpected keyword argument '{key}'"
                    " to method get_message_by_id"
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'message_id' is set
        if (
            "message_id" not in local_var_params
            or local_var_params["message_id"] is None
        ):
            raise ValueError(
                "Missing the required parameter `message_id` when calling `get_message_by_id`"
            )

        if "message_id" in local_var_params and not re.search(
            r"[a-zA-Z0-9_\\-]+", local_var_params["message_id"]
        ):
            raise ValueError(
                "Invalid value for parameter `message_id` when calling `get_message_by_id`, must conform to the pattern `/[a-zA-Z0-9_\\-]+/`"
            )
        collection_formats = {}

        path_params = {}
        if "message_id" in local_var_params:
            path_params["messageId"] = local_var_params["message_id"]

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )

        # Authentication setting
        auth_settings = ["access_token"]

        return self.api_client.call_api(
            "/messages/{messageId}",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="Message",
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def get_messages(self, **kwargs):
        """
        Get messages  # noqa: E501.

        Returns messages in chat: result page and marker referencing to the next page. Messages traversed in reverse direction so the latest message in chat will be first in result array. Therefore if you use `from` and `to` parameters, `to` must be **less than** `from`  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_messages(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int chat_id: Chat identifier to get messages in chat
        :param list[str] message_ids: Comma-separated list of message ids to get
        :param int _from: Start time for requested messages
        :param int to: End time for requested messages
        :param int count: Maximum amount of messages in response
        :return: MessageList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        if kwargs.get("async_req"):
            return self.get_messages_with_http_info(**kwargs)
        return self.get_messages_with_http_info(**kwargs)

    def get_messages_with_http_info(self, **kwargs):
        """
        Get messages  # noqa: E501.

        Returns messages in chat: result page and marker referencing to the next page. Messages traversed in reverse direction so the latest message in chat will be first in result array. Therefore if you use `from` and `to` parameters, `to` must be **less than** `from`  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_messages_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int chat_id: Chat identifier to get messages in chat
        :param list[str] message_ids: Comma-separated list of message ids to get
        :param int _from: Start time for requested messages
        :param int to: End time for requested messages
        :param int count: Maximum amount of messages in response
        :return: MessageList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()

        all_params = ["chat_id", "message_ids", "_from", "to", "count"]
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise TypeError(
                    f"Got an unexpected keyword argument '{key}'"
                    " to method get_messages"
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]

        if (
            "count" in local_var_params
            and local_var_params["count"] > self.MAX_MESSAGE_COUNT
        ):
            raise ValueError(
                f"Invalid value for parameter `count` when calling `get_messages`, must be a value less than or equal to `{self.MAX_MESSAGE_COUNT}`"
            )
        if "count" in local_var_params and local_var_params["count"] < 1:
            raise ValueError(
                "Invalid value for parameter `count` when calling `get_messages`, must be a value greater than or equal to `1`"
            )
        collection_formats = {}

        path_params = {}

        query_params = []
        if "chat_id" in local_var_params:
            query_params.append(("chat_id", local_var_params["chat_id"]))
        if "message_ids" in local_var_params:
            query_params.append(("message_ids", local_var_params["message_ids"]))
            collection_formats["message_ids"] = "csv"
        if "_from" in local_var_params:
            query_params.append(("from", local_var_params["_from"]))
        if "to" in local_var_params:
            query_params.append(("to", local_var_params["to"]))
        if "count" in local_var_params:
            query_params.append(("count", local_var_params["count"]))

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )

        # Authentication setting
        auth_settings = ["access_token"]

        return self.api_client.call_api(
            "/messages",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="MessageList",
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def send_message(self, new_message_body, **kwargs):
        """
        Send message  # noqa: E501.

        Sends a message to a chat. As a result for this method new message identifier returns.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.send_message(new_message_body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param NewMessageBody new_message_body: (required)
        :param int user_id: Fill this parameter if you want to send message to user
        :param int chat_id: Fill this if you send message to chat
        :param bool disable_link_preview: If `false`, server will not generate media preview for links in text
        :return: SendMessageResult
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        if kwargs.get("async_req"):
            return self.send_message_with_http_info(new_message_body, **kwargs)
        return self.send_message_with_http_info(new_message_body, **kwargs)

    def send_message_with_http_info(self, new_message_body, **kwargs):
        """
        Send message  # noqa: E501.

        Sends a message to a chat. As a result for this method new message identifier returns.
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.send_message_with_http_info(new_message_body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param NewMessageBody new_message_body: (required)
        :param int user_id: Fill this parameter if you want to send message to user
        :param int chat_id: Fill this if you send message to chat
        :param bool disable_link_preview: If `false`, server will not generate media preview for links in text
        :return: SendMessageResult
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()

        all_params = [
            "new_message_body",
            "user_id",
            "chat_id",
            "disable_link_preview",
        ]
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise TypeError(
                    f"Got an unexpected keyword argument '{key}'"
                    " to method send_message"
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'new_message_body' is set
        if (
            "new_message_body" not in local_var_params
            or local_var_params["new_message_body"] is None
        ):
            raise ValueError(
                "Missing the required parameter `new_message_body` when calling `send_message`"
            )

        collection_formats = {}

        path_params = {}

        query_params = []
        if "user_id" in local_var_params:
            query_params.append(("user_id", local_var_params["user_id"]))
        if "chat_id" in local_var_params:
            query_params.append(("chat_id", local_var_params["chat_id"]))
        if "disable_link_preview" in local_var_params:
            query_params.append(
                ("disable_link_preview", local_var_params["disable_link_preview"])
            )

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "new_message_body" in local_var_params:
            body_params = local_var_params["new_message_body"]
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )

        # HTTP header `Content-Type`
        header_params["Content-Type"] = self.api_client.select_header_content_type(
            ["application/json"]
        )

        # Authentication setting
        auth_settings = ["access_token"]

        return self.api_client.call_api(
            "/messages",
            "POST",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="SendMessageResult",
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

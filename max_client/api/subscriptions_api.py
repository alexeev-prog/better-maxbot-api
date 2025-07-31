
r"""
Max Bot API.

# About Bot API allows bots to interact with Max. Methods are called by sending HTTPS requests to [botapi.max.ru](https://botapi.max.ru) domain. Bots are third-party applications that use Max features. A bot can legitimately take part in a conversation. It can be achieved through HTTP requests to the Max Bot API.  ## Features Max bots of the current version are able to: - Communicate with users and respond to requests - Recommend users complete actions via programmed buttons - Request personal data from users (name, short reference, phone number) We'll keep working on expanding bot capabilities in the future.  ## Examples Bots can be used for the following purposes: - Providing support, answering frequently asked questions - Sending typical information - Voting - Likes/dislikes - Following external links - Forwarding a user to a chat/channel  ## @MasterBot [MasterBot](https://max.ru/MasterBot) is the main bot in Max, all bots creator. Use MasterBot to create and edit your bots. Feel free to contact us for any questions, [@support](https://max.ru/support) or [help@max.ru](mailto:help@max.ru).  ## HTTP verbs `GET` &mdash; getting resources, parameters are transmitted via URL  `POST` &mdash; creation of resources (for example, sending new messages)  `PUT` &mdash; editing resources  `DELETE` &mdash; deleting resources  `PATCH` &mdash; patching resources  ## HTTP response codes `200` &mdash; successful operation  `400` &mdash; invalid request  `401` &mdash; authentication error  `404` &mdash; resource not found  `405` &mdash; method is not allowed  `429` &mdash; the number of requests is exceeded  `503` &mdash; service unavailable  ## Resources format For content requests (PUT and POST) and responses, the API uses the JSON format. All strings are UTF-8 encoded. Date/time fields are represented as the number of milliseconds that have elapsed since 00:00 January 1, 1970 in the long format. To get it, you can simply multiply the UNIX timestamp by 1000. All date/time fields have a UTC timezone. ## Error responses In case of an error, the API returns a response with the corresponding HTTP code and JSON with the following fields:  `code` - the string with the error key  `message` - a string describing the error </br>  For example: ```bash > http https://botapi.max.ru/chats?access_token={EXAMPLE_TOKEN} HTTP / 1.1 403 Forbidden Cache-Control: no-cache Connection: Keep-Alive Content-Length: 57 Content-Type: application / json; charset = utf-8 Set-Cookie: web_ui_lang = ru; Path = /; Domain = .max.ru; Expires = 2019-03-24T11: 45: 36.500Z {    \"code\": \"verify.token\",    \"message\": \"Invalid access_token\" } ``` ## Receiving notifications Max Bot API supports 2 options of receiving notifications on new events for bots: - Push notifications via WebHook. To receive data via WebHook, you'll have to [add subscription](https://dev.max.ru/#operation/subscribe); - Notifications upon request via [long polling](#operation/getUpdates) API. All data can be received via long polling **by default** after creating the bot.  Both methods **cannot** be used simultaneously. Refer to the response schema of [/updates](https://dev.max.ru/#operation/getUpdates) method to check all available types of updates.  ### Webhook There is some notes about how we handle webhook subscription: 1. Sometimes webhook notification cannot be delivered in case when bot server or network is down.    In such case we well retry delivery in a short period of time (from 30 to 60 seconds) and will do this until get   `200 OK` status code from your server, but not longer than **8 hours** (*may change over time*) since update happened.    We also consider any non `200`-response from server as failed delivery.  2. To protect your bot from unexpected high load we send **no more than 100** notifications per second by default.   If you want increase this limit, contact us at [@support](https://max.ru/support).   It should be from one of the following subnets: ``` 5.101.42.200/31 31.177.104.200/31 89.221.230.200/31 ```   ## Message buttons You can program buttons for users answering a bot. Max supports the following types of buttons:  `callback` &mdash; sends a notification with payload to a bot (via WebHook or long polling)  `link` &mdash; makes a user to follow a link  `request_contact` &mdash; requests the user permission to access contact information (phone number, short link, email)  `request_geo_location` &mdash; asks user to provide current geo location  `chat` &mdash; creates chat associated with message  To start create buttons [send message](#operation/sendMessage) with `InlineKeyboardAttachment`: ```json {   \"text\": \"It is message with inline keyboard\",   \"attachments\": [     {       \"type\": \"inline_keyboard\",       \"payload\": {         \"buttons\": [           [             {               \"type\": \"callback\",               \"text\": \"Press me!\",               \"payload\": \"button1 pressed\"             }           ],           [             {               \"type\": \"chat\",               \"text\": \"Discuss\",               \"chat_title\": \"Message discussion\"             }           ]         ]       }     }   ] } ``` ### Chat button Chat button is a button that starts chat assosiated with the current message. It will be **private** chat with a link, bot will be added as administrator by default.  Chat will be created as soon as the first user taps on button. Bot will receive `message_chat_created` update.  Bot can set title and description of new chat by setting `chat_title` and `chat_description` properties.  Whereas keyboard can contain several `chat`-buttons there is `uuid` property to distinct them between each other. In case you do not pass `uuid` we will generate it. If you edit message, pass `uuid` so we know that this button starts the same chat as before.  Chat button also can contain `start_payload` that will be sent to bot as part of `message_chat_created` update.  ## Deep linking Max supports deep linking mechanism for bots. It allows passing additional payload to the bot on startup. Deep link can contain any data encoded into string up to **128** characters long. Longer strings will be omitted and **not** passed to the bot.  Each bot has start link that looks like: ``` https://max.ru/%BOT_USERNAME%/start/%PAYLOAD% ``` As soon as user clicks on such link we open dialog with bot and send this payload to bot as part of `bot_started` update: ```json {     \"update_type\": \"bot_started\",     \"timestamp\": 1573226679188,     \"chat_id\": 1234567890,     \"user\": {         \"user_id\": 1234567890,         \"name\": \"Boris\",         \"username\": \"borisd84\"     },     \"payload\": \"any data meaningful to bot\" } ```  Deep linking mechanism is supported for iOS version 2.7.0 and Android 2.9.0 and higher.  ## Text formatting  Message text can be improved with basic formatting such as: **strong**, *emphasis*, ~strikethough~,  <ins>underline</ins>, `code` or link. You can use either markdown-like or HTML formatting.  To enable text formatting set the `format` property of [NewMessageBody](#tag/new_message_model).  ### Max flavored Markdown To enable [Markdown](https://spec.commonmark.org/0.29/) parsing, set the `format` property of [NewMessageBody](#tag/new_message_model) to `markdown`.  We currently support only the following syntax:  `*empasized*` or `_empasized_` for *italic* text  `**strong**` or `__strong__` for __bold__ text  `~~strikethough~~`  for ~strikethough~ text  `++underline++`  for <ins>underlined</ins> text  ``` `code` ``` or ` ```code``` ` for `monospaced` text  `^^important^^` for highlighted text (colored in red, by default)  `[Inline URL](https://dev.max.ru/)` for inline URLs  `[User mention](max://user/%user_id%)` for user mentions without username  `# Header` for header  ### HTML support  To enable HTML parsing, set the `format` property of [NewMessageBody](#tag/new_message_model) to `html`.  Only the following HTML tags are supported. All others will be stripped:  Emphasized: `<i>` or `<em>`  Strong: `<b>` or `<strong>`  Strikethrough: `<del>` or `<s>`  Underlined: `<ins>` or `<u>`  Link: `<a href=\"https://dev.max.ru\">Docs</a>`  Monospaced text: `<pre>` or `<code>`  Highlighted text: `<mark>`  Header: `<h1>`  Text formatting is supported for iOS since version 3.1 and Android since 2.20.0.  # Versioning API models and interface may change over time. To make sure your bot will get the right info, we strongly recommend adding API version number to each request. You can add it as `v` parameter to each HTTP-request. For instance, `v=0.1.2`. To specify the data model version you are getting through WebHook subscription, use the `version` property in the request body of the [subscribe](https://dev.max.ru/#operation/subscribe) request.  # Libraries We have developed the official [Java client](https://github.com/max-messenger/max-bot-api-client-java) and [SDK](https://github.com/max-messenger/max-bot-sdk-java).  # Changelog To see changelog for older versions visit our [GitHub](https://github.com/max-messenger/max-bot-api-schema/releases).  # noqa: E501

OpenAPI spec version: 0.0.10
"""


import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from max_client.api_client import ApiClient


class SubscriptionsApi:
    """NOTE:"""

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_subscriptions(self, **kwargs):
        """
        Get subscriptions  # noqa: E501.

        In case your bot gets data via WebHook, the method returns list of all subscriptions  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_subscriptions(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: GetSubscriptionsResult
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        if kwargs.get("async_req"):
            return self.get_subscriptions_with_http_info(**kwargs)
        return self.get_subscriptions_with_http_info(**kwargs)

    def get_subscriptions_with_http_info(self, **kwargs):
        """
        Get subscriptions  # noqa: E501.

        In case your bot gets data via WebHook, the method returns list of all subscriptions  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_subscriptions_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :return: GetSubscriptionsResult
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()

        all_params = []
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise TypeError(
                    f"Got an unexpected keyword argument '{key}'"
                    " to method get_subscriptions"
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]

        collection_formats = {}

        path_params = {}

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
            "/subscriptions",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="GetSubscriptionsResult",
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def get_updates(self, **kwargs):
        """
        Get updates  # noqa: E501.

        You can use this method for getting updates in case your bot is not subscribed to WebHook. The method is based on long polling.  Every update has its own sequence number. `marker` property in response points to the next upcoming update.  All previous updates are considered as *committed* after passing `marker` parameter. If `marker` parameter is **not passed**, your bot will get all updates happened after the last commitment.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_updates(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int limit: Maximum number of updates to be retrieved
        :param int timeout: Timeout in seconds for long polling
        :param int marker: Pass `null` to get updates you didn't get yet
        :param list[str] types: Comma separated list of update types your bot want to receive
        :return: UpdateList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        if kwargs.get("async_req"):
            return self.get_updates_with_http_info(**kwargs)
        return self.get_updates_with_http_info(**kwargs)

    def get_updates_with_http_info(self, **kwargs):
        """
        Get updates  # noqa: E501.

        You can use this method for getting updates in case your bot is not subscribed to WebHook. The method is based on long polling.  Every update has its own sequence number. `marker` property in response points to the next upcoming update.  All previous updates are considered as *committed* after passing `marker` parameter. If `marker` parameter is **not passed**, your bot will get all updates happened after the last commitment.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_updates_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param int limit: Maximum number of updates to be retrieved
        :param int timeout: Timeout in seconds for long polling
        :param int marker: Pass `null` to get updates you didn't get yet
        :param list[str] types: Comma separated list of update types your bot want to receive
        :return: UpdateList
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()

        all_params = ["limit", "timeout", "marker", "types"]
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise TypeError(
                    f"Got an unexpected keyword argument '{key}'"
                    " to method get_updates"
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]

        if "limit" in local_var_params and local_var_params["limit"] > 1000:
            raise ValueError(
                "Invalid value for parameter `limit` when calling `get_updates`, must be a value less than or equal to `1000`"
            )
        if "limit" in local_var_params and local_var_params["limit"] < 1:
            raise ValueError(
                "Invalid value for parameter `limit` when calling `get_updates`, must be a value greater than or equal to `1`"
            )
        if "timeout" in local_var_params and local_var_params["timeout"] > 90:
            raise ValueError(
                "Invalid value for parameter `timeout` when calling `get_updates`, must be a value less than or equal to `90`"
            )
        if "timeout" in local_var_params and local_var_params["timeout"] < 0:
            raise ValueError(
                "Invalid value for parameter `timeout` when calling `get_updates`, must be a value greater than or equal to `0`"
            )
        collection_formats = {}

        path_params = {}

        query_params = []
        if "limit" in local_var_params:
            query_params.append(("limit", local_var_params["limit"]))
        if "timeout" in local_var_params:
            query_params.append(("timeout", local_var_params["timeout"]))
        if "marker" in local_var_params:
            query_params.append(("marker", local_var_params["marker"]))
        if "types" in local_var_params:
            query_params.append(("types", local_var_params["types"]))
            collection_formats["types"] = "csv"

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
            "/updates",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="UpdateList",
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def subscribe(self, subscription_request_body, **kwargs):
        """
        Subscribe  # noqa: E501.

        Subscribes bot to receive updates via WebHook. After calling this method, the bot will receive notifications about new events in chat rooms at the specified URL.  Your server **must** be listening on one of the following ports: **80, 8080, 443, 8443, 16384-32383**  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.subscribe(subscription_request_body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param SubscriptionRequestBody subscription_request_body: (required)
        :return: SimpleQueryResult
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        if kwargs.get("async_req"):
            return self.subscribe_with_http_info(subscription_request_body, **kwargs)
        return self.subscribe_with_http_info(subscription_request_body, **kwargs)

    def subscribe_with_http_info(self, subscription_request_body, **kwargs):
        """
        Subscribe  # noqa: E501.

        Subscribes bot to receive updates via WebHook. After calling this method, the bot will receive notifications about new events in chat rooms at the specified URL.  Your server **must** be listening on one of the following ports: **80, 8080, 443, 8443, 16384-32383**  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.subscribe_with_http_info(
        ...     subscription_request_body, async_req=True
        ... )
        >>> result = thread.get()

        :param async_req bool
        :param SubscriptionRequestBody subscription_request_body: (required)
        :return: SimpleQueryResult
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()

        all_params = ["subscription_request_body"]
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise TypeError(
                    f"Got an unexpected keyword argument '{key}' to method subscribe"
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'subscription_request_body' is set
        if (
            "subscription_request_body" not in local_var_params
            or local_var_params["subscription_request_body"] is None
        ):
            raise ValueError(
                "Missing the required parameter `subscription_request_body` when calling `subscribe`"
            )

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "subscription_request_body" in local_var_params:
            body_params = local_var_params["subscription_request_body"]
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
            "/subscriptions",
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

    def unsubscribe(self, url, **kwargs):
        """
        Unsubscribe  # noqa: E501.

        Unsubscribes bot from receiving updates via WebHook. After calling the method, the bot stops receiving notifications about new events. Notification via the long-poll API becomes available for the bot  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.unsubscribe(url, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str url: URL to remove from WebHook subscriptions (required)
        :return: SimpleQueryResult
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        if kwargs.get("async_req"):
            return self.unsubscribe_with_http_info(url, **kwargs)
        return self.unsubscribe_with_http_info(url, **kwargs)

    def unsubscribe_with_http_info(self, url, **kwargs):
        """
        Unsubscribe  # noqa: E501.

        Unsubscribes bot from receiving updates via WebHook. After calling the method, the bot stops receiving notifications about new events. Notification via the long-poll API becomes available for the bot  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.unsubscribe_with_http_info(url, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str url: URL to remove from WebHook subscriptions (required)
        :return: SimpleQueryResult
                 If the method is called asynchronously,
                 returns the request thread.
        """
        local_var_params = locals()

        all_params = ["url"]
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise TypeError(
                    f"Got an unexpected keyword argument '{key}'"
                    " to method unsubscribe"
                )
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'url' is set
        if "url" not in local_var_params or local_var_params["url"] is None:
            raise ValueError(
                "Missing the required parameter `url` when calling `unsubscribe`"
            )

        collection_formats = {}

        path_params = {}

        query_params = []
        if "url" in local_var_params:
            query_params.append(("url", local_var_params["url"]))

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
            "/subscriptions",
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

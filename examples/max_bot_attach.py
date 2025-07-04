# -*- coding: UTF-8 -*-
import json
import math
import os
import re
import sys
import traceback
from datetime import datetime, timedelta
from threading import Thread
from time import sleep

import requests
import six
import urllib3
from max_chat import ChatExt
from max_commander import UpdateCmn
from max_repiter import ChatActionRequestRepeater

from max_client import (
    ActionRequestBody,
    ApiClient,
    AudioAttachmentRequest,
    BotAddedToChatUpdate,
    BotCommand,
    BotInfo,
    BotPatch,
    BotRemovedFromChatUpdate,
    BotsApi,
    BotStartedUpdate,
    CallbackAnswer,
    Chat,
    ChatAdminPermission,
    ChatList,
    ChatMember,
    ChatMembersList,
    ChatsApi,
    ChatStatus,
    ChatTitleChangedUpdate,
    ChatType,
    Configuration,
    FileAttachmentRequest,
    GetSubscriptionsResult,
    InlineKeyboardAttachment,
    InlineKeyboardAttachmentRequest,
    InlineKeyboardAttachmentRequestPayload,
    Intent,
    LinkButton,
    LinkedMessage,
    Message,
    MessageBody,
    MessageCallbackUpdate,
    MessageChatCreatedUpdate,
    MessageCreatedUpdate,
    MessageEditedUpdate,
    MessageLinkType,
    MessageList,
    MessageRemovedUpdate,
    MessagesApi,
    NewMessageBody,
    NewMessageLink,
    PhotoAttachmentRequest,
    RequestContactButton,
    RequestGeoLocationButton,
    SenderAction,
    SendMessageResult,
    SimpleQueryResult,
    Subscription,
    SubscriptionRequestBody,
    SubscriptionsApi,
    TextFormat,
    Update,
    UploadApi,
    UploadEndpoint,
    UploadType,
    UserAddedToChatUpdate,
    UserRemovedFromChatUpdate,
    UserWithPhoto,
    VideoAttachmentRequest,
)
from max_client.cmn import BotLogger, Utils
from max_client.rest import ApiException, RESTResponse
from max_client.utl import OacUtils


class MaxBotException(Exception):
    pass


# noinspection SqlNoDataSourceInspection,SqlDialectInspection,GrazieInspection
class MaxBot(object):
    _work_threads_max_count = None
    threads = []
    chats_action = {}
    callbacks_list = {}

    limited_buttons = {}

    SERVICE_STR_SEQUENCE = chr(8203) + chr(8203) + chr(8203)

    last_mcb_update = {}

    lgz = BotLogger.get_instance()

    def __init__(self):
        # Общие настройки - логирование, кодировка и т.п.

        self.waiting_msg = False  # Выводить вейтерное сообщение

        self.set_encoding_for_p2()

        # Собственные настройки бота
        self.conf = Configuration()
        self.conf.api_key["access_token"] = self.token

        self.trace_requests = self.lgz.trace_requests

        self.polling_sleep_time = 5
        self.polling_error_sleep_time = 5

        self.client = ApiClient(self.conf)

        self.subscriptions = SubscriptionsApi(self.client)
        self.msg = MessagesApi(self.client)
        self.api = BotsApi(self.client)
        self.chats = ChatsApi(self.client)
        self.upload = UploadApi(self.client)

        self._languages_dict = None
        self._admins_contacts = None

        try:
            self.info = self.api.get_my_info()
            try:
                bp = BotPatch(commands=self.commands, description=self.description)
                self.info = self.api.edit_my_info(bp)
            except ApiException:
                self.lgz.exception("ApiException")
        except ApiException:
            self.lgz.exception("ApiException")
            self.info = None
        if isinstance(self.info, BotInfo):
            self.user_id = self.info.user_id
            self.first_name = self.info.first_name
            self.name = self.info.name
            self.last_name = self.info.last_name
            self.username = self.info.username
            self.title = self.first_name
        else:
            self.user_id = None
            self.first_name = None
            self.last_name = None
            self.name = None
            self.username = None
            self.title = None

        self.stop_polling = False

        self.lgz.info("%s inited." % self.title)

    @property
    def about(self):
        # type: () -> str
        self.lgz.warning("The default about string is used. Maybe is error?")
        return _(
            "This is the coolest bot in the world, but so far can not do anything. To open the menu, type /menu."
        )

    @property
    def main_menu_title(self):
        # type: () -> str
        return _("Abilities:")

    @property
    def main_menu_buttons(self):
        # type: () -> []
        self.lgz.warning("The default main menu buttons is used. Maybe is error?")
        buttons = [
            [
                LinkButton(
                    _("API documentation for Max-bots"), "https://dev.max.ru/docs"
                )
            ],
            [
                LinkButton(
                    _("JSON Diagram API Max Bots"),
                    "https://github.com/max-messenger/max-bot-api-schema",
                )
            ],
            [RequestContactButton(_("Report your contact details"))],
            [RequestGeoLocationButton(_("Report your location"), True)],
        ]

        return buttons

    @property
    def token(self):
        # type: () -> str
        raise NotImplementedError

    @property
    def description(self):
        # type: () -> str
        raise NotImplementedError

    def get_commands(self):
        # type: () -> [BotCommand]
        self.lgz.warning("The default command list is used. Maybe is error?")
        commands = [
            BotCommand("start_test", "начать"),
            BotCommand("menu", "показать меню"),
            BotCommand("list", "список всех чатов"),
        ]
        return commands

    @property
    def trace_requests(self):
        # type: () -> bool
        return self.conf.debug

    @trace_requests.setter
    def trace_requests(self, val):
        self.conf.debug = val

    def set_encoding_for_p2(self, encoding="utf8"):
        if six.PY3:
            return
        else:
            # noinspection PyCompatibility,PyUnresolvedReferences
            reload(sys)
            # noinspection PyUnresolvedReferences
            sys.setdefaultencoding(encoding)
            self.lgz.info(
                "The default encoding is set to %s" % sys.getdefaultencoding()
            )

    def check_threads(self):
        self.lgz.info(
            "%s of %s threads are used."
            % (len(MaxBot.threads), MaxBot.work_threads_max_count())
        )
        while len(MaxBot.threads) >= MaxBot.work_threads_max_count():
            err = (
                "Threads pool is full. The maximum number (%s) is used. Awaiting release."
                % MaxBot.work_threads_max_count()
            )
            self.lgz.debug(err)
            threads = MaxBot.threads.copy()
            for t in threads:
                if not t.is_alive():
                    self.lgz.debug("stop %s!" % t)
                    t.join()
                    MaxBot.threads.remove(t)
                else:
                    self.lgz.debug("still work %s!" % t)
            self.lgz.info(
                "After trying to release: %s out of %s are used."
                % (len(MaxBot.threads), MaxBot.work_threads_max_count())
            )

    @classmethod
    def check_commands(cls, commands):
        # type: ([BotCommand]) -> []
        err_c = []
        for cmd in commands:
            handler_name = "cmd_handler_%s" % cmd.name
            if hasattr(cls, handler_name):
                cmd_h = getattr(cls, handler_name)
                if not callable(cmd_h):
                    err_c.append(handler_name)
            else:
                err_c.append(handler_name)
        return err_c

    @property
    def commands(self):
        # type: () -> [BotCommand]
        l_c = self.get_commands()
        return l_c

    @property
    def admins_contacts(self):
        # type: () -> {[]}
        if self._admins_contacts is None:
            self._admins_contacts = {}
            # Формат: chats:-70934954694426,-70968954694437;users:591582322454,123582322123;
            l_fe = os.environ.get("TT_BOT_ADMINS_CONTACTS")
            if l_fe:
                f_users = re.match(r".*;?users:(-?\d.+?);.*", l_fe)
                f_chats = re.match(r".*;?chats:(-?\d.+?);.*", l_fe)
                if f_users:
                    l_el = []
                    for _ in f_users.groups()[0].split(","):
                        el = Utils.str_to_int(_)
                        if el:
                            if el not in l_el:
                                l_el.append(el)
                    self._admins_contacts["users"] = l_el
                if f_chats:
                    l_el = []
                    for _ in f_chats.groups()[0].split(","):
                        el = Utils.str_to_int(_)
                        if el:
                            if el not in l_el:
                                l_el.append(el)
                    self._admins_contacts["chats"] = l_el

        return self._admins_contacts

    @classmethod
    def work_threads_max_count(cls):
        if cls._work_threads_max_count is None:
            cls._work_threads_max_count = Utils.str_to_int(
                os.environ.get("TT_BOT_WORK_THREADS_MAX_COUNT")
            )
            if cls._work_threads_max_count is None:
                cls._work_threads_max_count = 15

        return cls._work_threads_max_count

    @staticmethod
    def add_buttons_to_message_body(message_body, buttons):
        # type: (NewMessageBody, list) -> NewMessageBody
        prev_attachments = message_body.attachments
        message_body.attachments = [
            InlineKeyboardAttachmentRequest(
                InlineKeyboardAttachmentRequestPayload(buttons)
            )
        ]
        if prev_attachments:
            for it in prev_attachments:
                if not isinstance(it, InlineKeyboardAttachment):
                    message_body.attachments.append(it)
        return message_body

    def view_main_menu(self, update):
        # type: (UpdateCmn) -> SendMessageResult
        if update.chat_id:
            return self.msg.send_message(
                self.add_buttons_to_message_body(
                    NewMessageBody(self.main_menu_title), self.main_menu_buttons
                ),
                chat_id=update.chat_id,
            )

    def get_buttons_for_chats_available(self, user_id, cmd, ext_args=None):
        # type: (int, str, dict) -> [[CallbackButtonCmd]]
        buttons = []
        ext_args = ext_args or {}
        chats_available = self.get_users_chats_with_bot(user_id)
        i = 0
        for chat in sorted(chats_available.values()):
            i += 1
            args = {"chat_id": chat.chat.chat_id}
            args.update(ext_args)
            buttons.append(
                [
                    CallbackButtonCmd(
                        "%d. %s" % (i, chat.chat_name),
                        cmd,
                        args,
                        Intent.DEFAULT,
                        bot_username=self.username,
                    )
                ]
            )
        return buttons

    def view_buttons_for_chats_available(
        self, title, cmd, user_id, chat_id, link=None, update=None
    ):
        # type: (str, str, int, int, NewMessageLink, Update) -> SendMessageResult
        return self.view_buttons(
            title,
            self.get_buttons_for_chats_available(user_id, cmd),
            user_id,
            chat_id,
            link=link,
            update=update,
        )

    def get_cmd_handler(self, update):
        if not isinstance(update, (Update, UpdateCmn)):
            return False, False
        if not isinstance(update, UpdateCmn):
            update = UpdateCmn(update, self)
        cmd_handler = "cmd_handler_%s" % update.cmd
        if hasattr(self, cmd_handler):
            return getattr(self, cmd_handler)

    def before_polling_update_list(self):
        pass

    def polling(self):
        self.lgz.info("Start. Press Ctrl-Break for stopping.")
        marker = None
        while not self.stop_polling:
            # noinspection PyBroadException
            try:
                self.before_polling_update_list()
                self.lgz.debug("Update request")
                if marker:
                    ul = self.subscriptions.get_updates(
                        marker=marker, types=Update.update_types, _request_timeout=45
                    )
                else:
                    ul = self.subscriptions.get_updates(
                        types=Update.update_types, _request_timeout=45
                    )
                self.lgz.debug("Update request completed. Marker=%s" % marker)
                marker = ul.marker
                if ul.updates:
                    self.after_polling_update_list(True)
                    self.lgz.info("There are %s updates" % len(ul.updates))
                    self.lgz.debug(ul)
                    for update in ul.updates:
                        self.lgz.debug(type(update))
                        self.check_threads()

                        t = Thread(target=self.handle_update, args=(update,))
                        MaxBot.threads.append(t)
                        t.name = "pooling-thr-%04d" % len(MaxBot.threads)
                        t.setDaemon(True)
                        self.lgz.debug(
                            "Thread started. Threads count=%s" % len(MaxBot.threads)
                        )
                        t.start()
                else:
                    self.after_polling_update_list()
                    self.lgz.debug("No updates...")
                self.lgz.debug("Pause for %s seconds" % self.polling_sleep_time)
                sleep(self.polling_sleep_time)

            except ApiException as err:
                if str(err.body).lower().find("Invalid access_token"):
                    raise
            except Exception:
                self.lgz.exception("Exception")
                self.lgz.warning(
                    "Pause for %s seconds because there was an error"
                    % self.polling_error_sleep_time
                )
                sleep(self.polling_error_sleep_time)
                # raise
        self.lgz.info("Stopping")

    def after_polling_update_list(self, updated=False):
        # type: (bool) -> None
        pass

    # Обработка тела запроса
    def handle_request_body(self, request_body):
        # type: (bytes) -> None
        self.check_threads()

        if len(MaxBot.threads) < MaxBot.work_threads_max_count():
            t = Thread(target=self.handle_request_body_, args=(request_body,))
            # noinspection PyBroadException
            try:
                MaxBot.threads.append(t)
                t.name = "webhook-thr-%04d" % len(MaxBot.threads)
                t.setDaemon(True)
                self.lgz.debug("Thread started. Threads count=%s" % len(MaxBot.threads))
                t.start()
            except Exception:
                self.lgz.exception("Exception")
            finally:
                self.lgz.debug("exited")
        else:
            err = (
                "Threads pool is full. The maximum number (%s) is used."
                % MaxBot.work_threads_max_count()
            )
            self.lgz.debug(err)
            incoming_data = self.deserialize_update(request_body)
            if isinstance(incoming_data, Update):
                update = UpdateCmn(incoming_data, self)
                self.send_error_message(update)
                self.send_admin_message(err, update)

    def before_handle_request_body(self, request_body):
        # type: (bytes) -> bytes
        if self:
            return request_body

    # Обработка тела запроса
    def handle_request_body_(self, request_body):
        # type: (bytes) -> None
        incoming_data = None
        # noinspection PyBroadException
        try:
            if request_body:
                self.lgz.debug(
                    "request body:\n%s\n%s"
                    % (request_body, request_body.decode("utf-8"))
                )
                request_body = self.before_handle_request_body(request_body)
                incoming_data = self.deserialize_update(request_body)
                if incoming_data:
                    incoming_data = self.after_handle_request_body(incoming_data)
                    self.lgz.debug(
                        "incoming data:\n type=%s;\n data=%s"
                        % (type(incoming_data), incoming_data)
                    )
                    if isinstance(incoming_data, Update):
                        if not self.update_is_service(UpdateCmn(incoming_data, self)):
                            self.handle_update(incoming_data)
                        else:
                            self.lgz.debug("This update is service - passed")
        except Exception as e:
            self.lgz.exception("Exception")
            if isinstance(incoming_data, Update):
                self.send_error_message(UpdateCmn(incoming_data, self), e)
        finally:
            self.lgz.debug("Thread exited. Threads count=%s" % len(MaxBot.threads))

    def after_handle_request_body(self, incoming_data):
        # type: (object) -> object
        if self:
            return incoming_data

    @classmethod
    def update_is_service(cls, update):
        # type: (UpdateCmn) -> bool
        res = False
        if (
            update
            and update.message
            and update.message.body
            and update.message.body.text
        ):
            res = (
                update.message.body.text[-(len(cls.SERVICE_STR_SEQUENCE)) :]
                == cls.SERVICE_STR_SEQUENCE
            )
        return res

    # noinspection DuplicatedCode
    def send_admin_message(
        self,
        text,
        update=None,
        exception=None,
        notify=True,
        link=None,
        text_escaped=False,
    ):
        # type: (str, UpdateCmn, Exception, bool, NewMessageLink, bool) -> []
        if not link:
            if isinstance(update, UpdateCmn):
                link = update.link
        err = ""
        if exception:
            err = "\n<mark>%s</mark>: <pre>%s</pre>" % (
                OacUtils.escape(exception.__class__.__name__),
                OacUtils.escape(traceback.format_exc()),
            )
        res = []
        now = datetime.now()
        if not text_escaped:
            text = OacUtils.escape(text)
        text = "%s(bot @%s): %s" % (now, OacUtils.escape(self.first_name), (text + err))
        text_add = ""
        if exception and update:
            text_add = "<pre>%s</pre>" % OacUtils.escape(str(update.update_current))
        if self.admins_contacts:
            if self.admins_contacts.get("chats"):
                for el in self.admins_contacts.get("chats"):
                    try:
                        res_s = self.send_message_long_text(
                            NewMessageBody(
                                link=link, notify=notify, format=TextFormat.HTML
                            ),
                            text,
                            chat_id=el,
                        )
                        if res_s:
                            res.extend(res_s)
                        if (
                            res_s
                            and isinstance(res_s[0], SendMessageResult)
                            and text_add
                        ):
                            res_s = self.send_message_long_text(
                                NewMessageBody(
                                    link=NewMessageLink(
                                        MessageLinkType.REPLY, res_s[0].message.body.mid
                                    ),
                                    notify=notify,
                                    format=TextFormat.HTML,
                                ),
                                text_add,
                                chat_id=el,
                            )
                            if res_s:
                                res.extend(res_s)
                    except Exception as e:
                        self.lgz.exception(e)

            if self.admins_contacts.get("users"):
                for el in self.admins_contacts.get("users"):
                    try:
                        res_s = self.send_message_long_text(
                            NewMessageBody(
                                link=link, notify=notify, format=TextFormat.HTML
                            ),
                            text,
                            user_id=el,
                        )
                        if res_s:
                            res.extend(res_s)
                        if isinstance(res_s, SendMessageResult) and text_add:
                            res_s = self.send_message_long_text(
                                NewMessageBody(
                                    link=NewMessageLink(
                                        MessageLinkType.REPLY, res_s.message.body.mid
                                    ),
                                    notify=notify,
                                    format=TextFormat.HTML,
                                ),
                                text_add,
                                user_id=el,
                            )
                            if res_s:
                                res.extend(res_s)
                    except Exception as e:
                        self.lgz.exception(e)

        return res

    def send_error_message(self, update, error=None, link=None):
        # type: (UpdateCmn, Exception, NewMessageLink) -> bool
        if not isinstance(update, UpdateCmn):
            return False

        if not link:
            if isinstance(update, UpdateCmn):
                link = update.link
        res = None
        main_info = self.title
        chat_type = update.chat_type

        if error:
            self.send_admin_message("error", update, error, link=link)

        if not self.update_is_service(update):
            try:
                if update and update.user_id and update.chat_id:
                    chat = self.chats.get_chat(update.chat_id)
                    if isinstance(chat, Chat):
                        chat = ChatExt(chat, self.title)
                        if isinstance(chat, ChatExt):
                            res = bool(
                                self.send_message_long_text(
                                    NewMessageBody(link=link),
                                    main_info + (" (%s)" % chat.chat_name),
                                    user_id=update.user_id,
                                )
                            )
            except Exception as e:
                self.lgz.exception(e)

            if not res:
                if chat_type == ChatType.DIALOG:
                    try:
                        if update and update.chat_id:
                            res = bool(
                                self.send_message_long_text(
                                    NewMessageBody(link=link),
                                    main_info,
                                    chat_id=update.chat_id,
                                )
                            )
                    except Exception as e:
                        self.lgz.exception(e)
                else:
                    self.send_admin_message(str(main_info), update, link=link)

        return res

    def deserialize_open_api_object(self, b_obj, response_type):
        # type: (bytes, str) -> object
        incoming_data = self.client.deserialize(
            urllib3.HTTPResponse(b_obj), response_type
        )
        return incoming_data

    def serialize_open_api_object(self, obj):
        # type: (object) -> str
        return json.dumps(self.client.sanitize_for_serialization(obj))

    def deserialize_update(self, b_obj):
        # type: (bytes) -> Update
        data = json.loads(b_obj)
        incoming_data = None
        if data.get("update_type"):
            incoming_data = self.client.deserialize(
                RESTResponse(urllib3.HTTPResponse(b_obj)),
                Update.discriminator_value_class_map.get(data.get("update_type")),
            )
        return incoming_data

    def serialize_update(self, update):
        # type: (Update) -> str
        return self.serialize_open_api_object(update)

    def action_repeat(self, chat_id, action_name, on=True):
        # type: (int, str, bool) -> None
        if chat_id in self.chats_action:
            t = self.chats_action[chat_id]
        else:
            t = ChatActionRequestRepeater(self.chats, chat_id)
            self.chats_action[chat_id] = t
            t.start()
        if t:
            t.action_switch(action_name, on)

    def before_handle_update(self, update):
        # type: (Update) -> None
        update = UpdateCmn(update, self)
        if update.chat_id:
            self.chats.send_action(
                update.chat_id, ActionRequestBody(SenderAction.MARK_SEEN)
            )
            if update.chat_type in [ChatType.DIALOG]:
                # Запускаем повторитель события
                self.action_repeat(update.chat_id, SenderAction.TYPING_ON)

    def handle_update(self, update):
        # type: (Update) -> bool
        # noinspection PyBroadException
        try:
            self.lgz.debug(" -> %s" % type(update))
            try:
                self.before_handle_update(update)

                is_command = False
                cmd_prefix = "@%s /" % self.info.username
                if isinstance(update, MessageCreatedUpdate):
                    if update.message.body.text.startswith(cmd_prefix):
                        is_command = True
                        update.message.body.text = str(
                            update.message.body.text
                        ).replace(cmd_prefix, "/")
                    elif update.message.body.text.startswith("/"):
                        if update.message.recipient.chat_type == ChatType.DIALOG:
                            is_command = True

                if is_command:
                    self.lgz.debug("entry to %s" % self.process_command)
                    res = self.process_command(update)
                    self.lgz.debug(
                        "exit from %s with result=%s" % (self.process_command, res)
                    )
                elif isinstance(update, MessageCreatedUpdate):
                    if not self.update_is_service(UpdateCmn(update, self)):
                        self.lgz.debug(
                            "entry to %s" % self.handle_message_created_update
                        )
                        res = self.handle_message_created_update(update)
                        self.lgz.debug(
                            "exit from %s with result=%s"
                            % (self.handle_message_created_update, res)
                        )
                    else:
                        res = False
                        self.lgz.debug("This update is service - passed")
                elif isinstance(update, MessageCallbackUpdate):
                    self.lgz.debug("entry to %s" % self.handle_message_callback_update)
                    res = self.handle_message_callback_update(update)
                    self.lgz.debug(
                        "exit from %s with result=%s"
                        % (self.handle_message_callback_update, res)
                    )
                elif isinstance(update, MessageEditedUpdate):
                    self.lgz.debug("entry to %s" % self.handle_message_edited_update)
                    res = self.handle_message_edited_update(update)
                    self.lgz.debug(
                        "exit from %s with result=%s"
                        % (self.handle_message_edited_update, res)
                    )
                elif isinstance(update, MessageRemovedUpdate):
                    self.lgz.debug("entry to %s" % self.handle_message_removed_update)
                    res = self.handle_message_removed_update(update)
                    self.lgz.debug(
                        "exit from %s with result=%s"
                        % (self.handle_message_removed_update, res)
                    )
                elif isinstance(update, BotStartedUpdate):
                    self.lgz.debug("entry to %s" % self.handle_bot_started_update)
                    res = self.handle_bot_started_update(update)
                    self.lgz.debug(
                        "exit from %s with result=%s"
                        % (self.handle_bot_started_update, res)
                    )
                elif isinstance(update, BotAddedToChatUpdate):
                    self.lgz.debug("entry to %s" % self.handle_bot_added_to_chat_update)
                    res = self.handle_bot_added_to_chat_update(update)
                    self.lgz.debug(
                        "exit from %s with result=%s"
                        % (self.handle_bot_added_to_chat_update, res)
                    )
                elif isinstance(update, BotRemovedFromChatUpdate):
                    self.lgz.debug(
                        "entry to %s" % self.handle_bot_removed_from_chat_update
                    )
                    res = self.handle_bot_removed_from_chat_update(update)
                    self.lgz.debug(
                        "exit from %s with result=%s"
                        % (self.handle_bot_removed_from_chat_update, res)
                    )
                elif isinstance(update, UserAddedToChatUpdate):
                    self.lgz.debug(
                        "entry to %s" % self.handle_user_added_to_chat_update
                    )
                    res = self.handle_user_added_to_chat_update(update)
                    self.lgz.debug(
                        "exit from %s with result=%s"
                        % (self.handle_user_added_to_chat_update, res)
                    )
                elif isinstance(update, UserRemovedFromChatUpdate):
                    self.lgz.debug(
                        "entry to %s" % self.handle_user_removed_from_chat_update
                    )
                    res = self.handle_user_removed_from_chat_update(update)
                    self.lgz.debug(
                        "exit from %s with result=%s"
                        % (self.handle_user_removed_from_chat_update, res)
                    )
                elif isinstance(update, ChatTitleChangedUpdate):
                    self.lgz.debug(
                        "entry to %s" % self.handle_chat_title_changed_update
                    )
                    res = self.handle_chat_title_changed_update(update)
                    self.lgz.debug(
                        "exit from %s with result=%s"
                        % (self.handle_chat_title_changed_update, res)
                    )
                elif isinstance(update, MessageChatCreatedUpdate):
                    self.lgz.debug(
                        "entry to %s" % self.handle_message_chat_created_update
                    )
                    res = self.handle_message_chat_created_update(update)
                    self.lgz.debug(
                        "exit from %s with result=%s"
                        % (self.handle_message_chat_created_update, res)
                    )
                elif isinstance(update, MessageConstructionRequest):
                    self.lgz.debug(
                        "entry to %s" % self.handle_message_construction_request
                    )
                    res = self.handle_message_construction_request(update)
                    self.lgz.debug(
                        "exit from %s with result=%s"
                        % (self.handle_message_construction_request, res)
                    )
                elif isinstance(update, MessageConstructedUpdate):
                    self.lgz.debug(
                        "entry to %s" % self.handle_message_constructed_update
                    )
                    res = self.handle_message_constructed_update(update)
                    self.lgz.debug(
                        "exit from %s with result=%s"
                        % (self.handle_message_constructed_update, res)
                    )
                else:
                    res = False
            finally:
                self.after_handle_update(update)
            return res
        except Exception as e:
            self.lgz.exception("Exception")
            update = UpdateCmn(update, self)
            self.send_error_message(update, e)

    def after_handle_update(self, update):
        # type: (Update) -> None
        update = UpdateCmn(update, self)
        if update.chat_id:
            # Отключаем повторитель события
            self.action_repeat(update.chat_id, SenderAction.TYPING_ON, False)

    def handle_message_created_update(self, update):
        # type: (MessageCreatedUpdate) -> bool
        update = UpdateCmn(update, self)
        # Проверка на ответ команде
        update_previous = self.prev_step_get(update.index)
        if isinstance(update_previous, Update):
            self.lgz.debug("Command answer detected (%s)." % update.index)
            # Если это ответ на вопрос команды, то установить соответствующий признак и снова вызвать команду
            update.this_cmd_response = True
            update.update_previous = update_previous
            update_previous = UpdateCmn(update_previous, self)
            res_w_m = None
            try:
                if self.waiting_msg and update.chat_type == ChatType.DIALOG:
                    msg_t = (
                        ("{%s} " % self.title)
                        + _("Wait for process your request (%s)...")
                        % update_previous.cmd
                    ) + self.SERVICE_STR_SEQUENCE
                    res_w_m = self.msg.send_message(
                        NewMessageBody(msg_t), chat_id=update.chat_id
                    )

                handler_exists, res = self.call_cmd_handler(update)
            finally:
                if isinstance(res_w_m, SendMessageResult):
                    self.msg.delete_message(res_w_m.message.body.mid)
            return res
        self.lgz.debug("Trivial message. Not commands answer (%s)." % update.index)
        return self.receive_message(update)

    def receive_message(self, update):
        # type: (UpdateCmn) -> bool
        pass

    receive_text = receive_message

    def handle_message_callback_update(self, update):
        # type: (MessageCallbackUpdate) -> bool
        self.last_mcb_update[update.message.recipient.chat_id] = update
        ind = UpdateCmn.get_callback_index(update.callback)
        if self.callbacks_list.get(ind):
            self.callbacks_list[ind] = [
                update.callback.timestamp,
                self.callbacks_list[ind][0],
            ]
        else:
            self.callbacks_list[ind] = [update.callback.timestamp]

        if update.callback.payload:
            self.lgz.debug("MessageCallbackUpdate:\r\n%s" % update.callback.payload)
            res = self.process_command(update)
            if res:
                self.delete_message(update.message.body.mid)
        else:
            res = self.delete_message(update.message.body.mid)
        return res

    def handle_message_edited_update(self, update):
        # type: (MessageEditedUpdate) -> bool
        update = UpdateCmn(update, self)
        if update and update.chat_id:
            chat = self.chats.get_chat(update.chat_id)
            return self.msg.send_message(
                NewMessageBody("отредактировал сообщение"), chat_id=chat.chat_id
            )
        # pass

    def handle_message_removed_update(self, update):
        # type: (MessageRemovedUpdate) -> bool
        pass

    def handle_bot_started_update(self, update):
        # type: (BotStartedUpdate) -> bool
        return self.process_command(update)

    def handle_bot_added_to_chat_update(self, update):
        # type: (BotAddedToChatUpdate) -> bool
        pass

    def handle_bot_removed_from_chat_update(self, update):
        # type: (BotRemovedFromChatUpdate) -> bool
        pass

    def handle_user_added_to_chat_update(self, update):
        # type: (UserAddedToChatUpdate) -> bool
        pass

    def handle_user_removed_from_chat_update(self, update):
        # type: (UserRemovedFromChatUpdate) -> bool
        pass

    def handle_chat_title_changed_update(self, update):
        # type: (ChatTitleChangedUpdate) -> bool
        pass

    def handle_message_chat_created_update(self, update):
        # type: (MessageChatCreatedUpdate) -> bool
        pass

    def handle_message_construction_request(self, update):
        # type: (MessageConstructionRequest) -> bool
        pass

    def handle_message_constructed_update(self, update):
        # type: (MessageConstructedUpdate) -> bool
        pass

    def get_chat_members(self, chat_id, user_ids=None):
        # type: (int, [int]) -> {ChatMember}
        marker = None
        m_dict = {}
        members = []
        while True:
            if user_ids:
                cm = self.chats.get_members(chat_id, user_ids=user_ids)
            elif marker:
                cm = self.chats.get_members(chat_id, marker=marker)
            else:
                cm = self.chats.get_members(chat_id)
            if isinstance(cm, ChatMembersList):
                marker = cm.marker
                members.extend(cm.members)
                for c in cm.members:
                    if isinstance(c, ChatMember):
                        m_dict[c.user_id] = c
            if not marker:
                break
        return m_dict

    def get_chat_admins(self, chat_id):
        # type: (int) -> {ChatMember}
        marker = None
        m_dict = {}
        admins = []
        while True:
            if marker:
                cm = self.chats.get_admins(chat_id, marker=marker)
            else:
                cm = self.chats.get_admins(chat_id)
            if isinstance(cm, ChatMembersList):
                marker = cm.marker
                admins.extend(cm.members)
                for c in cm.members:
                    if isinstance(c, ChatMember):
                        m_dict[c.user_id] = c
            if not marker:
                break
        return m_dict

    # Определяет разрешённость чата
    def chat_is_allowed(self, chat_ext, user_id=None):
        # type: (ChatExt, int) -> bool
        if isinstance(chat_ext, ChatExt):
            if user_id:
                pass
            ap = chat_ext.admin_permissions.get(self.user_id)
            return (
                ap
                and ChatAdminPermission.WRITE in ap
                and ChatAdminPermission.READ_ALL_MESSAGES in ap
            )

    @staticmethod
    def adm_permission_add(ce_ap, adm_perm):
        # type: (list, str) -> None
        if ce_ap and adm_perm not in ce_ap:
            ce_ap.append(adm_perm)

    @staticmethod
    def adm_perm_correct(ce_ap):
        if ce_ap and ChatAdminPermission.ADD_ADMINS in ce_ap:
            MaxBot.adm_permission_add(ce_ap, ChatAdminPermission.ADD_REMOVE_MEMBERS)
            MaxBot.adm_permission_add(ce_ap, ChatAdminPermission.READ_ALL_MESSAGES)
            MaxBot.adm_permission_add(ce_ap, ChatAdminPermission.WRITE)
            MaxBot.adm_permission_add(ce_ap, ChatAdminPermission.CHANGE_CHAT_INFO)
            MaxBot.adm_permission_add(ce_ap, ChatAdminPermission.PIN_MESSAGE)

    def get_dialog_name(self, title, user=None, chat=None, user_id=None):
        # type: (str, User, Chat, int) -> str
        user_id = user_id or (user.user_id if user else None)
        if user_id and chat and not user:
            try:
                user = (
                    self.get_chat_admins(chat.chat_id).get(user_id)
                    if chat.type != ChatType.DIALOG
                    else self.chats.get_chat(chat.chat_id).dialog_with_user
                )
            except ApiException as e:
                return (
                    "Error: %s (%s|%s) -> %s" % (user_id, chat.chat_id, chat.title, e)
                    + title
                )
        if user:
            return "%s (%s|%s) -> " % (user.user_id, user.name, user.username) + title

    # Определяет доступность чата для пользователя
    def chat_is_available(self, chat, user_id):
        # type: (Chat, int) -> ChatExt or None

        if isinstance(chat, Chat):
            if chat.status in [ChatStatus.ACTIVE]:
                members = None
                bot_user = None
                try:
                    if chat.type != ChatType.DIALOG:
                        bot_user = self.chats.get_membership(chat.chat_id)
                        if isinstance(bot_user, ChatMember):
                            # Только если бот админ
                            if bot_user.is_admin:
                                try:
                                    members = self.get_chat_members(
                                        chat.chat_id, [user_id]
                                    )
                                except ApiException as err:
                                    if err.status != 404:
                                        raise
                                    self.lgz.debug(
                                        "chat => chat_id=%(id)s - pass, because user %(user_id)s not found"
                                        % {"id": chat.chat_id, "user_id": user_id}
                                    )
                            else:
                                self.lgz.debug(
                                    "chat => chat_id=%(id)s - pass, because bot not admin"
                                    % {"id": chat.chat_id}
                                )
                                return None
                except ApiException as err:
                    if err.status != 403:
                        raise
                if members or chat.type == ChatType.DIALOG:
                    chat_ext = None
                    if members and chat.type != ChatType.DIALOG:
                        current_user = members.get(user_id)
                        if current_user and current_user.is_admin:
                            chat_ext = ChatExt(
                                chat,
                                self.get_dialog_name(self.title, user=current_user),
                            )
                            if bot_user:
                                chat_ext.admin_permissions[self.user_id] = (
                                    bot_user.permissions
                                )
                                self.adm_perm_correct(
                                    chat_ext.admin_permissions[self.user_id]
                                )
                                chat_ext.admin_permissions[user_id] = (
                                    current_user.permissions
                                )
                                self.adm_perm_correct(
                                    chat_ext.admin_permissions[user_id]
                                )
                            else:
                                self.lgz.debug(
                                    "Pass, because bot with id=%s not found into chat %s members list"
                                    % (self.user_id, chat.chat_id)
                                )
                    elif chat.type == ChatType.DIALOG:
                        current_user = chat.dialog_with_user
                        # Вот так интересно вычисляется id диалога бота с пользователем
                        # user_dialog_id = self.user_id ^ user_id
                        chat_ext = ChatExt(
                            chat, self.get_dialog_name(self.title, user=current_user)
                        )
                        if user_id == current_user.user_id:
                            chat_ext.admin_permissions[self.user_id] = [
                                ChatAdminPermission.WRITE,
                                ChatAdminPermission.READ_ALL_MESSAGES,
                            ]
                            chat_ext.admin_permissions[user_id] = [
                                ChatAdminPermission.WRITE,
                                ChatAdminPermission.READ_ALL_MESSAGES,
                            ]
                        else:
                            self.lgz.debug(
                                "Exit, because dialog_id=%s not for user_id=%s"
                                % (chat.chat_id, user_id)
                            )
                    if chat_ext and chat_ext.admin_permissions:
                        return chat_ext
                    else:
                        self.lgz.debug(
                            "Pass, because for user_id=%s  not admin permissions into chat_id=%s"
                            % (user_id, chat.chat_id)
                        )
                else:
                    self.lgz.debug(
                        "Pass, because for user_id=%s  not enough permissions into chat_id=%s"
                        % (user_id, chat.chat_id)
                    )
            else:
                self.lgz.debug(
                    "chat => chat_id=%(id)s - pass, because bot not active"
                    % {"id": chat.chat_id}
                )

    # Формирует список чатов пользователя, в которых админы и он и бот с доп проверкой разрешений
    def get_users_chats_with_bot(self, user_id):
        # type: (int) -> dict
        return self.get_users_chats_with_bot_adm(user_id, False)

    # Формирует список чатов пользователя, в которых админы и он и бот с возможностью доп проверки разрешений
    def get_users_chats_with_bot_adm(self, user_id, admin_only):
        # type: (int, bool) -> dict
        marker = None
        chats_available = {}
        while True:
            if marker:
                chat_list = self.chats.get_chats(marker=marker)
            else:
                chat_list = self.chats.get_chats()
            if isinstance(chat_list, ChatList):
                marker = chat_list.marker
                for chat in chat_list.chats:
                    self.lgz.debug(
                        "Found chat => chat_id=%(id)s; type: %(type)s; status: %(status)s; title: %(title)s; participants: %(participants)s; owner: %(owner)s"
                        % {
                            "id": chat.chat_id,
                            "type": chat.type,
                            "status": chat.status,
                            "title": chat.title,
                            "participants": chat.participants_count,
                            "owner": chat.owner_id,
                        }
                    )
                    chat_ext = self.chat_is_available(chat, user_id)
                    if chat_ext and (
                        admin_only or self.chat_is_allowed(chat_ext, user_id)
                    ):
                        chats_available[chat.chat_id] = chat_ext
                        self.lgz.debug(
                            "chat => chat_id=%(id)s added into list available chats"
                            % {"id": chat.chat_id}
                        )
                if not marker:
                    break
        return chats_available

    # Формирует список чатов пользователей, в которых админы и пользователь и бот с возможностью доп проверки разрешений
    def get_all_chats_with_bot_admin(self, admin_only=False):
        # type: ([int]) -> dict
        marker = None
        chats_available = {
            "Chats": {},
            "Members": {},
            "ChatsMembers": {},
        }
        chats_available_cm = chats_available["ChatsMembers"]
        chats_available_m = chats_available["Members"]
        chats_available_c = chats_available["Chats"]
        chats_all = {}
        bot = self.info
        if isinstance(bot, BotInfo):
            bot = ChatMember(
                description=bot.description,
                user_id=bot.user_id,
                name=bot.name,
                username=bot.username,
                is_bot=bot.is_bot,
                last_activity_time=bot.last_activity_time,
                avatar_url=bot.avatar_url,
                full_avatar_url=bot.full_avatar_url,
                last_access_time=0,
                is_owner=False,
                is_admin=True,
                join_time=0,
                permissions=[
                    ChatAdminPermission.WRITE,
                    ChatAdminPermission.READ_ALL_MESSAGES,
                ],
            )

        while True:
            if marker:
                chat_list = self.chats.get_chats(marker=marker)
            else:
                chat_list = self.chats.get_chats()
            if isinstance(chat_list, ChatList):
                marker = chat_list.marker
                for chat in chat_list.chats:
                    self.lgz.debug(
                        "Found chat => chat_id=%(id)s; type: %(type)s; status: %(status)s; title: %(title)s; participants: %(participants)s; owner: %(owner)s"
                        % {
                            "id": chat.chat_id,
                            "type": chat.type,
                            "status": chat.status,
                            "title": chat.title,
                            "participants": chat.participants_count,
                            "owner": chat.owner_id,
                        }
                    )
                    if chat.status not in [ChatStatus.ACTIVE]:
                        continue

                    admins = {}
                    if chat.type == ChatType.DIALOG:
                        dialog_user = chat.dialog_with_user
                        if isinstance(dialog_user, UserWithPhoto):
                            dialog_user = ChatMember(
                                description=dialog_user.description,
                                user_id=dialog_user.user_id,
                                name=dialog_user.name,
                                username=dialog_user.username,
                                is_bot=dialog_user.is_bot,
                                last_activity_time=dialog_user.last_activity_time,
                                avatar_url=dialog_user.avatar_url,
                                full_avatar_url=dialog_user.full_avatar_url,
                                last_access_time=0,
                                is_owner=False,
                                is_admin=True,
                                join_time=0,
                                permissions=[
                                    ChatAdminPermission.WRITE,
                                    ChatAdminPermission.READ_ALL_MESSAGES,
                                ],
                            )
                        # dialog_user_id = self.user_id ^ chat.chat_id
                        admins[dialog_user.user_id] = dialog_user
                        admins[bot.user_id] = bot
                    else:
                        try:
                            admins = self.get_chat_admins(chat.chat_id)
                        except ApiException as err:
                            if err.status != 403:
                                raise
                    bot_user = admins.get(self.user_id)
                    if bot_user:
                        for admin in admins.values():
                            if admin.user_id != self.user_id:
                                # chat_ext = chats_available[admin.user_id].get(chat.chat_id)
                                chat_ext = chats_all.get(chat.chat_id)
                                if not isinstance(chat_ext, ChatExt):
                                    chat_ext = ChatExt(
                                        chat,
                                        self.get_dialog_name(self.title, user=admin),
                                    )
                                    chats_all[chat.chat_id] = chat_ext
                                chat_ext.admin_permissions[self.user_id] = (
                                    bot_user.permissions
                                )
                                self.adm_perm_correct(
                                    chat_ext.admin_permissions[self.user_id]
                                )
                                chat_ext.admin_permissions[admin.user_id] = (
                                    admin.permissions
                                )
                                self.adm_perm_correct(
                                    chat_ext.admin_permissions[admin.user_id]
                                )

                                if chat_ext and (
                                    admin_only
                                    or self.chat_is_allowed(chat_ext, admin.user_id)
                                ):
                                    if chats_available_cm.get(admin.user_id) is None:
                                        chats_available_cm[admin.user_id] = {}
                                    if chats_available_c.get(chat_ext.chat_id) is None:
                                        chats_available_c[chat_ext.chat_id] = chat_ext
                                    if chats_available_m.get(admin.user_id) is None:
                                        chats_available_m[admin.user_id] = admins.get(
                                            admin.user_id
                                        )

                                    chats_available_cm[admin.user_id][chat.chat_id] = (
                                        chat_ext
                                    )
                    else:
                        self.lgz.debug(
                            "Pass, because for chat_id=%s bot (id=%s) is not admin"
                            % (chat.chat_id, self.user_id)
                        )
                if not marker:
                    break
        return chats_available

    @staticmethod
    def limited_buttons_index(**kwargs):
        """

        :rtype: str
        """
        if "mid" in kwargs:
            return kwargs["mid"]

    @staticmethod
    def limited_buttons_get(index):
        # type: (str) -> [[]]
        return MaxBot.limited_buttons.get(index)

    @staticmethod
    def limited_buttons_set(index, buttons):
        # type: (str, [[]]) -> None
        MaxBot.limited_buttons[index] = buttons

    @staticmethod
    def limited_buttons_del(index):
        # type: (str) -> None
        if index in MaxBot.limited_buttons:
            MaxBot.limited_buttons.pop(index)

    def cmd_handler_get_buttons_oth(self, update):
        if not isinstance(update.update_current, MessageCallbackUpdate):
            return False
        if update.cmd_args:
            direction = update.cmd_args.get("direction")
            start_from = update.cmd_args.get("start_from")
            max_lines = update.cmd_args.get("max_lines")
            add_close_button = update.cmd_args.get("add_close_button")
            add_info = update.cmd_args.get("add_info")
            mid = update.message.body.mid
            if direction == "close":
                self.limited_buttons_del(self.limited_buttons_index(mid=mid))
                return True
            buttons = self.limited_buttons_get(self.limited_buttons_index(mid=mid))
            if mid and buttons:
                self.view_buttons(
                    title=None,
                    buttons=buttons,
                    update=mid,
                    add_info=add_info,
                    add_close_button=add_close_button,
                    start_from=start_from,
                    max_lines=max_lines,
                )
            else:
                self.send_notification(update, _("Something went wrong..."))
                return True
        return False

    def view_buttons(
        self,
        title,
        buttons,
        user_id=None,
        chat_id=None,
        link=None,
        update=None,
        add_info=False,
        add_close_button=False,
        start_from=None,
        max_lines=None,
    ):
        # type: (str or None, list, int or None, int or None, NewMessageLink, Update, bool, bool, int or None, int or None) -> SendMessageResult
        start_from = start_from or 0
        max_lines_orig = max_lines
        max_lines = min(
            max(max_lines or CallbackButtonCmd.MAX_ROWS - 1, 1),
            CallbackButtonCmd.MAX_ROWS - 1,
        )

        base_buttons = buttons
        limited = False
        if buttons:
            buttons = []
            buttons_service = [[]]
            pos_start = min(len(base_buttons), max(0, start_from))
            pos_end = min(len(base_buttons), max(0, start_from + max_lines))
            pages = len(base_buttons) % max_lines
            is_pages_start = pos_start == 0
            is_pages_end = pos_end == len(base_buttons)
            cmd = "get_buttons_oth"
            fast_rev_need = pages >= 5
            if len(base_buttons) > max_lines:
                if fast_rev_need and not is_pages_start:
                    button_title = "⏮"
                    buttons_service[0].append(
                        CallbackButtonCmd(
                            button_title,
                            cmd,
                            {
                                "direction": "backward",
                                "start_from": 0,
                                "max_lines": max_lines_orig,
                                "add_close_button": add_close_button,
                                "add_info": add_info,
                            },
                            Intent.POSITIVE,
                            bot_username=self.username,
                        )
                    )
                if pos_start > 0:
                    button_title = "←"
                    if add_info:
                        button_title = "%s %d-%d/\n%d" % (
                            button_title,
                            max(0, pos_start - max_lines) + 1,
                            pos_start,
                            len(base_buttons),
                        )
                    buttons_service[0].append(
                        CallbackButtonCmd(
                            button_title,
                            cmd,
                            {
                                "direction": "backward",
                                "start_from": pos_start - max_lines,
                                "max_lines": max_lines_orig,
                                "add_close_button": add_close_button,
                                "add_info": add_info,
                            },
                            Intent.POSITIVE,
                            bot_username=self.username,
                        )
                    )
                    limited = True
            buttons.extend(base_buttons[pos_start:pos_end])
            if len(base_buttons) > max_lines:
                if pos_end < len(base_buttons):
                    button_title = "→"
                    if add_info:
                        button_title = "%s %d-%d/%d" % (
                            button_title,
                            pos_start + 1 + max_lines,
                            min(len(base_buttons), pos_start + max_lines * 2),
                            len(base_buttons),
                        )
                    buttons_service[0].append(
                        CallbackButtonCmd(
                            button_title,
                            cmd,
                            {
                                "direction": "forward",
                                "start_from": pos_end,
                                "max_lines": max_lines_orig,
                                "add_close_button": add_close_button,
                                "add_info": add_info,
                            },
                            Intent.POSITIVE,
                            bot_username=self.username,
                        )
                    )
                    limited = True
                if fast_rev_need and not is_pages_end:
                    button_title = "⏭"
                    buttons_service[0].append(
                        CallbackButtonCmd(
                            button_title,
                            cmd,
                            {
                                "direction": "forward",
                                "start_from": len(base_buttons) - max_lines,
                                "max_lines": max_lines_orig,
                                "add_close_button": add_close_button,
                                "add_info": add_info,
                            },
                            Intent.POSITIVE,
                            bot_username=self.username,
                        )
                    )
            if add_close_button:
                buttons_service[0].append(
                    CallbackButtonCmd(
                        _("Close"),
                        cmd,
                        {
                            "direction": "close",
                            "start_from": pos_end,
                            "add_close_button": add_close_button,
                            "add_info": add_info,
                        },
                        Intent.NEGATIVE,
                        bot_username=self.username,
                    )
                )
            if buttons_service[0]:
                buttons.extend(buttons_service)

            mb = self.add_buttons_to_message_body(
                NewMessageBody(title, link=link), buttons
            )
        else:
            mb = NewMessageBody(_("No available items found."), link=link)
        mid = None
        if isinstance(update, MessageCallbackUpdate):
            mid = update.message.body.mid
        elif isinstance(update, str):
            mid = update

        if not (user_id or chat_id or mid):
            raise TypeError("user_id or chat_id or mid must be defined.")
        res = None
        if mid:
            self.msg.edit_message(mid, mb)
        else:
            if chat_id:
                res = self.msg.send_message(mb, chat_id=chat_id)
            else:
                res = self.msg.send_message(mb, user_id=user_id)

        if isinstance(res, SendMessageResult):
            mid = res.message.body.mid

        if limited and mid:
            self.limited_buttons_set(self.limited_buttons_index(mid=mid), base_buttons)
        return res

    def view_buttons_lim(
        self,
        title,
        buttons,
        user_id=None,
        chat_id=None,
        link=None,
        update=None,
        lim_items=None,
        lim_notify=None,
        lim_notify_g=None,
        lim_notify_admin=None,
        add_info=False,
        add_close_button=False,
        start_from=None,
        max_lines=None,
    ):
        # type: (str or None, list, int or None, int or None, NewMessageLink, Update, int, str, str, str, bool, bool, int or None, int or None) -> SendMessageResult
        if lim_items:
            first_call = update and UpdateCmn(update).cmd_args is None
            num_subscribers_cur = len(buttons)
            if num_subscribers_cur > lim_items:
                b = buttons or []
                buttons = []
                i = 0
                for e in b:
                    if i >= lim_items:
                        break
                    i += 1
                    buttons.append(e)
                if lim_notify_admin and first_call:
                    self.send_admin_message(lim_notify_admin)
            if lim_notify and (
                (lim_notify_g and num_subscribers_cur >= lim_items)
                or (not lim_notify_g and num_subscribers_cur > lim_items)
            ):
                m_t = lim_notify
                if lim_notify_g and num_subscribers_cur > lim_items:
                    m_t += "\n" + lim_notify_g
                title = "%s\n\n{m_t}" % title
        return self.view_buttons(
            title,
            buttons,
            user_id,
            chat_id,
            link=link,
            update=update,
            add_info=add_info,
            add_close_button=add_close_button,
            start_from=start_from,
            max_lines=max_lines,
        )

    def get_yes_no_buttons(self, cmd_dict):
        # type: ([{}]) -> list
        if not cmd_dict:
            return []
        return self.get_buttons(
            [
                CallbackButtonCmd(
                    _("Yes"),
                    cmd_dict["yes"]["cmd"],
                    cmd_dict["yes"]["cmd_args"],
                    Intent.POSITIVE,
                    bot_username=self.username,
                ),
                CallbackButtonCmd(
                    _("No"),
                    cmd_dict["no"]["cmd"],
                    cmd_dict["no"]["cmd_args"],
                    Intent.NEGATIVE,
                    bot_username=self.username,
                ),
            ]
        )

    @staticmethod
    def get_buttons(cbc, orientation="horizontal"):
        # type: ([CallbackButtonCmd], str) -> list
        if not cbc:
            return []
        orientation = orientation or "horizontal"
        res = []
        for bt in cbc:
            res.append(bt)
        if orientation == "horizontal":
            res = [res]
        else:
            res = [[_] for _ in res]

        return res

    def upload_content(self, content, upload_type, content_name=None):
        # type: ([], str, str) -> dict
        upload_ep = self.upload.get_upload_url(type=upload_type)
        if isinstance(upload_ep, UploadEndpoint):
            rdf = requests.post(
                upload_ep.url,
                files={
                    "files": (
                        "file" if not content_name else content_name,
                        content,
                        "multipart/form-data",
                    )
                },
                verify=Utils.get_environ_bool("TT_BOT_UPLOAD_SSL_VERIFY", True),
            )
            if rdf.status_code == 200:
                return rdf.json()

    def attach_contents(self, items):
        # type: ([(bytes, str)]) -> []
        if not items:
            return
        attachments = []
        for item in items:
            klass = None
            if item[1] == UploadType.VIDEO:
                klass = VideoAttachmentRequest
            elif item[1] == UploadType.IMAGE:
                klass = PhotoAttachmentRequest
            elif item[1] == UploadType.AUDIO:
                klass = AudioAttachmentRequest
            elif item[1] == UploadType.FILE:
                klass = FileAttachmentRequest

            if klass:
                if not isinstance(item[0], dict):
                    upl = self.upload_content(
                        item[0], item[1], None if len(item) < 3 else item[2]
                    )
                    if isinstance(upl, dict):
                        attachments.append(klass(upl))
                else:
                    attachments.append(klass(item[0]))
        return attachments

    # noinspection PyIncorrectDocstring
    def send_message(self, mb, max_retry=20, sl_time=1, **kwargs):
        """
        :param NewMessageBody mb: (required)
        :param int max_retry: maximum number of repetitions
        :param int sl_time: delay time for repeating an error
        :param int user_id: Fill this parameter if you want to send message to user
        :param int chat_id: Fill this if you send message to chat
        :return: SendMessageResult
                 If the method is called asynchronously,
                 returns the request thread.
        """

        rpt = 0
        while rpt < max_retry:
            try:
                rpt += 1
                self.lgz.debug(str(rpt) + " trying: send message with post")
                res_msg = self.msg.send_message(mb, **kwargs)
                self.lgz.debug(str(rpt) + " trying: message is sent")
                return res_msg
            except ApiException as e:
                self.lgz.debug(
                    "Warning: status:%(status)s; reason:%(reason)s; body:%(body)s"
                    % {"status": e.status, "reason": e.reason, "body": e.body}
                )
                if rpt >= max_retry or not (
                    e.status == 400
                    and e.body.find('"code":"attachment.not.ready"') >= 0
                    or e.status == 429
                ):
                    raise
                slt = sl_time
                if e.status == 429:  # too.many.requests
                    slt = 2
                self.lgz.debug(str(rpt) + " sleep: %s sec." % slt)
                sleep(slt)

    # noinspection PyIncorrectDocstring
    def send_message_long_text(self, mb, long_text, max_retry=20, sl_time=1, **kwargs):
        # type: (NewMessageBody, str or [], int, int, dict) -> [SendMessageResult]
        """
        :param NewMessageBody mb: (required)
        :param str long_text: (required)
        :param int max_retry: maximum number of repetitions
        :param int sl_time: delay time for repeating an error
        :param int user_id: Fill this parameter if you want to send message to user
        :param int chat_id: Fill this if you send message to chat
        :return: SendMessageResult
                 If the method is called asynchronously,
                 returns the request thread.
        """
        res_list = []

        if not isinstance(long_text, list):
            text_storage = Utils.put_into_text_storage(
                [], long_text, NewMessageBody.MAX_BODY_LENGTH * 0.9
            )
        else:
            text_storage = long_text
        link_p = mb.link
        i = 0
        for text in text_storage:
            i += 1
            if i != 1:
                mb.attachments = None
            mb.text = text.strip() if text is not None else None
            mb.link = link_p
            res = self.send_message(mb, max_retry, sl_time, **kwargs)
            if res:
                link_p = NewMessageLink(MessageLinkType.REPLY, res.message.body.mid)
            res_list.append(res)
        return res_list

    def send_notification(self, update, notification):
        """

        :rtype: None
        :param UpdateCmn update:
        :param str notification:
        """
        if update and notification:
            if isinstance(update.update_current, MessageCallbackUpdate):
                update_current = update.update_current
            else:
                update_current = self.last_mcb_update.get(update.chat_id)
            if update_current:
                self.msg.answer_on_callback(
                    update_current.callback.callback_id,
                    CallbackAnswer(notification=notification),
                )

    def delete_message(self, mid):
        # type: (str) -> SimpleQueryResult
        try:
            return self.msg.delete_message(mid)
        except ApiException:
            pass

    def get_chat_messages(self, chat_id, dt_end=None, dt_start=None, max_msg=1000):
        # type: (int, datetime, datetime, int or None) -> [Message]
        message_list = []
        ut_start = Utils.datetime_to_unix_time(dt_start) if dt_start else None
        dt_end = dt_end or datetime.now().astimezone() + timedelta(seconds=1)
        ut_end = Utils.datetime_to_unix_time(dt_end)
        # [(_.timestamp, datetime_from_unix_time(_.timestamp)) for _ in m_l]
        while True:
            m_l = self.msg.get_messages(
                chat_id=chat_id, count=MessagesApi.MAX_MESSAGE_COUNT, _from=ut_end
            ).messages
            if not m_l:
                break
            if ut_start and m_l[0].timestamp < ut_start:
                break
            message_list.extend(m_l)
            ut_end = m_l[-1].timestamp - 1
            if max_msg and len(message_list) >= max_msg:
                break
        return message_list[:max_msg]

    def get_messages(self, mid_list):
        # type: ([str]) -> [Message]
        try:
            ml = self.msg.get_messages(message_ids=mid_list)
            if isinstance(ml, MessageList) and ml.messages:
                return ml.messages
        except ApiException:
            pass

    # Возвращает список сообщений по списку mid ов
    def get_message_list(self, mid_list):
        # type: ([str]) -> [Message]
        message_list = []
        bad_mid_list = []
        max_cnt_for_mid_list = 80
        for i in range(math.ceil(len(mid_list) / max_cnt_for_mid_list)):
            cur_mid_list = mid_list[
                (i * max_cnt_for_mid_list) : ((i + 1) * max_cnt_for_mid_list)
            ]
            try:
                msg_m_list = self.msg.get_messages(
                    message_ids=cur_mid_list, count=MessagesApi.MAX_MESSAGE_COUNT
                )
                if msg_m_list:
                    message_list.extend(msg_m_list.messages)
                    getting_mid_list = [_.body.mid for _ in msg_m_list.messages]
                    for mid in cur_mid_list:
                        if mid not in getting_mid_list:
                            msg = self.get_message(mid)
                            if msg:
                                message_list.append(msg)
                            else:
                                bad_mid_list.append(mid)
            except (ApiException, ValueError):
                for mid in cur_mid_list:
                    msg = self.get_message(mid)
                    if msg:
                        message_list.append(msg)
                    else:
                        bad_mid_list.append(mid)
        # Очищаем список переданных mid - как обработанных
        mid_list.clear()
        # Битые mid возвращаем, как необработанные
        mid_list.extend(bad_mid_list)

        return message_list

    def get_message(self, mid):
        # type: ([str]) -> Message
        try:
            return self.msg.get_message_by_id(mid)
        except (ApiException, ValueError):
            pass

    def get_forwarded_message(self, message):
        # type: (Message or str) -> LinkedMessage
        if isinstance(message, str):
            message = self.get_message(message)
        if (
            isinstance(message, Message)
            and isinstance(message.body, MessageBody)
            and isinstance(message.link, LinkedMessage)
            and message.link.type in [MessageLinkType.FORWARD]
        ):
            return message.link

    def get_forwarded_message_full(self, message):
        # type: (Message) -> Message
        lm = self.get_forwarded_message(message)
        if isinstance(lm, LinkedMessage) and lm.message:
            return self.get_message(lm.message.mid)

    def subscribe(self, url_list, adding=False):
        # type:(MaxBot, [str], bool) -> bool
        if not url_list:
            return False
        if not adding:
            res = self.subscriptions.get_subscriptions()
            if isinstance(res, GetSubscriptionsResult):
                for subscription in res.subscriptions:
                    if isinstance(subscription, Subscription):
                        res = self.subscriptions.unsubscribe(subscription.url)
                        if isinstance(res, SimpleQueryResult) and not res.success:
                            self.lgz.warning(
                                "Failed delete subscribe url=%s" % subscription.url
                            )
                        elif isinstance(res, SimpleQueryResult) and res.success:
                            self.lgz.info("Deleted subscribe url=%s" % subscription.url)
        for url in url_list:
            wh_info = "WebHook url=%s, version=%s" % (url, self.conf.api_version)
            sb = SubscriptionRequestBody(url, version=self.conf.api_version)
            res = self.subscriptions.subscribe(sb)
            if isinstance(res, SimpleQueryResult) and not res.success:
                raise MaxBotException(res.message)
            elif not isinstance(res, SimpleQueryResult):
                raise MaxBotException(
                    "Something went wrong when subscribing the WebHook %s" % wh_info
                )
            self.lgz.info("Bot subscribed to receive updates via WebHook %s" % wh_info)
        return True


class BotDev(MaxBot):
    @property
    def token(self):
        return os.environ.get("MAX_BOT_API_TOKEN")

    @property
    def description(self):
        return (
            "Этот бот помогает в разработке и управлении ботами.\n\n"
            "This bot is an helper in the development and management of bots."
        )


if __name__ == "__main__":
    BotDev().polling()

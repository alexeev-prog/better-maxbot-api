# -*- coding: UTF-8 -*-
import functools
import hashlib
import inspect
import logging
import math
import os
import re
import sys
import time
from datetime import date, datetime
from html.entities import name2codepoint
from html.parser import HTMLParser
from logging.handlers import RotatingFileHandler
from typing import Callable, TypeVar

from croniter import croniter

RT = TypeVar("RT")


# noinspection PyUnusedLocal
def log_dec(
    func: Callable[..., RT],
    *args: object,
    **kwargs: object,  # pylint: disable=W0613
) -> Callable[..., RT]:
    # logger = logging.getLogger(func.__module__)
    logger = BotLogger.get_instance()

    # noinspection PyShadowingNames
    @functools.wraps(func)
    def decorator(*args: object, **kwargs: object) -> RT:  # pylint: disable=W0613
        logger.debug("Entering: %s", func.__name__)
        result = func(*args, **kwargs)
        logger.debug(result)
        logger.debug("Exiting: %s", func.__name__)
        return result

    return decorator


class _HTMLToText(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._buf = []
        self.hide_output = False

    def handle_starttag(self, tag, attrs):
        if tag in ("p", "br") and not self.hide_output:
            self._buf.append("\n")
        elif tag in ("script", "style"):
            self.hide_output = True

    def handle_startendtag(self, tag, attrs):
        if tag == "br":
            self._buf.append("\n")

    def handle_endtag(self, tag):
        if tag == "p":
            self._buf.append("\n")
        elif tag in ("script", "style"):
            self.hide_output = False

    def handle_data(self, text):
        if text and not self.hide_output:
            self._buf.append(re.sub(r"\s+", " ", text))

    # noinspection SpellCheckingInspection
    def handle_entityref(self, name):
        if name in name2codepoint and not self.hide_output:
            c = chr(name2codepoint[name])
            self._buf.append(c)

    # noinspection SpellCheckingInspection
    def handle_charref(self, name):
        if not self.hide_output:
            n = int(name[1:], 16) if name.startswith("x") else int(name)
            self._buf.append(chr(n))

    def get_text(self):
        return re.sub(r" +", " ", "".join(self._buf))


class Utils:
    @staticmethod
    def dt_timestamp(dt):
        return time.mktime(dt.timetuple())

    @staticmethod
    def datetime_from_unix_time(unix_time):
        return datetime.fromtimestamp(float(unix_time / 1000))

    @staticmethod
    def datetime_to_unix_time(dt):
        return int(Utils.dt_timestamp(dt) * 1000)

    @staticmethod
    def get_default_list_display(self, list_prev=None, list_last=None):
        list_display = []
        if list_prev:
            list_display.extend(list_prev)
        for field in self._meta.fields:
            list_display.append(field.name)
        if list_last:
            list_display.extend(list_last)
        return tuple(list_display)

    @staticmethod
    def str_to_int(string, default=None):
        value = default
        try:
            value = int(string)
        except TypeError:
            pass
        except ValueError:
            pass
        return value

    @staticmethod
    def int_str_to_bool(string, default=False):
        value = default
        if string is not None:
            int_str = Utils.str_to_int(string.strip())
            if string and int_str is not None:
                value = bool(int_str)

        return value

    @staticmethod
    def str_to_float(string, default=None):
        value = default
        try:
            value = float(
                string.strip().replace(",", ".").replace(" ", "").replace(" ", "")
            )
        except TypeError:
            pass
        except ValueError:
            pass
        return value

    @staticmethod
    def get_environ_int(np, default=None):
        # type: (str, int) -> int
        s = os.environ.get(np)
        if s is None:
            res = default
        else:
            res = Utils.str_to_int(s)
            if res is None:
                res = default
        return res

    @staticmethod
    def get_environ_bool(np, default=None):
        # type: (str, bool) -> bool
        res = default
        s = os.environ.get(np)
        if s:
            s = s.lower()
            if s == "true":
                res = True
            elif s == "false":
                res = False
        return res

    @staticmethod
    def str_add(primary_string, added_string, delimiter="; "):
        if not isinstance(primary_string, str):
            primary_string = str(primary_string)
        if not isinstance(added_string, str):
            added_string = str(added_string)
        res = primary_string
        if added_string and len(added_string) != 0:
            res += ("" if not res else delimiter) + added_string
        return res

    @staticmethod
    def get_md5_hash_str(str_):
        # type: (str) -> str
        return hashlib.md5(str(str_).encode("utf-8")).hexdigest()

    @staticmethod
    def put_into_text_storage(text_storage, text, max_length):
        # type: ([], str, int) -> []

        max_length = int(max_length)
        if len(text_storage) == 0:
            text_storage.append("")
        ci = len(text_storage) - 1
        if len(text_storage[ci] + text) <= max_length:
            text = text_storage[ci] + text
            text_storage[ci] = text
        else:
            s_m = []
            p_c = math.ceil(len(text) / max_length)
            for i in range(p_c):
                s_m.append(text[max_length * i : max_length * (i + 1)])
            if not text_storage[ci]:
                text_storage.pop(ci)
            text_storage.extend(s_m)

        return text_storage

    @staticmethod
    def get_calling_function_filename(called_function, pass_cnt=1):
        sts = inspect.stack(0)
        i = 0
        for st in sts:
            i += 1
            if st.function == called_function:
                break
        i = i + (pass_cnt - 1)
        calling_function_filename = None
        if i > 0:
            try:
                calling_function_filename = sts[i].filename
            except IndexError:
                pass
        return calling_function_filename

    @staticmethod
    def is_call_from_child() -> bool:
        sts = inspect.stack(0)
        try:
            return sts[1].function == sts[2].function
        except IndexError:
            pass

    @staticmethod
    def get_cur_func_name() -> str:
        sts = inspect.stack(0)
        try:
            return sts[1].function
        except IndexError:
            pass

    @staticmethod
    def get_environ_languages_dict(np, default=None) -> dict:
        res = {}
        default = default or {"ru": "Русский", "en": "English"}
        l_fe = os.environ.get(np)
        if l_fe:
            l_l = l_fe.split(":")
            for l_c in l_l:
                l_r = l_c.split("=")
                if len(l_r) == 2:
                    res[l_r[0]] = l_r[1]
        if not res:
            res = default
        return res

    @staticmethod
    def update_dict(args: dict, arg_ext: dict) -> dict:
        if arg_ext:
            args.update(arg_ext)
        return args

    @staticmethod
    def dt_str_normalize(date_str: str):
        return (date_str or "").replace(",", ".").replace("/", ".")

    @classmethod
    def get_datetime_by_str(
        cls, date_str: str, fmt_date_usr="%d.%m.%Y", fmt_date_usr_short="%d.%m.%y"
    ) -> datetime:
        date_str = cls.dt_str_normalize(date_str)
        try:
            return datetime.strptime(date_str, fmt_date_usr).astimezone()
        except (TypeError, ValueError):
            try:
                return datetime.strptime(date_str, fmt_date_usr_short).astimezone()
            except (TypeError, ValueError):
                pass

    @classmethod
    def get_date_by_str(
        cls, date_str: str, fmt_date_usr="%d.%m.%Y", fmt_date_usr_short="%d.%m.%y"
    ) -> date:
        dt = cls.get_datetime_by_str(
            date_str, fmt_date_usr=fmt_date_usr, fmt_date_usr_short=fmt_date_usr_short
        )
        if dt:
            return dt.date()

    @staticmethod
    def html_to_text(html):
        """
        Given a piece of HTML, return the plain text it contains.
        This handles entities and char refs, but not javascript and stylesheets.
        """
        parser = _HTMLToText()
        try:
            parser.feed(html)
            parser.close()
        except Exception as e:  # HTMLParseError: No good replacement?
            print(e)
        return parser.get_text()

    STOP_ALL_RUNNING_SCHEDULERS = False

    @staticmethod
    def scheduler_run(func: callable, cron_str: str, sl_time=15, *args, **kwargs):
        if func is None:
            return
        lgz = BotLogger.get_instance()
        lgz.debug(
            f"scheduler {func.__name__} cron string - {cron_str}, args={args}, kwargs={kwargs}"
        )
        itr = croniter(cron_str, datetime.now().astimezone())
        itr.get_next(datetime)
        lgz.debug(
            f"scheduler {func.__name__} next run - {itr.get_current(datetime)} ({cron_str}), args={args}, kwargs={kwargs}"
        )
        while not Utils.STOP_ALL_RUNNING_SCHEDULERS:
            try:
                if datetime.now().astimezone() >= itr.get_current(datetime):
                    dtn = itr.get_next(datetime)
                    func(*args, **kwargs)
                    lgz.debug(
                        f"scheduler {func.__name__} next run - {dtn} ({cron_str}), args={args}, kwargs={kwargs}"
                    )
            except Exception as e:
                lgz.exception(f"Exception:{e}")
            finally:
                time.sleep(sl_time)


class ExtList(list):
    def __init__(self, no_double=False):
        self.no_double = no_double
        super(ExtList, self).__init__()

    def append(self, obj):
        if not self.no_double or obj not in self:
            super(ExtList, self).append(obj)

    def extend(self, list_add):
        if self.no_double:
            set_main = set(self)
            set_add = set(list_add)
            set_add_nd = set_add - set_main
            list_add = list(set_add_nd)
        super(ExtList, self).extend(list_add)

    def get(self, index):
        try:
            return self[index]
        except IndexError:
            pass


class BotLogger(logging.Logger):
    __instance = None

    # noinspection PyProtectedMember,PyUnresolvedReferences
    def __new__(cls, **kwargs):
        instance = None
        if not cls.__instance:
            instance_name = os.environ.get("MAX_BOT_LOGGING_NAME") or "MaxBot"
            instance = logging.getLogger(instance_name)
            # noinspection SpellCheckingInspection
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s[%(threadName)s-%(thread)d] - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s"
            )

            log_file_max_bytes = (
                Utils.get_environ_int("MAX_BOT_LOGGING_FILE_MAX_BYTES") or 10485760
            )
            log_file_backup_count = (
                Utils.get_environ_int("MAX_BOT_LOGGING_FILE_BACKUP_COUNT") or 10
            )
            fh = RotatingFileHandler(
                f"bots_{instance_name}.log",
                mode="a",
                maxBytes=log_file_max_bytes,
                backupCount=log_file_backup_count,
                encoding="UTF-8",
            )
            fh.setFormatter(formatter)
            instance.addHandler(fh)

            sh = logging.StreamHandler(stream=sys.stdout)
            sh.setFormatter(formatter)
            instance.addHandler(sh)

            cls.trace_requests = (
                Utils.get_environ_bool("MAX_BOT_TRACE_REQUESTS") or False
            )
            cls.logging_level = os.environ.get("MAX_BOT_LOGGING_LEVEL") or "INFO"
            cls.logging_level = logging._nameToLevel.get(cls.logging_level)
            if cls.logging_level is None:
                instance.setLevel(logging.DEBUG if cls.trace_requests else logging.INFO)
            else:
                instance.setLevel(cls.logging_level)
            instance.trace_requests = cls.trace_requests
        return instance

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            cls.__instance = BotLogger()
        return cls.__instance


class Scheduler:
    lgz = BotLogger.get_instance()

    def __init__(self, sl_time=15, fr_level=1) -> None:
        super().__init__()
        self._running = True

        # Частота срабатывания таймера в процессе, сек.
        self.sl_time = sl_time
        # Порог срабатывания таймера при старте — % времени прошедшего от прошлого запуска к общей длительности итерации
        self.fr_level = fr_level

    def terminate(self):
        self._running = False

    def run(self, func: callable, cron_str: str, *args, **kwargs):
        if func is None:
            return
        self.lgz.debug(
            f"scheduler {func.__name__} cron string - {cron_str}, args={args}, kwargs={kwargs}"
        )
        itr = croniter(cron_str, datetime.now().astimezone())
        itr_p = croniter(cron_str, datetime.now().astimezone())
        itr_p.get_prev(datetime)
        dt_prev = itr_p.get_current(datetime)
        dt_cur = itr.get_current(datetime)
        itr.get_next(datetime)
        dt_next = itr.get_current(datetime)
        pr_prev = 100 * ((dt_cur - dt_prev) / (dt_next - dt_prev))
        if pr_prev <= self.fr_level:
            self.lgz.debug(
                f"scheduler {func.__name__} {pr_prev:.4f}% from previous running: next run modify to {itr.get_current(datetime)}. First run level: {self.fr_level:.4f} %"
            )
            itr.get_prev(datetime)
        self.lgz.debug(
            f"scheduler {func.__name__} next run - {itr.get_current(datetime)} ({cron_str}), args={args}, kwargs={kwargs} [{pr_prev:.4f} %]"
        )
        while self._running:
            try:
                if datetime.now().astimezone() >= itr.get_current(datetime):
                    dtn = itr.get_next(datetime)
                    func(*args, **kwargs)
                    self.lgz.debug(
                        f"scheduler {func.__name__} next run - {dtn} ({cron_str}), args={args}, kwargs={kwargs}"
                    )
            except Exception as e:
                self.lgz.exception(f"Exception:{e}")
            finally:
                time.sleep(self.sl_time)

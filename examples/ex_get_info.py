import os

from max_client import ApiClient, BotCommand, BotPatch, BotsApi, Configuration

conf = Configuration()
conf.api_key["access_token"] = os.environ.get("MAX_BOT_API_TOKEN")
client = ApiClient(conf)
api = BotsApi(client)
info = api.get_my_info()
print(info)


commands = [
    BotCommand("start_test", "начать"),
    BotCommand("menu", "показать меню"),
    BotCommand("list", "список всех чатов"),
]

bp = BotPatch(commands=commands, description="Новое описание для бота")
info = api.edit_my_info(bp)
print(info)

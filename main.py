import logging
import os

from telegram.ext import Updater, CommandHandler

from daibot.utils import start, dice, help
from daibot.roll import newroll, joinroll, nowroll, listroll, statusroll

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

TOKEN = os.environ.get("DAIBOT_TOKEN", None)
if TOKEN is None:
    logging.error("Fatal error: token not found, abort!")
    import sys

    sys.exit(1)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

handlers = [
    ["start", start],
    ["help", help],
    ["dice", dice],
    ["newroll", newroll],
    ["joinroll", joinroll],
    ["nowroll", nowroll],
    ["listroll", listroll],
    ["statusroll", statusroll],
]
for text, command in handlers:
    handler = CommandHandler(text, command)
    dispatcher.add_handler(handler)

updater.start_polling()
updater.idle()

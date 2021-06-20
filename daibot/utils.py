import random
import time

import telegram


def start(update, context):
    if update.message.chat.type == "private":
        context.bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        context.bot.send_message(chat_id=update.message.chat_id, text="Hi!")
    else:
        context.bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        msg = context.bot.send_message(chat_id=update.message.chat_id, text="Hi!")
        time.sleep(5)
        context.bot.delete_message(
            chat_id=update.message.chat_id, reply_to_message_id=msg.message_id
        )


def help(update, context):
    context.bot.send_chat_action(
        chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
    )
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="""
/start - Say Hi!
/help - Get help
/newroll - Create a new roll
/joinroll - Join current active roll
/nowroll - Roll owner roll now
/listroll - List all users in current roll
/statusroll - Show current roll status
""",
    )


def dice(update, context):
    context.bot.send_chat_action(
        chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
    )
    update.message.reply_text(
        f"You have rolled {random.randint(1, 6)}",
        reply_to_message_id=update.message.message_id,
    )

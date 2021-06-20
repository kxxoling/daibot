import random
import csv

import telegram


def newroll(update, context):
    if update.message.chat.type == "private":
        context.bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Roll is not available in private chat.",
        )
    else:
        groupid = update._effective_chat.id
        username = update._effective_user.username
        if not groupid in context.chat_data:
            context.chat_data[groupid] = [username]
            context.bot.send_message(
                update.message.chat_id,
                "New Roll created. The owner is @" + username,
            )
        else:
            context.bot.send_message(
                update.message.chat_id,
                "Roll already exists.",
            )


def joinroll(update, context):
    if update.message.chat.type == "private":
        context.bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Roll is not available in private chat.",
        )
    else:
        username = update._effective_user.username
        groupid = update._effective_chat.id
        if not groupid in context.chat_data:
            update.message.reply_text(
                "No exists Roll. Please use /newroll to create one.",
                reply_to_message_id=update.message.message_id,
            )
        else:
            if not username in context.chat_data[groupid]:
                context.chat_data[groupid].append(username)
                update.message.reply_text(
                    f"@{username} have joined the list successfully.",
                    reply_to_message_id=update.message.message_id,
                )
            else:
                update.message.reply_text(
                    "You are already in the list.",
                    reply_to_message_id=update.message.message_id,
                )


def nowroll(update, context):
    if update.message.chat.type == "private":
        context.bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Roll is not available in private chat.",
        )
    else:
        username = update._effective_user.username
        groupid = update._effective_chat.id
        if not groupid in context.chat_data:
            update.message.reply_text(
                'No exists Roll. Please use "newroll" to create one.',
                reply_to_message_id=update.message.message_id,
            )
        else:
            if username != context.chat_data[groupid][0]:
                update.message.reply_text(
                    "You have no right to roll. Please contact the owner @%s"
                    % context.chat_data[groupid][0],
                    reply_to_message_id=update.message.message_id,
                )
            else:
                rolldict = {
                    i: random.randint(1, 100) for i in context.chat_data[groupid]
                }
                sorted_roll = sorted(rolldict.items(), key=lambda kv: kv[1])

                with open(f"{groupid}-roll.log", "a+") as f:
                    for k, v in sorted_roll:
                        f.write(f"{k},{v}\n")

                text = "\n".join([f"@{k} have rolled {v}\n" for k, v in sorted_roll])

                text += f"\n Congratulations on @{sorted_roll[-1][0]}!"

                context.bot.send_message(chat_id=update.message.chat_id, text=text)
                context.chat_data.pop(groupid)


def listroll(update, context):
    if update.message.chat.type == "private":
        context.bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Roll is not available in private chat.",
        )
    else:
        groupid = update._effective_chat.id

        if not groupid in context.chat_data:
            update.message.reply_text(
                'No exists Roll. Use "/newroll" to create one.',
                reply_to_message_id=update.message.message_id,
            )
        else:
            text = "In this round, we have:\n" + "\n".join(
                [username for username in context.chat_data[groupid]]
            )
            context.bot.send_message(chat_id=update.message.chat_id, text=text)


def statusroll(update, context):
    if update.message.chat.type == "private":
        context.bot.send_chat_action(
            chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
        )
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Roll is not available in private chat.",
        )
    else:
        groupid = update._effective_chat.id
        csv_path = f"{groupid}-roll.log"

        try:
            with open(csv_path) as csv_file:
                reader = csv.DictReader(csv_file, fieldnames=["name", "score"])
                text = "\n".join([f'{row["name"]} {row["score"]}' for row in reader])
                context.bot.send_message(chat_id=update.message.chat_id, text=text)
        except FileNotFoundError:
            context.bot.send_message(
                chat_id=update.message.chat_id, text="Nothing found, see you next time."
            )

from time import time
from uuid import uuid4

from bot import (
    bot,
    bot_name,
    config_dict,
    DATABASE_URL,
    user_data,
)
from bot.helper.ext_utils.db_handler import DbManager
from bot.helper.ext_utils.status_utils import get_readable_time
from bot.helper.ext_utils.shortener import short_url
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.button_build import ButtonMaker
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage, sendLogMessage

from pyrogram.filters import command
from pyrogram.handlers import MessageHandler


async def checking_access(user_id, button=None):
    if not config_dict["TOKEN_TIMEOUT"]:
        return (
            None,
            button
        )
    user_data.setdefault(
        user_id,
        {}
    )
    data = user_data[user_id]
    if DATABASE_URL:
        data["time"] = await DbManager().get_token_expire_time(user_id)
    expire = data.get("time")
    isExpired = (
        expire is None
        or expire is not None
        and (time() - expire) > config_dict["TOKEN_TIMEOUT"]
    )
    if isExpired:
        token = (
            data["token"]
            if expire is None
            and "token" in data
            else str(uuid4())
        )
        inittime = time()
        if expire is not None:
            del data["time"]
        data["token"] = token
        data["inittime"] = inittime
        if DATABASE_URL:
            await DbManager().update_user_token(
                user_id,
                token,
                inittime
            )
        user_data[user_id].update(data)
        if button is None:
            button = ButtonMaker()
        button.ubutton(
            "Get New Token",
            short_url(f"https://redirect.z-mirror.eu.org/{bot_name}/{token}")
        )
        tmsg = (
            "Your <b>Token</b> is expired. Get a new one."
            f"\n<b>Token Validity</b>: {get_readable_time(config_dict["TOKEN_TIMEOUT"])}\n"
        )
        return (
            tmsg,
            button
        )
    return (
        None,
        button
    )


async def start(client, message):
    tag = message.from_user.mention
    if (
        len(message.command) > 1
        and len(message.command[1]) == 36
    ):
        userid = message.from_user.id
        input_token = message.command[1]
        if DATABASE_URL:
            stored_token = await DbManager().get_user_token(userid)
            if stored_token is None:
                return await sendMessage(
                    message,
                    "This token is not associated with your account.\n\nPlease generate your own token."
                )
            if input_token != stored_token:
                return await sendMessage(
                    message,
                    "Invalid token.\n\nPlease generate a new one."
                )
            inittime = await DbManager().get_token_init_time(userid)
            duration = time() - inittime # type: ignore
            if (
                config_dict["MINIMUM_DURATOIN"]
                and (
                    duration < config_dict["MINIMUM_DURATOIN"]
                )
            ):
                await DbManager().update_user_tdata(
                    userid,
                    0,
                    0
                )
                await sendLogMessage(
                    message,
                    f"#BYPASS\n\nShortener bypass detected.",
                    tag
                )
                return await sendMessage(
                    message,
                    "Shortener bypass detected.\n\nPlease generate a new token.\n\n<b>Don't try to bypass it, next time ban.</b>"
                )
        if userid not in user_data:
            return await sendMessage(
                message,
                "This token is not yours!\n\nKindly generate your own."
            )
        data = user_data[userid]
        if (
            "token" not in data
            or data["token"] != input_token
        ):
            return await sendMessage(
                message,
                "Token already used!\n\nKindly generate a new one."
            )
        duration = time() - data["inittime"]
        if (
            config_dict["MINIMUM_DURATOIN"]
            and (
                duration < config_dict["MINIMUM_DURATOIN"]
            )
        ):
            del data["token"]
            await sendLogMessage(
                message,
                f"#BYPASS\n\nShortener bypass detected.",
                tag
            )
            return await sendMessage(
                message,
                "Shortener bypass detected.\n\nPlease generate a new token.\n\n<b>Don't try to bypass it, next time ban.</b>"
            )
        token = str(uuid4())
        ttime = time()
        data["token"] = token
        data["time"] = ttime
        user_data[userid].update(data)
        if DATABASE_URL:
            await DbManager().update_user_tdata(
                userid,
                token,
                ttime
            )
        msg = (
            "Your token refreshed successfully!\n"
            f"Validity: {get_readable_time(int(config_dict["TOKEN_TIMEOUT"]))}\n\n"
            "<b>Your Limites:</b>\n"
            f"{config_dict["USER_MAX_TASKS"]} parallal tasks.\n"
        )
        return await sendMessage(
            message,
            msg
        )
    elif (
        config_dict["DM_MODE"]
        and message.chat.type != message.chat.type.SUPERGROUP
    ):
        start_string = "Bot Started.\n" \
                       "Now I will send all of your stuffs here.\n" \
                       "Use me at: @TellYcloud_Bots"
    elif (
        not config_dict["DM_MODE"]
        and message.chat.type != message.chat.type.SUPERGROUP
        and not await CustomFilters.authorized(
            client,
            message
        )
    ):
        start_string = "Sorry, you cannot use me in private!"
    elif (
        not config_dict["DM_MODE"]
        and message.chat.type != message.chat.type.SUPERGROUP
        and await CustomFilters.authorized(
            client,
            message
        )
    ):
        start_string = "There's nothing to Start here.\n" \
                       "Try something else or read HELP"
    else:
        start_string = "Start me in DM, not in the group.\n" \
                       f"cc: {tag}"
    await sendMessage(
        message,
        start_string
    )


bot.add_handler( # type: ignore
    MessageHandler(
        start,
        filters=command(
            BotCommands.StartCommand
        )
    )
)

from aiofiles.os import (
    remove,
    path as aiopath
)
from pyrogram.filters import (
    command,
    regex
)
from pyrogram.handlers import (
    MessageHandler,
    CallbackQueryHandler
)

from bot import (
    bot,
    aria2,
    task_dict,
    task_dict_lock,
    OWNER_ID,
    user_data,
    LOGGER,
    config_dict,
    qbittorrent_client,
)
from bot.helper.ext_utils.bot_utils import (
    bt_selection_buttons,
    sync_to_async
)
from bot.helper.ext_utils.status_utils import (
    get_readable_file_size,
    getTaskByGid,
    MirrorStatus
)
from bot.helper.ext_utils.task_manager import limit_checker
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import (
    auto_delete_message,
    delete_links,
    sendMessage,
    sendStatusMessage,
    deleteMessage,
)


async def select(_, message):
    if not config_dict["BASE_URL"]:
        smsg = await sendMessage(
            message,
            "Base URL not defined!"
        )
        await auto_delete_message(
            message,
            smsg
        )
        return
    user_id = message.from_user.id
    msg = message.text.split()
    if len(msg) > 1:
        gid = msg[1]
        task = await getTaskByGid(gid)
        if task is None:
            smsg = await sendMessage(
                message,
                f"GID: <code>{gid}</code> Not Found."
            )
            await auto_delete_message(
                message,
                smsg
            )
            return
    elif reply_to_id := message.reply_to_message_id:
        async with task_dict_lock:
            task = task_dict.get(reply_to_id)
        if task is None:
            smsg = await sendMessage(
                message,
                "This is not an active task!"
            )
            await auto_delete_message(
                message,
                smsg
            )
            return
    elif len(msg) == 1:
        msg = (
            "Reply to an active /cmd which was used to start the download or add gid along with cmd\n\n"
            + "This command mainly for selection incase you decided to select files from already added torrent. "
            + "But you can always use /cmd with arg `s` to select files before download start."
        )
        smsg = await sendMessage(
            message,
            msg
        )
        await auto_delete_message(
            message,
            smsg
        )
        return

    if (
        OWNER_ID != user_id
        and task.listener.userId != user_id
        and (
            user_id not in user_data
            or not user_data[user_id].get("is_sudo")
        )
    ):
        smsg = await sendMessage(
            message,
            "This task is not for you!"
        )
        await auto_delete_message(
            message,
            smsg
        )
        return
    if await sync_to_async(task.status) not in [
        MirrorStatus.STATUS_DOWNLOADING,
        MirrorStatus.STATUS_PAUSED,
        MirrorStatus.STATUS_QUEUEDL,
    ]:
        smsg = await sendMessage(
            message,
            "Task should be in download or pause (incase message deleted by wrong) or queued status (incase you have used torrent file)!",
        )
        await auto_delete_message(
            message,
            smsg
        )
        return
    if (
        task.name().startswith("[METADATA]") or
        task.name().startswith("Trying")
    ):
        smsg = await sendMessage(
            message,
            "Try after downloading metadata finished!"
        )
        await auto_delete_message(
            message,
            smsg
        )
        return

    try:
        id_ = task.gid()
        if not task.queued:
            if task.listener.isQbit:
                await sync_to_async(task.update)
                id_ = task.hash()
                await sync_to_async(
                    qbittorrent_client.torrents_pause,
                    torrent_hashes=id_
                )
            else:
                await sync_to_async(task.update)
                try:
                    await sync_to_async(
                        aria2.client.force_pause,
                        id_
                    )
                except Exception as e:
                    LOGGER.error(
                        f"{e} Error in pause, this mostly happens after abuse aria2"
                    )
        task.listener.select = True
    except:
        smsg = await sendMessage(
            message,
            "This is not a bittorrent task!"
        )
        await auto_delete_message(
            message,
            smsg
        )
        return

    SBUTTONS = bt_selection_buttons(id_)
    msg = "Your download paused. Choose files then press Done Selecting button to resume downloading."
    await sendMessage(
        message,
        msg,
        SBUTTONS
    )


async def get_confirm(_, query):
    user_id = query.from_user.id
    data = query.data.split()
    message = query.message
    task = await getTaskByGid(data[2])
    if task is None:
        await query.answer(
            "This task has been cancelled!",
            show_alert=True
        )
        await deleteMessage(message)
        return
    if user_id != task.listener.userId:
        await query.answer(
            "This task is not for you!",
            show_alert=True
        )
    elif data[1] == "pin":
        await query.answer(
            data[3],
            show_alert=True
        )
    elif data[1] == "done":
        await query.answer()
        id_ = data[3]
        if hasattr(
            task,
            "seeding"
        ):
            if task.listener.isQbit:
                tor_info = (
                    await sync_to_async(
                        qbittorrent_client.torrents_info,
                        torrent_hash=id_
                    )
                )[0]
                path = tor_info.content_path.rsplit(
                    "/",
                    1
                )[0]
                res = await sync_to_async(
                    qbittorrent_client.torrents_files,
                    torrent_hash=id_
                )
                for f in res:
                    if f.priority == 0:
                        f_paths = [
                            f"{path}/{f.name}",
                            f"{path}/{f.name}.!qB"
                        ]
                        for f_path in f_paths:
                            if await aiopath.exists(f_path):
                                try:
                                    await remove(f_path)
                                except:
                                    pass
                if not task.queued:
                    await sync_to_async(
                        qbittorrent_client.torrents_resume,
                        torrent_hashes=id_
                    )
            else:
                res = await sync_to_async(
                    aria2.client.get_files,
                    id_
                )
                task.listener.size = sum(
                    int(file['length'])
                    for file in res
                    if file['selected'] == 'true'
                )
                LOGGER.info(f"Total size after selection: {get_readable_file_size(task.listener.size)}")
                if limit_exceeded := await limit_checker(task.listener):
                    LOGGER.info(f"Aria2 Limit Exceeded: {task.listener.name} | {get_readable_file_size(task.listener.size)}")
                    amsg = await task.listener.onDownloadError(limit_exceeded)
                    await sync_to_async(
                        aria2.client.remove,
                        id_
                    )
                    await delete_links(task.listener.message)
                    await auto_delete_message(
                        task.listener.message,
                        amsg
                    )
                    return
                for f in res:
                    if (
                        f["selected"] == "false" and
                        await aiopath.exists(f["path"])
                    ):
                        try:
                            await remove(f["path"])
                        except:
                            pass
                if not task.queued:
                    try:
                        await sync_to_async(aria2.client.unpause, id_)
                    except Exception as e:
                        LOGGER.error(
                            f"{e} Error in resume, this mostly happens after abuse aria2. Try to use select cmd again!"
                        )
        await sendStatusMessage(message)
        await deleteMessage(message)
    else:
        await deleteMessage(message)
        await task.cancel_task()


bot.add_handler( # type: ignore
    MessageHandler(
        select,
        filters=command(
            BotCommands.SelectCommand
        ) & CustomFilters.authorized
    )
)
bot.add_handler( # type: ignore
    CallbackQueryHandler(
        get_confirm,
        filters=regex("^sel")
    )
)

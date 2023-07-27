from AutoAnimeBot.modules.utils import (
    format_time,
    get_duration,
    get_filesize,
    tags_generator,
)
from AutoAnimeBot.modules.thumbnail import generate_thumbnail
from config import COMMENTS_GROUP_LINK, INDEX_CHANNEL_USERNAME
from pyrogram.types import Message
from AutoAnimeBot.modules.progress import upload_progress
import os
import time
from AutoAnimeBot.core.log import LOGGER
from AutoAnimeBot.modules.progress import t1, dcount

logger = LOGGER("Uploader")


async def upload_video(app, msg, file, id, tit, title, eid):
    global t1, dcount
    t1 = time.time()
    dcount = 1

    try:
        logger.info("Uploading --> " + title)
        c_time = time.time()
        duration = get_duration(file)
        size = get_filesize(file)
        ep_num = int(eid.split("-episode-")[1].strip())
        thumbnail, w, h = await generate_thumbnail(
            id, file, tit, ep_num, size, format_time(duration)
        )
        tags = tags_generator(tit)
        caption = f"🎥 **{title}**\n\n{tags}"
        await app.send_video_note(
            app.UPLOADS_CHANNEL_ID,
            video_note=file,
            thumb=thumbnail,
            duration=duration,
            file_name=os.path.basename(file),
            progress=upload_progress,
            progress_args=(title, msg, logger),
        )
        try:
            await msg.delete()
        except:
            pass
        try:
            os.remove(file)
        except:
            pass
        try:
            os.remove(thumbnail)
        except:
            pass

    except Exception as e:
        logger.warning(str(e))

    return  # You can return something meaningful here if needed, or just remove the return statement.

from config import COMMENTS_GROUP_LINK, INDEX_CHANNEL_USERNAME
from pyrogram.types import Message
from AutoAnimeBot.modules.progress import upload_progress
import os
import time
from AutoAnimeBot.core.log import LOGGER
from AutoAnimeBot.modules.progress import t1, dcount
from AutoAnimeBot.modules.utils import get_duration

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
        thumbnail_url = "https://telegra.ph/file/99bf642c8bd3f465af0ee.png"
        tags = tags_generator(tit)
        caption = f"🎥 **{title}**\n\n{tags}"
        await app.send_video_note(
            app.UPLOADS_CHANNEL_ID,
            video_note=file,
            thumb=thumbnail_url,  # Use the provided image URL as the thumbnail
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

    except Exception as e:
        logger.warning(str(e))

    return 

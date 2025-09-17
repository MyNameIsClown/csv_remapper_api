from app.scheduler_config import scheduler
import logging
import os
import logging
from datetime import datetime, timedelta

LOGGER = logging.getLogger(__name__)

FILES = ["files", timedelta(minutes=5)]
RESPONSE_FILES = ["files_response", timedelta(minutes=1)]
CONFIG_FILES = ["config_files", timedelta(minutes=1)]

async def delete_files():
    """Deletes files form response files/config/response folder when it has more than X minutes of lifetime"""
    try:
        if not os.path.exists(FILES[0]):
            LOGGER.warning(f"The folder {FILES[0]} not exists yet")
            return
        if not os.path.exists(RESPONSE_FILES[0]):
            LOGGER.warning(f"The folder {RESPONSE_FILES[0]} not exists yet")
            return
        if not os.path.exists(CONFIG_FILES[0]):
            LOGGER.warning(f"The folder {CONFIG_FILES[0]} not exists yet")
            return

        check_folder_files_lifetime(FILES[0], FILES[1])
        check_folder_files_lifetime(RESPONSE_FILES[0], RESPONSE_FILES[1])
        check_folder_files_lifetime(CONFIG_FILES[0], CONFIG_FILES[1])

    except Exception as e:
        LOGGER.error(f"Error deleting file: {e}") 

def check_folder_files_lifetime(folder, lifetime):
    now = datetime.now()
    for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)

            # Solo procesar archivos normales
            if not os.path.isfile(filepath):
                check_folder_files_lifetime(filepath, lifetime)

            # Hora de última modificación
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            age = now - mtime

            if age > lifetime:
                os.remove(filepath)
                LOGGER.info(f"🗑️ Delete: {filename} (lifetime: {age})")

@scheduler.scheduled_job('interval', seconds=10)
async def remove_files():
    await delete_files()
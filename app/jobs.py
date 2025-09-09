from app.scheduler_config import scheduler
import logging
import os
import logging
from datetime import datetime, timedelta

LOGGER = logging.getLogger(__name__)

FILES_DIR = "files"  # Upload file folder
RESPONSE_FILES_DIR = "files_response"  # Response file folder
FILES_DIR_MAX_AGE = timedelta(minutes=5)
RESPONSE_FILES_DIR_MAX_AGE = timedelta(minutes=1)

async def delete_expired_files():
    """Deletes files form files folder when it has more than 5 minutes of lifetime"""
    try:
        now = datetime.now()

        if not os.path.exists(FILES_DIR):
            LOGGER.warning(f"The folder {FILES_DIR} not exists yet")
            return

        for filename in os.listdir(FILES_DIR):
            filepath = os.path.join(FILES_DIR, filename)

            # Solo procesar archivos normales
            if not os.path.isfile(filepath):
                continue

            # Hora de última modificación
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            age = now - mtime

            if age > FILES_DIR_MAX_AGE:
                os.remove(filepath)
                LOGGER.info(f"🗑️ Delete: {filename} (lifetime: {age})")

    except Exception as e:
        LOGGER.error(f"Error deleting file: {e}")

async def delete_response_files():
    """Deletes files form response files folder when it has more than  minutes of lifetime"""
    try:
        now = datetime.now()

        if not os.path.exists(RESPONSE_FILES_DIR):
            LOGGER.warning(f"The folder {RESPONSE_FILES_DIR} not exists yet")
            return

        for filename in os.listdir(RESPONSE_FILES_DIR):
            filepath = os.path.join(RESPONSE_FILES_DIR, filename)

            # Solo procesar archivos normales
            if not os.path.isfile(filepath):
                continue

            # Hora de última modificación
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            age = now - mtime

            if age > RESPONSE_FILES_DIR_MAX_AGE:
                os.remove(filepath)
                LOGGER.info(f"🗑️ Delete: {filename} (lifetime: {age})")

    except Exception as e:
        LOGGER.error(f"Error deleting file: {e}")

@scheduler.scheduled_job('interval', seconds=10)
async def remove_files():
    await delete_response_files()
    await delete_expired_files()
from app.scheduler_config import scheduler
import logging
import os
import logging
from datetime import datetime, timedelta

LOGGER = logging.getLogger(__name__)

FILES_DIR = "files"  # carpeta donde subes los archivos
MAX_AGE = timedelta(minutes=5)

async def delete_expired_files():
    """Elimina los archivos de la carpeta files con más de 5 min de antigüedad"""
    try:
        now = datetime.now()

        if not os.path.exists(FILES_DIR):
            LOGGER.warning(f"La carpeta {FILES_DIR} no existe todavía.")
            return

        for filename in os.listdir(FILES_DIR):
            filepath = os.path.join(FILES_DIR, filename)

            # Solo procesar archivos normales
            if not os.path.isfile(filepath):
                continue

            # Hora de última modificación
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            age = now - mtime

            if age > MAX_AGE:
                os.remove(filepath)
                LOGGER.info(f"🗑️ Eliminado: {filename} (antigüedad: {age})")

    except Exception as e:
        LOGGER.error(f"Error eliminando archivos: {e}")

@scheduler.scheduled_job('interval', seconds=10)
async def remove_files():
    await delete_expired_files()
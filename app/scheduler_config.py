from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

# Scheduler global
scheduler = AsyncIOScheduler(timezone=utc)

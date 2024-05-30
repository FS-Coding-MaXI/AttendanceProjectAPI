import logging
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from repositories.class_repository import get_all_classes
from services.meeting_service import create_meeting

logging.basicConfig(level=logging.DEBUG)

scheduler = AsyncIOScheduler()


async def create_weekly_meetings():
    classes = get_all_classes()
    for class_ in classes:
        create_meeting(class_.id)


def start_scheduler():
    scheduler.add_job(
        create_weekly_meetings, "interval", weeks=1, next_run_time=datetime.now()
    )
    scheduler.start()

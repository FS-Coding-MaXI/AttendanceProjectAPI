import logging
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from repositories.class_repository import get_all_classes
from services.meeting_service import create_meeting

logging.basicConfig(level=logging.DEBUG)

scheduler = AsyncIOScheduler()


async def create_weekly_meetings():
    logging.debug("Creating weekly meetings")
    classes = get_all_classes()
    logging.debug(f"Classes: {classes}")
    for class_ in classes:
        logging.debug(f"Creating meeting for class {class_.id}")
        create_meeting(class_.id)


def start_scheduler():
    scheduler.add_job(
        create_weekly_meetings, "interval", weeks=1, next_run_time=datetime.now()
    )
    scheduler.start()

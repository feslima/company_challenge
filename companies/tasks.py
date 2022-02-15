from celery import Celery
from celery.schedules import crontab

from core.celery import app as celery_app

from .services import update_companies


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    # Check each day at 05:00 (server local time) for company updates
    sender.add_periodic_task(
        crontab(hour=5), update_company_task.s(), name="Daily company update."
    )


@celery_app.task
def update_company_task():
    update_companies()

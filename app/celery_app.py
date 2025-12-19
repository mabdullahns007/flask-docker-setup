from celery import Celery, Task
from flask import Flask
from datetime import timedelta

CELERY_CONFIG = dict(
    broker_url="redis://redis:6379/0",
    result_backend="redis://redis:6379/0",
    task_ignore_result=True,
    beat_schedule={
        "daily-data-sync": {
            "task": "data_sync_task",
            "schedule": timedelta(days=1),  # Daily (every 24 hours)
        }
    },
)

celery_app = Celery(__name__)
celery_app.conf.update(CELERY_CONFIG)


def celery_init_app(app: Flask) -> Celery:
    app.config.from_mapping(
        CELERY=CELERY_CONFIG
    )
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

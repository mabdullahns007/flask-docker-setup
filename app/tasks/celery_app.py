import os
from celery import Celery, Task
from app import create_app
from datetime import timedelta


def celery_init_app(app) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask,)
    celery_app.conf.update(
        broker_url=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
        result_backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
        beat_schedule={
            "daily-data-sync": {
                "task": "data_sync_task",
                "schedule": timedelta(days=1),  # Daily (every 24 hours)
            }
        },
        task_ignore_result=False,
    )
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

# Initialize the Flask app and get the Celery instance for the worker
flask_app = create_app()
celery_app = flask_app.extensions["celery"]

# Import tasks to register them
import app.tasks.car_tasks

import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.constants import (DEFAULT_DATABASE_URI,DEFAULT_JWT_EXPIRATION_MINUTES,DEFAULT_SECRET_KEY)

db = SQLAlchemy()


def create_app(): 
    load_dotenv()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", DEFAULT_SECRET_KEY)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URI", DEFAULT_DATABASE_URI
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv(
        "JWT_SECRET_KEY", app.config["SECRET_KEY"]
    )
    expiration_env = os.getenv("JWT_EXPIRATION_MINUTES")
    try:
        expiration_minutes = (
            int(expiration_env) if expiration_env else DEFAULT_JWT_EXPIRATION_MINUTES
        )
    except ValueError:
        expiration_minutes = DEFAULT_JWT_EXPIRATION_MINUTES
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://redis:6379/0",
            result_backend="redis://redis:6379/0",
            task_ignore_result=True,
            beat_schedule={
                "daily-data-sync": {
                    "task": "data_sync_task",
                    "schedule": 86400.0, # Daily (every 24 hours) or use crontab in real app
                }
            }
        ),
    )
    app.config["JWT_EXPIRATION_MINUTES"] = expiration_minutes
    db.init_app(app)
    
    from app.celery_utils import celery_init_app
    celery_init_app(app)
    
    # Import tasks to ensure they are registered
    from app import tasks

    from app.routes.auth import auth_bp

    app.register_blueprint(auth_bp)

    return app


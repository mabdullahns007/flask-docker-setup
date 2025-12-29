import os
from celery import Celery, Task
from app import create_app
from datetime import timedelta
import requests
from app import db
from app.models.car import CarMake, CarModel, CarYear
from app.constants import URL


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

@celery_app.task(name="data_sync_task")
def carDataSync():
    headers = {
        'X-Parse-Application-Id': os.getenv('PARSE_APPLICATION_ID'),
        'X-Parse-Master-Key': os.getenv('PARSE_MASTER_KEY')
    }
    
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        
        synced_count = 0
        for item in results:
            year = item.get("Year")
            make_name = item.get("Make")
            model_name = item.get("Model")
            
            # Data Filtering
            if not year or not (2012 <= int(year) <= 2022):
                continue
                
            # Upsert CarMake
            make = CarMake.query.filter_by(name=make_name).first()
            if not make:
                make = CarMake(name=make_name)
                db.session.add(make)
                db.session.flush()  # To get make.id
            
            # Upsert CarModel
            model = CarModel.query.filter_by(name=model_name, make_id=make.id).first()
            if not model:
                model = CarModel(name=model_name, make_id=make.id)
                db.session.add(model)
                db.session.flush()  # To get model.id
                
            # Upsert CarYear
            car_year = CarYear.query.filter_by(year=int(year), model_id=model.id).first()
            if not car_year:
                car_year = CarYear(year=int(year), model_id=model.id)
                db.session.add(car_year)
            
            synced_count += 1
            
        db.session.commit()
        return f"Successfully synced {synced_count} records."
        
    except Exception as e:
        db.session.rollback()
        return f"Error during sync: {str(e)}"

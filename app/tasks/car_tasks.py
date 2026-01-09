import os
import requests
from app import db
from app.models.car import CarMake, CarModel, CarYear
from app.constants import URL
from celery_app import celery_app

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
        print(f"Synced {synced_count} records.")    
        
    except Exception as e:
        db.session.rollback()
        return f"Error during sync: {str(e)}"

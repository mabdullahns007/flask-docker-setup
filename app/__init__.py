import os
import time
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from app.constants import (DEFAULT_DATABASE_URI,DEFAULT_JWT_EXPIRATION_MINUTES,DEFAULT_SECRET_KEY)


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app(): 
    
    load_dotenv()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", DEFAULT_SECRET_KEY)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI", DEFAULT_DATABASE_URI)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", app.config["SECRET_KEY"])
    expiration_env = os.getenv("JWT_EXPIRATION_MINUTES")

    try:
        expiration_minutes = (int(expiration_env) if expiration_env else DEFAULT_JWT_EXPIRATION_MINUTES)
    except ValueError:
        expiration_minutes = DEFAULT_JWT_EXPIRATION_MINUTES

    app.config["JWT_EXPIRATION_MINUTES"] = expiration_minutes
    db.init_app(app)
<<<<<<< HEAD
    
    from app.celery_app import celery_init_app
    celery_init_app(app)
    
    # Import tasks to ensure they are registered
    from app import tasks
=======
    migrate.init_app(app, db)
    ma.init_app(app)

    from celery_app import celery_init_app
    celery_init_app(app)
>>>>>>> 6cec868 (Migrations for new Models, Celery Integration)

    from app.routes.auth.apis import auth_bp
    from app.routes.car.apis import car_bp
    from app.models import User, CarMake, CarModel, CarYear

    app.register_blueprint(auth_bp)
    app.register_blueprint(car_bp)

    with app.app_context():
        from flask_migrate import upgrade
        from sqlalchemy import text
        
        max_retries = 60  
        retry_interval = 2  
        
        print("Waiting for database to be ready...")
        for attempt in range(max_retries):
            try:
                with db.engine.connect() as connection:
                    connection.execute(text("SELECT 1"))
                    connection.commit()
                
                print(f"✓ Database connected successfully on attempt {attempt + 1}")
                
                print("Applying database migrations...")
                upgrade()
                print("✓ Database migrations applied successfully!")
                break
                
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"⏳ Attempt {attempt + 1}/{max_retries}: Database not ready yet, retrying in {retry_interval}s...")
                    time.sleep(retry_interval)
                else:
                    print(f"✗ Failed to connect to database after {max_retries} attempts")
                    print(f"✗ Last error: {e}")
                    raise
    return app

from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()
    app = Flask(__name__)

    from app.routes.ping import ping_bp
    app.register_blueprint(ping_bp)

    return app


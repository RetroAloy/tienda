import os
from webbrowser import get
from flask import Flask
from . import db
from . import producto
from . import auth


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = 'unakey',
        DATABASE_HOST = os.environ.get('DATABASE_FLASK_HOST'),
        DATABASE_USER = os.environ.get('DATABASE_FLASK_USER'),
        DATABASE_PASSWORD = os.environ.get('DATABASE_FLASK_PASSWORD'),
        DATABASE = os.environ.get('DATABASE_FLASK')
    )
    
    db.init_app(app)
    app.register_blueprint(producto.bp)
    app.register_blueprint(auth.bp)
    
    return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

# creating a database
db = SQLAlchemy()
DB_NAME = "database.db"


def createApp():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'spookyscarysecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import viewer
    from .authenciation import authenciator

    app.register_blueprint(viewer, url_prefix='/')
    app.register_blueprint(authenciator, url_prefix='/')

    from .models import User, Fuel_Quote

    create_database(app)

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Database created!")

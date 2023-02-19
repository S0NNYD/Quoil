from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#creating a database
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

    return app
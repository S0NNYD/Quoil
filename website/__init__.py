from flask import Flask

def createApp():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'spookyscarysecretkey'

    from .views import viewer
    from .authenciation import authenciator

    app.register_blueprint(viewer, url_prefix='/')
    app.register_blueprint(authenciator, url_prefix='/')

    return app
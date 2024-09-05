import os
from flask import Flask

def sentiment_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'KldU98e3@#rj09(dwfa)dcvP[!2]cdKajewqIwnLemNRdaqW'

    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    from .views import views
    
    app.register_blueprint(views, url_prefix='/')

    return app
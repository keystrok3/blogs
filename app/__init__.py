
""" 
    Package Constructor For The Application
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

moment = Moment()
db = SQLAlchemy()

# Application Factory: Will take the configuration used by the application
# and create the application, configure it, and initialize the extensions
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    moment.init_app(app)
    db.init_app(app)
    
    # api blueprint
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    return app
from flask import Flask
from flask_login import LoginManager

from model import db

import route.api
import route.principal

def create_app():

    app = Flask(__name__, instance_relative_config = True)
    app.config.from_pyfile('configuración.py')

    # Inicializamos la DB
    db.init_app(app)

    app.register_blueprint(route.api.bp)
    app.register_blueprint(route.principal.bp)

    route.api.jwt.init_app(app)
    route.principal.login_manager.init_app(app)

    print(app.url_map)

    return app
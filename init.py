from flask import Flask
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

app = Flask(__name__, instance_relative_config = True)
app.config.from_pyfile('configuración.py')

from model import db

# Inicializamos la DB
db.init_app(app)

# Inicializamos el Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'iniciar_sesión'
login_manager.login_message = 'Por favor, inicia sesión primero'

# Inicializamos el Flask JWT
jwt = JWTManager(app)
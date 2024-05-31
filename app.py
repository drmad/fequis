# from sqlalchemy import select
# from flask import render_template, request, redirect, flash, url_for, session
# from init import app
# from model import db, Usuario, Post
# import datetime
# from form import NuevoUsuario, IniciarSesión, EditarUsuario
# from flask_login import LoginManager, login_user, logout_user, current_user, login_required
# from argon2 import PasswordHasher
# from PIL import Image

from init import app, login_manager

import route.api
import route.principal




app.register_blueprint(route.api.bp)
app.register_blueprint(route.principal.bp)



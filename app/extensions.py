from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail
from flask_wtf import CSRFProtect
from flask_restplus import Api
from celery import Celery

login = LoginManager()
db = SQLAlchemy()
db_migrate = Migrate()
debug_toolbar = DebugToolbarExtension()
mail = Mail()
crsf=CSRFProtect()
api = Api()
celery = Celery()
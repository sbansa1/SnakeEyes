from flask import Blueprint


user = Blueprint("user", __name__,template_folder='templates')

from app.blueprints.user import views

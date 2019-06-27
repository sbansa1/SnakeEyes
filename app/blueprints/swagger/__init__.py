from flask import Blueprint

test = Blueprint("test", __name__)
from app.blueprints.swagger import views
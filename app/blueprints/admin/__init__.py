from flask import Blueprint

admin_blu = Blueprint("admin",__name__ ,template_folder='templates', url_prefix="/admin")

from app.blueprints.admin import views



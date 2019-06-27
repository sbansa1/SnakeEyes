from flask.blueprints import Blueprint

billing = Blueprint("billing", __name__, template_folder="templates")


from app.blueprints.billings import views


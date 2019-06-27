from flask import Blueprint


contact = Blueprint("contact",__name__, template_folder='templates')

from app.blueprints.contact.forms import ContactForm
from app.blueprints.contact import views
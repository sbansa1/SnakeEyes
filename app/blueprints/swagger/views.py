from flask_restplus import Resource

from app.blueprints.user.model import User
from app.extensions import api

user = User()

@api.route("/hello")
class HelloWorld(Resource):

    def get(self):
        return ""
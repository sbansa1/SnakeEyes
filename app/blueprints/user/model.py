from collections import OrderedDict
from time import time

import jwt
from flask import current_app
from flask_login import UserMixin
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

from app.blueprints.billings.models.creditcard import CreditCard
from app.blueprints.billings.models.subscriptions import Subscription
from app.extensions import db
from app.extensions import login
from app.lib.utility_sqlalchemy import AwareDateTime, ResourceMixin


class User(db.Model, UserMixin, ResourceMixin):

    __tablename__ = "users"
    ROLE = OrderedDict()
    ROLE["member"] = "MEMBER"
    ROLE["admin"] = "ADMIN"

    id = db.Column(db.Integer, primary_key=True)

    #Authentication

    role = db.Column(db.Enum(*ROLE, name="role_types", native_enum=False, server_default="member", index=True,
                             nullable= False))
    active = db.Column("is_active", db.Boolean, server_default="1", nullable=False)
    username = db.Column( db.String( 30 ), unique=True, index=True )
    email = db.Column( db.String( 128 ), unique=True, index=True, nullable=False )
    password = db.Column( db.String( 30 ), nullable=False, server_default='' )
    subscription = db.relationship(Subscription,backref="users",uselist=False,passive_deletes=True)
    creditcard = db.relationship(CreditCard, backref='users',passive_deletes=True, uselist=False)


    # Activity Tracking

    sign_in_count = db.Column( db.Integer, nullable=False, default=0)
    current_sign_in_on = db.Column(AwareDateTime())
    current_sign_in_ip = db.Column( db.String(45))
    last_sign_is_on = db.Column(AwareDateTime())

    #Personal Details
    name  = db.Column("name", db.String(128))
    payment_id = db.Column(db.String(128), unique = True)
    cancelled_subscription_on = db.Column(AwareDateTime())

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password = User.encrypt_password( kwargs.get("password", " "))

    @classmethod
    def find_by_identity(cls, identity):
        """Find a User by their e-mail or Username.
        :param identity: E-mail or Username
        :type identity: str
        :return: User instance
        """
        current_app.logger.debug("{0} has tried to login".format(identity ))
        return User.query.filter( (User.email == identity) | (User.username == identity) ).first()

    @classmethod
    def encrypt_password(cls, password_plainText):
        if password_plainText:
            generate_password_hash(password_plainText)
        return None

    def authenicate_password(self, password= '', with_password=True):

        """The check password Hash method accepts the Password Hash and the password
        and checks if its the correct password Hash for the current password if the hash matches
        then it returns true"""

        if with_password:
            check_password_hash(self.password, password)

        return True

    def get_password_reset_token(self, expires_in=600):

        token = jwt.encode({"user_id": self.id,
                             "role": self.role, "username": self.username, "exp": time() + expires_in},
                            current_app.config["SECRET_KEY"], algorithm="HS256").decode("UTF-8")
        print(token)
        return token

    @staticmethod
    def decode_password_reset_token(self, token):
        payload = jwt.decode( token, current_app.config["SECRET_KEY"], algorithms=["HS256"] )["reset_password"]
        return payload


    @classmethod
    def search(cls, query):
        """
        Search a resource by 1 or more fields.

        :param query: Search query
        :type query: str
        :return: SQLAlchemy filter
        """
        if not query:
            return ''

        search_query = '%{0}%'.format(query)
        search_chain = (User.email.ilike(search_query),
                        User.username.ilike(search_query))

        return or_(*search_chain)

    @classmethod
    def is_last_admin(cls, user, new_role, new_active):
        """
        Determine whether or not this user is the last admin account.

        :param user: User being tested
        :type user: User
        :param new_role: New role being set
        :type new_role: str
        :param new_active: New active status being set
        :type new_active: bool
        :return: bool
        """
        is_changing_roles = user.role == 'admin' and new_role != 'admin'
        is_changing_active = user.active is True and new_active is None

        if is_changing_roles or is_changing_active:
            admin_count = User.query.filter( User.role == 'admin' ).count()
            active_count = User.query.filter(User.is_active is True).count()

            if admin_count == 1 or active_count == 1:
                return True

        return False

    def update_activity_tracking(self, ip_address):
        """
        Update various fields on the user that's related to meta data on their
        account, such as the sign in count and ip address, etc..

        :param ip_address: IP address
        :type ip_address: str
        :return: SQLAlchemy commit results
        """
        self.sign_in_count += 1

        self.last_sign_in_on = self.current_sign_in_on
        self.last_sign_in_ip = self.current_sign_in_ip

        #self.current_sign_in_on = datetime.datetime.now(pytz.utc)
        self.current_sign_in_ip = ip_address

        return self.save()

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))


    @classmethod
    def initialize_password_reset(cls,identity=None):
        """

        :param identity:
        :return:
        """

        u = User.find_by_identity(identity)
        reset_token = u.get_password_reset_token()

        from app.lib.flask_mail import (
            send_password_reset_mail)
        send_password_reset_mail(u,reset_token)

        return u










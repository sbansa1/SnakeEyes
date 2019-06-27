from logging.handlers import SMTPHandler

import stripe
from flask import Flask, render_template, logging, app
from flask_admin.contrib.sqla import ModelView
from werkzeug.middleware.proxy_fix import ProxyFix

from app.blueprints import stripe_webhooks_com
from app.blueprints.admin import admin_blu
from app.blueprints.contact import contact
from app.blueprints.billings import billing
from app.blueprints.user import user
from app.blueprints.user.model import User
from app.blueprints.swagger import test
from app.config import Config
from app.blueprints.page import page
from app.extensions import db, db_migrate, login, debug_toolbar, crsf, mail,api


def create_app(settings_override=None, config_settings=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_settings)
    if settings_override:
        app.config.update(settings_override)

    stripe.api_key = app.config.get('STRIPE_SECRET_KEY')
    stripe.api_version = app.config.get('STRIPE_API_VERSION')

    app.logger.setLevel(app.config["LOG_LEVEL"])
    app.register_blueprint(page)
    app.register_blueprint(user)
    app.register_blueprint(contact)
    app.register_blueprint(admin_blu)
    app.register_blueprint(billing)
    app.register_blueprint(test)
    #app.register_blueprint(stripe_webhooks_com)
    middleware(app)
    errortemplates(app)
    extensions(app)


    return app


def extensions(app):

    db.init_app(app)
    debug_toolbar.init_app(app)
    db_migrate.init_app(app,db)
    login.init_app(app)
    crsf.init_app(app)
    mail.init_app(app)
    api.init_app(app)






def middleware(app):
    app.wsgi_app = ProxyFix(app.wsgi_app)

    return None


def errortemplates(app):


    def render_Status(status):

        error = getattr(status,'code',500)
        return render_template("error/{0}.html".format(error)), error

    for err in [400,500]:
        app.errorhandler(err)(render_Status)

    return None


def error_handler(app):


    mail_handler = SMTPHandler((app.config.get('MAIL_SERVER')),
                               (app.config.get('MAIL_PORT')),
                               app.config.get("MAIL_USERNAME"),
                               [app.config.get('MAIL_USERNAME')],
                               '[Exception handler] A 5XX was thrown',
                               (app.config.get('MAIL_USERNAME'),
                                (app.config.get('MAIL_PASSWORD'))),
                               secure=())

    mail_handler.setLevel(logging.ERROR)


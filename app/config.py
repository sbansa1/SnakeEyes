import os
from datetime import timedelta

from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__name__))

class Config(object):
    DEBUG = True
    SECRET_KEY = os.environ.get("secret_key") or "you will never guess"

    #DataBase Query String
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #ADMIN
    FLASK_ADMIN_SWATCH = os.environ.get("flask_admin_swatch") or "cerulean"
    DEBUG = True
    LOG_LEVEL = 'DEBUG'  # CRITICAL / ERROR / WARNING / INFO / DEBUG

    #SERVER_NAME = 'localhost:8000'
    #SECRET_KEY = 'insecurekeyfordev'
    # Flask-Mail.
    MAIL_DEFAULT_SENDER = 'saurabh.bnss0123@gmail.com'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'saurabh.bnss0123@gmail.com'
    MAIL_PASSWORD = 'Sterlite77&'

    #Celery
    CELERY_BROKER_URL = 'redis://:devpassword@redis:6379/0'
    CELERY_RESULT_BACKEND = 'redis://:devpassword@redis:6379/0'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_REDIS_MAX_CONNECTIONS = 5

    #Celery Cron Job Schedule
    CELERYBEAT_SCHEDULE = { 'mark-expire-credit-cards':{
        "tasks":'app.tasks.tasks.mark_old_credit_Cards',
        'schedule': crontab(hour=0,minute=0 )
    }

    }

    #ADMIN
    SEED_ADMIN_EMAIL = 'dev@local.host'
    SEED_ADMIN_PASSWORD = 'devpassword'
    REMEMBER_COOKIE_DURATION = timedelta( days=90 )


    #STRIPE

    STRIPE_PUBLIC_API_KEY="pk_test_NmXoaVZIiQL5a5jnW4hVTvtD00Ktw8hCdW"
    STRIPE_PRIVATE_KEY="sk_test_LcRleNnpNnePfdRaGXPW46FR003oBOrAca"

    STRIPE_API_VERSION = "2019-05-16"

    STRIPE_PLANS = {
        '0':{
            'id':'bronze',
            'name':'Bronze',
            'amount':200,
            'currency':'USD',
            'interval': "month",
            "interval_count":1,
            "livemode": False,
            "trial_period_days":14,
            "statement_descriptor":"BRONZE SNAKEYES PLAN",
            "metadata":{}
        },
        "1":{

            'id': 'gold',
            'name': 'GOLD',
            'amount': 500,
            'currency': 'USD',
            'interval': "month",
            "interval_count": 1,
            "livemode": False,
            "trial_period_days": 14,
            "statement_descriptor": "GOLD SNAKEYES PLAN",
            "metadata": {'recommended': True}




        },
        "2":{

            'id': 'platinum',
            'name': 'Platinum',
            'amount': 500,
            'currency': 'USD',
            'interval': "month",
            "interval_count": 1,
            "livemode": False,
            "trial_period_days": 14,
            "statement_descriptor": "Platinum SNAKEYES PLAN",
            "metadata": {}

        }
    }





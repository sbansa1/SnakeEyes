import datetime

from faker import Faker

from app.blueprints.user.model import User
from app.extensions import db
from app import create_app

import click
import random

app = create_app()
db.app = app

fake = Faker()



@click.command()
def users():
    random_Email = []
    data = []
    click.echo("Working....")

    #Generate a random User Name

    for i in range(0,99):
        random_Email.append(fake.email())
    random_Email.append(app.config['SEED_ADMIN_EMAIL'] )
    random_Email = list(set(random_Email))

    while True:
        if len(random_Email)==0:
            break

        fake_datetime = fake.date_time_between(
            start_date='-1y', end_date='now').strftime('%s')

        created_on = datetime.utcfromtimestamp(
            float(fake_datetime) ).strftime('%Y-%m-%dT%H:%M:%S Z')

        random_range = random.random()
        email  = random_Email.pop()

        if random_range >=0.05:
            role = "member"
        else:
            role = "admin"


        if random_range >= 0.5:
            random_num = str(int(round((random.random() * 1000))))
            username = fake.first_name() + random_num

        else:
            username = None



        params = {"create_on" : created_on,
                  'created_on': created_on,
                  'updated_on': created_on,
                  'role': role,
                  'email': email,
                  'username': username,
                  'password': User.encrypt_password( 'password' ),
                  'sign_in_count': random.random() * 100,
                  'current_sign_in_on': User.current_sign_in_on,
                  'current_sign_in_ip': fake.ipv4(),
                  'last_sign_in_on': User.current_sign_in_on,
                  'last_sign_in_ip': fake.ipv4()

                  }

        if email == app.config["ADMIN_EMAIL"]:
           password= User.encrypt_password(app.config["ADMIN_PASSWORD"])
           params["role"] = "admin"
           params["password"] = password

        data.append(params)

        return _bulk_insert(User,data,"user")



def _bulk_insert(model, data, label):
    with app.app_context():
        model.query.delete()
        db.session.commit()

        if db.engine.execute(model.__table__.insert(),data):
            _log_status(model.query.count(), label)
    return None

def _log_status(count, model_label):
    """
    Log the output of how many records were created.

       :param count: Amount created
       :type count: int
       :param model_label: Name of the model
       :type model_label: str
       :return: None
       """
    click.echo( 'Created {0} {1}'.format( count, model_label ) )
    return None










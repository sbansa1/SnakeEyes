from app import create_celery_app
from app.lib.flask_mailplus import send_templated_msg


celery = create_celery_app()

@celery.task()
def test_mail_func(email,message):

    ctx = {'email':email, 'message':message}

    send_templated_msg(subject='[Snake Eyes], contact',
                       sender = email,
                       recipients= "",
                       reply_to = email,
                       template = "contact/mail/index",ctx=ctx)
    return None
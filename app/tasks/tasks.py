from app.blueprints.billings.models.creditcard import CreditCard
from app.extensions import celery


@celery.task()
def mark_old_credit_Cards():
    """

    :return:
    """

    return CreditCard.mark_old_credit_cards()
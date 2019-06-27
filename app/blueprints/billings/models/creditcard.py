import datetime

from app.extensions import db
from app.lib.utility_datetime import time_delta
from app.lib.utility_sqlalchemy import ResourceMixin


class CreditCard(db.Model, ResourceMixin):
    """

    """
    IS_EXPIRING_THRESHOLD_MONTHS = 2


    __tablename__ = "credit_cards"

    id = db.Column(db.Integer, primary_key=True,index=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id",ondelete="CASCADE", onupdate="CASCADE"),
                        index=True, nullable=False)

    brand = db.Column(db.String(128))
    last4 = db.Column(db.Integer)
    expiry_date = db.Column(db.Date,index=True)
    is_expiring = db.Column(db.Boolean(),server_default='0',nullable=False)

    def __init__(self,**kwargs):
        #Call SQL-ALCHEMY Default's Constructor
        super(CreditCard,self).__init__(**kwargs)


    @classmethod
    def extract_credit_card_information(cls,customer):
        """

        Extract the credit card info from a payment customer object.

        :param customer: Payment customer
        :type customer: Payment customer
        :return: dict
        """

        card_info = customer.sources.data[0]
        exp_Date = datetime.date(card_info.exp_year,card_info.exp_month,1)

        card = {'brand': card_info.brand,
                "last4": card_info.last4,
                "exp_date":exp_Date,
                "is_expiring":CreditCard.is_expiring_soon(exp_Date=exp_Date)

        }

        return card

    @classmethod
    def is_expiring_soon(cls,exp_date=None, compare_date=None):


        """

        :param exp_date:
        :param compare_date:
        :return:
        """

        return exp_date<=time_delta(CreditCard.IS_EXPIRING_THRESHOLD_MONTHS,compare_date)

    @classmethod
    def mark_old_credit_cards(cls,compare_date=None):
        """

        :param compare_date:
        :return:
        """

        today_with_Delta = time_delta(CreditCard.IS_EXPIRING_THRESHOLD_MONTHS,compare_date)

        CreditCard.query.filter(CreditCard.expiry_date<=today_with_Delta).update({CreditCard.is_expiring:True})

        return db.session.commit()












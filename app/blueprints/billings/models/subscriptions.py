from datetime import datetime

import pytz

from app.blueprints.billings.gateway.stripecom import Subscription as PaymentSubscription, Plan as PaymentCard
from app.blueprints.billings.models.creditcard import CreditCard
from app.config import Config
from app.extensions import db
from app.lib.utility_sqlalchemy import ResourceMixin


class Subscription(db.Model,ResourceMixin):
    """
    A model Class for creating Subscription)
    """

    __tablename__="subscriptions"



    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id',ondelete='CASCADE',onupdate='CASCADE'),
                        index=True,nullable=False)
    plan = db.Column(db.String(128))
    coupon = db.Column(db.String(128))

    def __init__(self,**kwargs):
        super(Subscription,self).__init__(**kwargs)

    @classmethod
    def stripe_get_plan_by_id(cls,plan):

        for key,value in Config.STRIPE_PLANS.items():
            if value.get('id')==plan:
                return Config.STRIPE_PLANS[key]




    def create(self, user=None, name=None, plan=None, coupon=None, token=None):
        """

        :param user: User Id
        :param name: Name of the plan
        :param plan: The available plan itself
        :param coupon: Coupon is Optional
        :param token: Stripe token.
        :return: It will return a Stripe instance.
        """

        if token is None:
            return False

        if coupon:
            self.coupon = coupon.Upper()


        customer = PaymentSubscription.create(token=token,
                                       email=user.email,
                                       plan=plan,
                                       coupon=self.coupon)


        #Update the user details
        user.payment_id = customer.id
        user.name = name

        #Set the subscription details
        self.user_id=user.id
        self.plan = plan

        #Redeem Coupon
        if coupon:
            coupon = Coupon.query.filter(Coupon.code==self.coupon).first()
            coupon.redeem()

        credit_card = CreditCard(user_id=user.id,**CreditCard.extract_credit_card_information(customer))

        #Add the user who is buying the subscription
        db.session.add(user)
        #Add the credit card
        db.session.add(credit_card)
        #Add the subscription
        db.session.add(self)

        db.session.commit()

        return True


    def update(self,user=None,coupon=None,plan=None):
        """

        :param user:
        :param coupon:
        :param plan:
        :return:
        """

        PaymentSubscription.update(user.payment_id,coupon,plan)
        user.subscription.plan = plan

        if coupon:
            user.subscription.coupon = coupon
            coupon = Coupon.query.filter(Coupon.code==coupon).first()

            if coupon:
                coupon.redeem()

        db.session.add(user.subscription)
        db.session.commit()

        return True

    def cancel(self,user=None,discard_credit_card=True):
        """

        :param user:
        :param discard_credit_card:
        :return:
        """

        PaymentSubscription.cancel(user.payment_id)
        user.payment_id = None
        user.cancelled_subscription_on = datetime.datetime.now(pytz.utc)

        db.session.add(user)
        db.session.delete(user.subscription)

        if discard_credit_card:
            db.session.delete(user.creditcard)

        db.session.commit()

        return True


    def update_payment_method(self,user=None,creditcard=None,name=None,token=None):

        if token is None:
            return False

        customer = PaymentCard.update(user.payment_id,token)
        user.name = name

        new_card = CreditCard.extract_credit_card_information(customer)
        creditcard.brand = new_card.get('brand')
        creditcard.last4 = new_card.get('last4')
        creditcard.expiry_date = new_card.get("expiry_date")
        creditcard.is_expiring = new_card.get("is_expiring")

        db.session.add(user)
        db.session.add(creditcard)

        db.session.commit()

        return True


    @classmethod
    def get_new_plan(cls,keys):

        for key in keys:
            split_key = key.split('sumbit_')
            if isinstance(split_key,list) and len(split_key)==2:
                if PaymentCard.stripe_get_plan_by_id(split_key[1]):
                    return split_key[1]


        return None












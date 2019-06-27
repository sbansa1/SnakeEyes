from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField
from wtforms.validators import DataRequired, Length, Optional


class CreditCardForm(FlaskForm):
    stripe_key = HiddenField('stripe_publishable_key',[DataRequired(),Length(1,128)])
    plan = HiddenField('Plan',[DataRequired(),Length(1,128)])
    coupon_code = StringField("Coupon Code", [Optional(), Length(1,128)])
    name = StringField("Name on Card", [DataRequired(), Length(1,128)])



class UpdateSubscriptionForm(FlaskForm):
    coupon_code = StringField("Do You have An Active Coupon?", [Optional(), Length(1,254)])


class CancelSubscription(FlaskForm):
    """

    """
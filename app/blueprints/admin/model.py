from sqlalchemy import func

from app.blueprints.billings.models.subscriptions import Subscription
from app.blueprints.user.model import User, db


class DashBoard(object):
    @classmethod
    def _group_count_method(cls,model,field):

        """
        Group results for a specific model and field.
        :param model: Name of the model
        :type model: SQLAlchemy model
        :param field: Name of the field to group on
        :type field: SQLAlchemy field
        :return: dict
         """

        count = func.count(field)
        query = db.session.query(count,field).group_by(field).all()

        results = {

            "Query": query,
            "Count": model.query.count()

        }

        return results


    @classmethod
    def group_count_method(cls):

        return DashBoard._group_count_method(User,User.role)

    @classmethod
    def group_and_count_subscription(cls):
        return DashBoard._group_count_method(Subscription,Subscription.plan)


    @classmethod
    def group_and_count_coupons(cls):
        """
        Obtain coupoun stats across all the subscribers

        :return: tupule
        """
        not_null = db.session.query(Subscription).filter(Subscription.coupon.isnot(None)).count()
        total = db.session.query(func.count(Subscription.id)).scalar() #counts all the rows in the subscription model

        if total==0:
            percent =0
        else:
            percent = (round(not_null/float(total)) * 100,1)


        return not_null,total,percent





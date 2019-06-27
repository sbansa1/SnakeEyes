import stripe


class Plan(object):

    @classmethod
    def retrive(cls,plan):
        """
        Retrieve an existing plan.

        API Documentation:
        https://stripe.com/docs/api#retrieve_plan

        :param plan: Plan identifier
        :type plan: str
        :return: Stripe plan
        """

        try:
          return stripe.Plan.retrieve(plan)
        except stripe.error.StripeError as e:
            print(e)

    @classmethod
    def delete(cls,plan):

        """
        Delete an existing plan.

        API Documentation:
        https://stripe.com/docs/api#delete_plan

        :param plan: Plan identifier
        :type plan: str
        :return: Stripe plan object
        """

        try:
            plan = stripe.Plan.retrieve(plan)
            return plan.delete()
        except stripe.error.StripeError as e:
            print(e)



    @classmethod
    def list(cls):

        try:
            return stripe.Plan.all()
        except stripe.error.StripeError as e:
            print(e)



    @classmethod
    def create(cls,id=None, name=None, amount=None, currency=None,
               interval=None, interval_count=None, trial_period_days=None,
               metadata=None, statement_descriptor=None):

        """
              Create a new plan.

              API Documentation:
                https://stripe.com/docs/api#create_plan

              :param id: Plan identifier
              :type id: str
              :param name: Plan name
              :type name: str
              :param amount: Amount in cents to charge or 0 for a free plan
              :type amount: int
              :param currency: 3 digit currency abbreviation
              :type currency: str
              :param interval: Billing frequency
              :type interval: str
              :param interval_count: Number of intervals between each bill
              :type interval_count: int
              :param trial_period_days: Number of days to run a free trial
              :type trial_period_days: int
              :param metadata: Additional data to save with the plan
              :type metadata: dct
              :param statement_descriptor: Arbitrary string to appear on CC statement
              :type statement_descriptor: str
              :return: Stripe plan
              """
        try:
            return stripe.Plan.create(id=id,
            name=name,amount=amount,currency=currency,
            interval=interval,interval_count=interval_count,trial_period_days=trial_period_days,
            metadata=metadata,statement_descriptor=statement_descriptor)
        except stripe.error.StripeError as e:
            print(e)


    @classmethod
    def update(cls,id = None, name = None, metadata = None,statement_descriptor = None):

        """
        Update an existing plan.

        API Documentation:
          https://stripe.com/docs/api#update_plan

        :param id: Plan identifier
        :type id: str
        :param name: Plan name
        :type name: str
        :param metadata: Additional data to save with the plan
        :type metadata: dct
        :param statement_descriptor: Arbitrary string to appear on CC statement
        :type statement_descriptor: str
        :return: Stripe plan
        """
        try:
         plan = stripe.Plan.retrieve(id)
         plan.name = name
         plan.metadata = metadata
         plan.statement_descriptor = statement_descriptor

         return stripe.Plan.save(plan)

        except stripe.error.StripeError as e:
            print(e)



class Subscription(object):
    @classmethod
    def create(cls,token=None, email=None, coupon=None, plan=None):
        """
        Create a new subscription.

        API Documentation:
          https://stripe.com/docs/api#create_subscription

        :param token: Token returned by JavaScript
        :type token: str
        :param email: E-mail address of the customer
        :type email: str
        :param coupon: Coupon code
        :type coupon: str
        :param plan: Plan identifier
        :type plan: str
        :return: Stripe customer
        """
        param = {"token":token,
                 "email":email,
                 "plan":plan}

        if coupon:
            param['coupon'] = coupon

        return stripe.Customer.create(**param)



    @classmethod
    def update(cls,customer_id=None,coupon=None,plan=None):
        """

        :param customer:
        :param coupon:
        :param plan:
        :return:
        """

        customer = stripe.Customer.retrieve(customer_id)
        subscription_id = customer.subscriptions.data[0].id
        subscription = customer.subscriptions.retrieve(subscription_id)
        subscription.plan = plan


        if coupon:
            subscription.coupon = coupon

        return subscription.save()


    @classmethod
    def cancel(cls,customer_id=None):
        """

        :param customer_id:
        :return:
        """
        customer = stripe.Customer.retrieve(customer_id)
        subscription_id = customer.subscriptions.data[0].id
        subscription_cancel = customer.subscriptions.retrieve(subscription_id).delete()

        return subscription_cancel




class Card(object):

    @classmethod
    def update(cls,customer_id, stripe_token=None):

        """

        :param customer_id:
        :param stripe_token:
        :return:
        """

        customer = stripe.Customer.retrieve(customer_id)
        customer.source = stripe_token

        return customer.save()

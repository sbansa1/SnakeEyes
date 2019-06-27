from flask import flash, url_for, request, current_app, render_template, app
from flask_login import current_user
from flask_login import login_required
from werkzeug.utils import redirect

from app.blueprints.billings import billing
from app.blueprints.billings.forms import CreditCardForm, UpdateSubscriptionForm, CancelSubscription
from app.blueprints.billings.models.creditcard import CreditCard
from app.blueprints.billings.models.subscriptions import Subscription


@billing.route("/create", methods=['GET','POST'])
@login_required
def create():
    if current_user.subscription:
        flash("The user is already subscribed")
        return redirect(url_for("user.settings"))

    plan = request.args.get("plan")
    subscription_plan = Subscription.stripe_get_plan_by_id(plan)


    if subscription_plan is None and request.method == 'GET':
        flash("No such plan")
        return redirect(url_for("billing.pricing"))

    stripe_key =  current_app.config.get('STRIPE_PUBLIC_API_KEY')
    form = CreditCardForm(stripe_key=stripe_key, plan=plan)

    if form.validate_on_submit():
        subscription = Subscription()
        created=subscription.create(user=current_user,
                            name= request.form.get('name'),
                            plan=request.form.get('plan'),
                            coupon=request.form.get("coupon_code"),
                            token=request.form.get("stripe_token"))
        if created:
            flash("Awesome Thanks for subscribing", 'Thanks')
        else:
            flash("you must have a javascript enabled", 'Error')


        return redirect(url_for("user.settings"))

    return render_template("billing/payment_method.html",form=form,plan=subscription_plan)



@billing.route("/updatecard",methods=['GET','POST'])
@login_required
def update_credit_card():

    if not current_user.creditcard:
        flash("Please make sure you have the card added before")
        return redirect(url_for("user.settings"))

    active_plan = Subscription.stripe_get_plan_by_id(current_user.subscription.plan)

    card = current_user.creditcard
    stripe_key = current_app.config.get('STRIPE_PUBLIC_API_KEY')

    form = CreditCardForm(stripe_key=stripe_key,plan=active_plan,name=current_user.name)

    if form.validate_on_submit():
        subscription = Subscription()
        updated = subscription.update_payment_method(user=current_user,
                                           credit_card = card,
                                           name = request.form.get("name"),
                                           token = request.form.get("token"))

        if updated:
            flash("The details have been updated", "success")

        else:
            flash("your javascript is disabled", "failure")
        return redirect(url_for('user.settings'))

    render_template("billing/payment_method.html",form=form, plan=active_plan, card_last4=str(CreditCard.last4))


@billing.route("/update",methods=['GET','POST'])
@login_required
def update():

    current_plan = current_user.subscription.plan
    active_plan = Subscription.stripe_get_plan_by_id(current_plan)
    new_plan = Subscription.get_new_plan(request.form.keys())


    plan = Subscription.stripe_get_plan_by_id(new_plan)

    is_same_plan = new_plan == active_plan['id']

    if((new_plan is not None and plan is None) or is_same_plan) and request.method == 'POST':
        return(url_for("billing.update"))

    form = UpdateSubscriptionForm(coupon_code=current_user.subscription.coupon)

    if form.validate_on_submit():
        subscription = Subscription()
        updated = subscription.update(user=current_user,coupon= request.form.get("coupon_code"),plan=plan.get("id"))

        if updated:
            flash("The details have been updated", "success")

        else:
            flash("your javascript is disabled", "failure")
        return redirect(url_for('user.settings'))

    render_template("billing/pricing.html",form=form,plan=app.config.STRIPE_PLANS,active_plan=active_plan)



@billing.route('/cancel',methods=['GET','POST'])
@login_required
def cancel():

    if not current_user.subscription:
        flash('You do not have an active subscription','error')
        return redirect(url_for('user.settings'))

    form = CancelSubscription()

    if form.validate_on_submit():
        subscription = Subscription()
        cancelled = subscription.cancel(user=current_user)

        if cancelled:
            flash("Sorry to have see you go", "Cancelled")
            return redirect(url_for('user.settings'))

    return render_template('billing/cancel.html',form=form)




@billing.route('/pricing')
def pricing():
    if current_user.is_authenticated and current_user.subscription:
        return redirect(url_for('billing.update'))

    form = UpdateSubscriptionForm()

    return render_template('billing/pricing.html', form=form,
                           plans=current_app.config.get('STRIPE_PLANS'))








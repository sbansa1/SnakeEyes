from flask import flash, url_for, render_template, request
from werkzeug.utils import redirect
from app.blueprints.contact import contact
from app.blueprints.contact.forms import ContactForm


@contact.route("/contact", methods=['GET','POST'])
def index():
    form = ContactForm()
    if form.validate_on_submit():
        from app.blueprints.contact.tasks import test_mail_func
        test_mail_func.delay(request.form.get('email'), request.form.get('message'))
        flash("Success! Form has been successfully submitted")
        return redirect(url_for('contact.index'))
    return render_template("contact/index.html", form=form)
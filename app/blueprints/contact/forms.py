from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length


class ContactForm(FlaskForm):

    email = EmailField("Please enter your email",[DataRequired(),Length(3,100)])
    message = TextAreaField("Please enter a Message ?",[DataRequired(),Length(1,1085)])
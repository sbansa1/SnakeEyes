from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp, Optional, Email
from wtforms_alchemy import Unique, ModelForm
from wtforms_components import EmailField

from app.blueprints.user.model import User
from app.blueprints.user.validators import ensure_existing_password_matches, ensure_identity_exists
from app.extensions import db


class LoginForm(FlaskForm):
    next = HiddenField()
    identity = StringField("Username or email", [DataRequired(), Length(1,256)])
    password = PasswordField("Password", validators=[DataRequired(), Length(8,128)])


class BeginPasswordResetForm(FlaskForm):
    identity = StringField('Username or Email', validators=[DataRequired(), Length(1,128), ensure_identity_exists])


class PasswordRestForm(FlaskForm):
    reset_token = HiddenField()
    password = PasswordField('Password',validators=[DataRequired(), Length(8,128)])


class SignupForm(ModelForm,FlaskForm):
    email = EmailField(validators=[DataRequired(), Email(), Unique(User.email, get_session=lambda : db.session)])
    password = PasswordField("Password", validators=[DataRequired(), Length(8,128)])

class WelcomeForm(ModelForm,FlaskForm):
    username_message = 'Letters, numbers and underscores only please'

    username = StringField(validators=[Unique(User.username, get_session = lambda : db.session),DataRequired(),
                                              Length(1,16), Regexp('^\w+$', message=username_message)])


class UpdateCredentials(ModelForm,FlaskForm):

    current_password = PasswordField( 'Current password',
                                      [DataRequired(),
                                       Length( 8, 128 ), ensure_existing_password_matches] )

    email = EmailField(validators=[
        Email(),
        Unique(
            User.email,
            get_session=lambda: db.session
        )
    ] )
    password = PasswordField( 'Password', [Optional(), Length( 8, 128 )] )


class PasswordResetForm(FlaskForm):
    reset_token = HiddenField()
    password = PasswordField('Password', [DataRequired(), Length(8, 128)])


from collections import OrderedDict

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField
from wtforms.validators import Optional, Length, Regexp, DataRequired
from wtforms_alchemy import Unique, ModelForm

from app.blueprints.user.model import User
from app.extensions import db
from app.lib.util_wtfForms import choices_from_dict


class SearchForm(FlaskForm, ModelForm):
    q = StringField('search terms', validators=[Optional(), Length(1,128)])



class UserForm(FlaskForm,ModelForm):
    username_message = "Only Letters,  Numbers and Special Characters are Considered "
    username = StringField(validators=[(Unique(User.username,
                                               get_session=lambda : db.session)),
                                       Optional(),Length(1,20), Regexp('^/w+$',message=username_message)])
    role = SelectField("Privledges", validators=[DataRequired()],choices=choices_from_dict(User.ROLE,
                                                                                           prepend_blank=False))
    active = BooleanField('Yes, allow this user to sign in')


class BulkDeleteAll(FlaskForm,ModelForm):

    SCOPE = OrderedDict()
    SCOPE['all_selected_items'] = 'All selected items'
    SCOPE['all_search_results'] = 'All search results'

    scope = SelectField("Privledges",validators=[DataRequired()],choices=choices_from_dict(SCOPE,prepend_blank=False))




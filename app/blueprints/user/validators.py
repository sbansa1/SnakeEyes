from wtforms.validators import  ValidationError

from app.blueprints.user.model import User

def ensure_identity_exists(form,field):
    """Ensure an identity exists.
    :param form: wtforms Instance
    :param field: Field being passed in
    :return: None
    """

    user = User.find_by_identity(field.data)

    if not user:
        raise ValidationError('Unable to Locate account')

def ensure_existing_password_matches(form,field):
    """
    Ensure that the Current password matches their existing account.
    :param form: wtforms Instance
    :param field: Field being passed in
    :return: None
    """

    user = User.query.get(form._obj.id)

    if not user.authenicate_password(password=field.data):
        raise ValidationError("Password does not Match")

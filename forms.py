from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email

from models import  User


class RegistrationForm(FlaskForm):
    email = StringField(render_kw={"placeholder": "Email"}, validators=[DataRequired(), Email()])
    submit = SubmitField()

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('You are already registered.')


from flask_wtf import FlaskForm

from wtforms import validators
from wtforms import StringField
from wtforms import PasswordField
from wtforms import ValidationError
from wtforms.fields import EmailField

from author.models import Author


class RegisterForm(FlaskForm):
    full_name = StringField("Full Name", [validators.InputRequired()])
    email = EmailField("Email address", [
                       validators.InputRequired(), validators.Email()])
    password = PasswordField(
        "New Password", [validators.InputRequired(), validators.Length(min=4, max=80)])
    confirm = PasswordField("Repeat Password", [validators.EqualTo(
        fieldname='password', message="Passwords must match")])

    def validate_email(self, email):
        author = Author.query.filter_by(email=email.data).first()
        if author is not None:
            raise ValidationError(
                message="Email already in use, please use a different one.")

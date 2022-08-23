from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed

from wtforms import StringField
from wtforms import TextAreaField
from wtforms import FileField
from wtforms import validators

from wtforms_alchemy import QuerySelectField

from blog.models import Category


def categories():
    return Category.query


class PostForm(FlaskForm):
    image = FileField("Image", validators=[FileAllowed(
        ['jpg', 'png'], "We only accept JPG or PNG images")])
    title = StringField("Title", validators=[
                        validators.InputRequired(), validators.Length(max=80)])
    body = TextAreaField("Content", validators=[validators.InputRequired()])
    category = QuerySelectField(
        "Category", query_factory=categories, get_label="name", allow_blank=True)
    new_category = StringField("New Category")

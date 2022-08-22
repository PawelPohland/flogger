from flask import Blueprint
from flask import session
from flask import render_template


blog_app = Blueprint('blog_app', __name__)


@blog_app.route('/')
def index():
    return render_template("blog/index.html")

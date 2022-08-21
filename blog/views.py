from flask import Blueprint
from flask import session


blog_app = Blueprint('blog_app', __name__)


@blog_app.route('/')
def index():
    if session.get("full_name"):
        return f"Hi, {session['full_name']}"
    return 'Blog Homepage'

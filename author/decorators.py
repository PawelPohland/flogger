from functools import wraps

from flask import session
from flask import request
from flask import redirect
from flask import url_for
from flask import flash


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            flash("Please login to continue")
            return redirect(url_for("author_app.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

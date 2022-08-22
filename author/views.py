from urllib import request
from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask import session
from flask import flash

from werkzeug.security import generate_password_hash

from author.models import Author
from author.forms import RegisterForm
from author.forms import LoginForm

from application import db


author_app = Blueprint('author_app', __name__)


@author_app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        author = Author(full_name=form.full_name.data,
                        email=form.email.data, password=hashed_password)
        db.session.add(author)
        db.session.commit()

        flash("You are now registered, please login")
        return redirect(url_for("author_app.login"))
    return render_template('author/register.html', form=form)


@author_app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = None

    if request.method == "GET" and request.args.get("next"):
        session["next"] = request.args.get("next", None)

    if form.validate_on_submit():
        author = Author.query.filter_by(email=form.email.data).first()
        session["id"] = author.id
        session["full_name"] = author.full_name

        if "next" in session:
            redirect_to = session.get("next")
            session.pop("next")
            return redirect(redirect_to)
        else:
            return redirect(url_for("blog_app.index"))

    return render_template("author/login.html", form=form, error=error)


@author_app.route("/logout")
def logout():
    session.pop("id")
    session.pop("full_name")
    flash("User logged out")
    return redirect(url_for("author_app.login"))

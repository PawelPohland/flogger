from flask import Blueprint

from author.models import Author


author_app = Blueprint('author_app', __name__)


@author_app.route('/register', methods=['GET', 'POST'])
def register():
    return 'Author registration'

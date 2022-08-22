from application import db
from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    slug = db.Column(db.String(255), unique=True)
    publish_date = db.Column(db.DateTime)
    live = db.Column(db.Boolean)

    author = db.relationship(
        "Author", backref=db.backref("posts", lazy="dynamic"))

    category = db.relationship(
        "Category", backref=db.backref("posts", lazy="dynamic"))

    def __init__(self, author, title, body, category=None, slug=None, publish_date=None, live=True):
        self.author_id = author.id
        self.title = title
        self.body = body

        if category:
            self.category_id = category.id

        self.slug = slug

        if publish_date is None:
            self.publish_date = datetime.utcnow()

        self.live = live

    def __repr__(self):
        return f"<Post {self.title}>"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Category {self.name}>"

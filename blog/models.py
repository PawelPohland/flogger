from application import db
from datetime import datetime


# association table
tag_x_post = db.Table('tag_x_post',
                      db.Column('tag_id', db.Integer, db.ForeignKey(
                          'tag.id'), primary_key=True),
                      db.Column('post_id', db.Integer, db.ForeignKey(
                          'post.id'), primary_key=True))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    # store only file name, 36 characters for UUID
    image = db.Column(db.String(36))
    slug = db.Column(db.String(255), unique=True)
    publish_date = db.Column(db.DateTime)
    live = db.Column(db.Boolean)

    author = db.relationship(
        "Author", backref=db.backref("posts", lazy="dynamic"))

    category = db.relationship(
        "Category", backref=db.backref("posts", lazy="dynamic"))

    tags = db.relationship("Tag", secondary=tag_x_post, lazy="subquery", order_by="asc(Tag.id)",
                           backref=db.backref("posts", lazy="dynamic"))

    def __init__(self, author, title, body, image=None, category=None, slug=None, publish_date=None, live=True):
        self.author_id = author.id
        self.title = title
        self.body = body
        self.image = image

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


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Tag {self.name}>"

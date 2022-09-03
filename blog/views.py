from flask import Blueprint
from flask import session
from flask import render_template
from flask import redirect
from flask import request
from flask import flash
from flask import url_for

from slugify import slugify

from application import db

from blog.models import Post
from blog.models import Category
from blog.models import Tag
from blog.forms import PostForm

from author.models import Author
from author.decorators import login_required

from settings import BLOG_POST_IMAGES_PATH

from uuid import uuid4
import os

from PIL import Image


blog_app = Blueprint('blog_app', __name__)


POSTS_PER_PAGE = 2


@blog_app.route('/')
def index():
    page = int(request.values.get("page", 1))
    posts = Post.query.filter_by(live=True).order_by(
        Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template("blog/index.html", posts=posts, title="Latest Posts")


@blog_app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    tags_field = request.values.get("tags_field", "")

    if form.validate_on_submit():
        image_id = None

        if form.image.data:
            f = form.image.data
            image_id = str(uuid4())
            file_name = image_id + ".png"
            file_path = os.path.join(BLOG_POST_IMAGES_PATH, file_name)
            Image.open(f).save(file_path)

            image_resize(BLOG_POST_IMAGES_PATH, image_id, 600, "lg")
            image_resize(BLOG_POST_IMAGES_PATH, image_id, 300, "sm")

        if form.new_category.data:
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            category = new_category
        else:
            category = form.category.data

        author = Author.query.get(session["id"])
        title = form.title.data.strip()
        body = form.body.data.strip()

        post = Post(author=author, title=title, body=body,
                    image=image_id, category=category)

        save_tags(post, tags_field)

        db.session.add(post)
        db.session.commit()

        slug = slugify(str(post.id) + "-" + post.title)
        post.slug = slug
        db.session.commit()

        flash("Article posted")
        return redirect(url_for("blog_app.article", slug=slug))

    return render_template("blog/post.html", form=form, action="new", tags_field=tags_field)


@blog_app.route('/posts/<slug>')
def article(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template("blog/article.html", post=post)


@blog_app.route("/edit/<slug>", methods=["GET", "POST"])
@login_required
def edit(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    tags_field = request.values.get("tags_field", load_tags(post))

    form = PostForm(obj=post)

    if form.validate_on_submit():
        original_image = post.image
        original_title = post.title
        form.populate_obj(post)

        if form.image.data:
            f = form.image.data
            image_id = str(uuid4())
            file_name = image_id + ".png"
            file_path = os.path.join(BLOG_POST_IMAGES_PATH, file_name)
            Image.open(f).save(file_path)

            image_resize(BLOG_POST_IMAGES_PATH, image_id, 600, "lg")
            image_resize(BLOG_POST_IMAGES_PATH, image_id, 300, "sm")

            post.image = image_id
        else:
            post.image = original_image

        if form.new_category.data:
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            post.category = new_category

        if form.title.data != original_title:
            post.slug = slugify(str(post.id) + "-" + form.title.data)

        save_tags(post, tags_field)

        db.session.commit()
        flash("Article edited")

        return redirect(url_for("blog_app.article", slug=post.slug))

    return render_template("blog/post.html", form=form, post=post, tags_field=tags_field, action="edit")


@blog_app.route("/delete/<slug>")
@login_required
def delete(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    post.live = False
    db.session.commit()

    flash("Article deleted")
    return redirect(url_for("blog_app.index"))


@blog_app.route("/categories/<category_id>")
def categories(category_id):
    category = Category.query.filter_by(id=category_id).first_or_404()
    page = int(request.values.get("page", 1))

    #posts = category.posts.filter_by(live=True).order_by(Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)

    posts = Post.query.filter_by(category=category, live=True)\
        .order_by(Post.publish_date.desc())\
        .paginate(page, POSTS_PER_PAGE, False)

    return render_template("blog/category_posts.html", posts=posts, title=category.name, category_id=category_id)


@blog_app.route("/tags/<tag>")
def tags(tag):
    tag = Tag.query.filter_by(name=tag).first_or_404()
    page = int(request.values.get("page", 1))

    posts = tag.posts.filter_by(live=True)\
        .order_by(Post.publish_date.desc())\
        .paginate(page, POSTS_PER_PAGE, False)

    return render_template("blog/tag_posts.html", posts=posts, title=f"Tag: {tag.name}", tag=tag.name)


def image_resize(original_file_path, image_id, image_base, extension):
    file_path = os.path.join(original_file_path, image_id + ".png")
    image = Image.open(file_path)

    wpercent = (image_base / float(image.size[0]))
    hsize = int(float(image.size[1]) * float(wpercent))

    image = image.resize((image_base, hsize), Image.ANTIALIAS)
    modified_file_path = os.path.join(
        original_file_path, image_id + "." + extension + ".png")

    image.save(modified_file_path)


def save_tags(post, tags_field):
    post.tags.clear()

    for tag_item in tags_field.split(","):
        tag = Tag.query.filter_by(name=slugify(tag_item)).first()
        if not tag:
            tag = Tag(name=slugify(tag_item))
            db.session.add(tag)
        post.tags.append(tag)

    return post


def load_tags(post):
    tags_field = ""

    for tag in post.tags:
        tags_field += tag.name + ", "

    return tags_field[:-2]

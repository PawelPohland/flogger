from application import create_app as create_app_base
from application import db

from utils.test_db import TestDB

from slugify import slugify

import os
import unittest
import pathlib

from dotenv import load_dotenv
env_dir = pathlib.Path(__file__).parents[1]
load_dotenv(os.path.join(env_dir, '.flaskenv'))


class PostTest(unittest.TestCase):
    def create_app(self):
        return create_app_base(SQLALCHEMY_DATABASE_URI=self.db_uri, TESTING=True, WTF_CSRF_ENABLED=False, SECRET_KEY="mySecret!")

    def setUp(self):
        self.test_db = TestDB()
        self.db_uri = self.test_db.create_db()
        self.app_factory = self.create_app()
        self.app = self.app_factory.test_client()

        with self.app_factory.app_context():
            db.create_all()

    def tearDown(self):
        with self.app_factory.app_context():
            db.drop_all()

        self.test_db.drop_db()

    def user_dict(self):
        return {
            "full_name": "John Smith",
            "email": "john.smith@test.com",
            "password": "test123",
            "confirm": "test123"
        }

    def post_dict(self):
        return {
            "title": "My Awesome Post",
            "body": "This is my awesome post content!",
            "new_category": "Tech",
            "tags_field": "flask, python"
        }

    def test_blog_post_create(self):
        # try to post without logging in
        rv = self.app.get("/post", follow_redirects=True)
        assert "Please login to continue" in str(rv.data)

        # register and login
        self.app.post("/register", data=self.user_dict())
        self.app.post("/login", data=self.user_dict())

        # post first post
        rv = self.app.post("/post", data=self.post_dict(),
                           follow_redirects=True)
        assert "Article posted" in str(rv.data)
        assert "Tech" in str(rv.data)  # category

    def test_blog_post_update_delete(self):
        # register user and post
        self.app.post("/register", data=self.user_dict())
        self.app.post("/login", data=self.user_dict())
        self.app.post("/post", data=self.post_dict())

        # edit article
        post2 = self.post_dict()
        post2["title"] = "My New Awesome Post"
        post2["tags_field"] = "django"
        endpoint = f"/edit/1-{slugify(self.post_dict()['title'])}"

        rv = self.app.post(endpoint, data=post2, follow_redirects=True)

        assert "Article edited" in str(rv.data)
        assert "My New Awesome Post" in str(rv.data)
        assert "flask" not in str(rv.data)

        # delete the article
        endpoint = f"/delete/1-{slugify(post2['title'])}"
        rv = self.app.get(endpoint, follow_redirects=True)
        assert "Article deleted" in str(rv.data)

from application import create_app as create_app_base
from application import db
from author.models import Author
from utils.test_db import TestDB

from flask import session

import os
import unittest
import pathlib

from dotenv import load_dotenv
env_dir = pathlib.Path(__file__).parents[1]
load_dotenv(os.path.join(env_dir, '.flaskenv'))


class AuthorTest(unittest.TestCase):
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

    def test_user_registration(self):
        # try to register new user
        rv = self.app.post("/register", data=self.user_dict(),
                           follow_redirects=True)
        assert "You are now registered" in str(rv.data)

        # if registration worked, than visit homepage
        # and check if that user exists in database
        with self.app as c:
            c.get("/")
            assert Author.query.filter_by(
                email=self.user_dict()["email"]).count() == 1

        # try to register the same user (non unique email) again
        rv = self.app.post("/register", data=self.user_dict(),
                           follow_redirects=True)
        assert "Email already in use" in str(rv.data)

        # try to register different user but this time
        # password and confirmation mismatch
        user2 = self.user_dict()
        user2["email"] = "smith.john@test.com"
        user2["confirm"] = "123test"

        rv = self.app.post("/register", data=user2, follow_redirects=True)
        assert "Passwords must match" in str(rv.data)

    def test_user_login(self):
        # register new user
        self.app.post("/register", data=self.user_dict())

        # login that new user
        with self.app as c:
            c.post("/login", data=self.user_dict(), follow_redirects=True)
            assert session["id"] == 1

        # test if logout works
        with self.app as c:
            c.get("/logout", follow_redirects=True)
            assert session.get("id") is None

        user2 = self.user_dict()
        user2["password"] = "wrong_password"

        # trying to login with wrong password
        rv = self.app.post("/login", data=user2, follow_redirects=True)
        assert "Incorect email or password" in str(rv.data)

        user3 = self.user_dict()
        user3["email"] = "noone@test.com"

        # trying to login with nonexisting email
        rv = self.app.post("/login", data=user3, follow_redirects=True)
        assert "Incorect email or password" in str(rv.data)

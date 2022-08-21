import os
from flask_sqlalchemy import SQLAlchemy


class TestDB:
    def __init__(self):
        self.db_name = os.environ['DATABASE_NAME'] + '_test'
        self.db_host = os.environ['DB_HOST']
        self.db_root_password = os.environ['MYSQL_ROOT_PASSWORD']

        if self.db_root_password:
            self.db_username = 'root'
            self.db_password = self.db_root_password
        else:
            self.db_username = os.environ['DB_USERNAME']
            self.db_password = os.environ['DB_PASSWORD']

        self.db_uri = f"mysql+pymysql://{self.db_username}:{self.db_password}@{self.db_host}"

    def get_connection(self):
        engine = SQLAlchemy.create_engine(
            SQLAlchemy, sa_url=self.db_uri, engine_opts={})
        conn = engine.connect()
        conn.execute("COMMIT")

        return conn

    def create_db(self):
        if self.db_username == 'root':
            conn = self.get_connection()
            conn.execute(f"CREATE DATABASE {self.db_name}")
            conn.close()

        return f"{self.db_uri}/{self.db_name}"

    def drop_db(self):
        if self.db_username == 'root':
            conn = self.get_connection()
            conn.execute(f"DROP DATABASE {self.db_name}")
            conn.close()

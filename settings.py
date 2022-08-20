import os


SECRET_KEY = os.getenv('SECRET_KEY')

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DATABASE_NAME = os.getenv('DATABASE_NAME')

MYSQL_ROOT_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD')

DB_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:3306/{DATABASE_NAME}"

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True

BLOG_NAME = os.getenv('BLOG_NAME')
BLOG_POST_IMAGES_PATH = os.path.join(
    os.getcwd(), *os.getenv('BLOG_POST_IMAGES_PATH').split('/'))
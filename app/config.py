# coding=utf-8
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI') or 'mysql+pymysql://root:root@127.0.0.1:3306/smile_team?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    SECRET_KEY = "\x1b\xcbC?B\x84e\xb6rX?\xae4\xe0\x9f\xf0+\x87\xfe}k\xcf\x91\xb3"
"""项目配置"""

import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # SECRET_KEY: 优先从环境变量读取，否则自动生成随机密钥（仅用于开发）
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

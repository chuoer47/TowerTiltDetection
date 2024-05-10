"""
该类为数据库模型
"""

from appdir import db


class User(db.Model):
    """用户"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Question(db.Model):
    """论坛问题"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True)
    question = db.Column(db.String(300), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    datetime = db.Column(db.DateTime)

    def __repr__(self):
        return '<Question {}>'.format(self.title)


class Answer(db.Model):
    """论坛回答"""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))


class DailyData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    blood_glucose = db.Column(db.String(100), index=True)
    amount_of_exercise = db.Column(db.String(100), index=True)
    composition_of_Diet = db.Column(db.String(100), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Tower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    description = db.Column(db.String(100), index=True)


class TiltRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    towerId = db.Column(db.Integer, db.ForeignKey('tower.id'))
    towerUpperE = db.Column(db.String(100), index=True)
    towerUpperS = db.Column(db.String(100), index=True)
    towerUpperW = db.Column(db.String(100), index=True)
    towerUpperN = db.Column(db.String(100), index=True)
    towerBottomE = db.Column(db.String(100), index=True)
    towerBottomS = db.Column(db.String(100), index=True)
    towerBottomW = db.Column(db.String(100), index=True)
    towerBottomN = db.Column(db.String(100), index=True)
    towerTilt = db.Column(db.String(100), index=True)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(100), index=True)
    title = db.Column(db.String(100), index=True)

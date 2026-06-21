"""数据库模型定义"""

from appdir import db


class User(db.Model):
    """用户"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(256))  # 存储哈希值，需要更长的字段

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


class Tower(db.Model):
    """杆塔"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    description = db.Column(db.String(100), index=True)


class TiltRecord(db.Model):
    """杆塔倾斜记录"""
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    towerId = db.Column(db.Integer, db.ForeignKey('tower.id'))
    towerUpperE = db.Column(db.String(100))
    towerUpperS = db.Column(db.String(100))
    towerUpperW = db.Column(db.String(100))
    towerUpperN = db.Column(db.String(100))
    towerBottomE = db.Column(db.String(100))
    towerBottomS = db.Column(db.String(100))
    towerBottomW = db.Column(db.String(100))
    towerBottomN = db.Column(db.String(100))
    towerTilt = db.Column(db.String(100))


class Article(db.Model):
    """文章"""
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(100), index=True)
    title = db.Column(db.String(100), index=True)

"""Flask CLI 命令"""

from datetime import datetime

import click
from werkzeug.security import generate_password_hash

from appdir import app, db
from appdir.models import User, Article, Question, Answer, Tower, TiltRecord
from appdir.utils.dataset import dic_article, dic_forum, dict_tower, dict_tiltData


@app.cli.command("print")
def printf():
    click.echo("hello world")


@app.cli.command("initdb")
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """初始化数据库"""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command("admin")
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """创建管理员用户"""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.password = generate_password_hash(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')


@app.cli.command("addArticle")
def addArticle():
    for key, v in dic_article.items():
        title = v.split("/")[1]
        title = title.split(".")[0]
        article = Article(id=key, path=v, title=title)
        db.session.add(article)
    db.session.commit()
    click.echo('add articles!')


@app.cli.command("initForum")
def initForum():
    for item in dic_forum:
        questionId = item['id']
        title = item['title']
        question = item['question']
        answer = item['answer']
        q = Question(id=questionId, title=title, question=question, datetime=datetime.now())
        a = Answer(content=answer, question_id=questionId)
        db.session.add(q)
        db.session.add(a)
    db.session.commit()
    click.echo('init forum success!')


@app.cli.command("initTower")
def initTower():
    for item in dict_tower:
        id = item['id']
        name = item['name']
        description = item['description']
        t = Tower(id=id, name=name, description=description)
        db.session.add(t)
    db.session.commit()
    click.echo('init tower success!')


@app.cli.command("initTiltData")
def initTiltData():
    for item in dict_tiltData:
        towerId = item['towerId']
        towerUpperE = item['towerUpperE']
        towerUpperS = item['towerUpperS']
        towerUpperW = item['towerUpperW']
        towerUpperN = item['towerUpperN']
        towerBottomE = item['towerBottomE']
        towerBottomS = item['towerBottomS']
        towerBottomW = item['towerBottomW']
        towerBottomN = item['towerBottomN']
        towerTilt = item['towerTilt']
        t = TiltRecord(towerId=towerId,
                       towerUpperE=towerUpperE,
                       towerUpperS=towerUpperS,
                       towerUpperW=towerUpperW,
                       towerUpperN=towerUpperN,
                       towerBottomE=towerBottomE,
                       towerBottomS=towerBottomS,
                       towerBottomW=towerBottomW,
                       towerBottomN=towerBottomN,
                       datetime=datetime.now(),
                       towerTilt=towerTilt)
        db.session.add(t)
    db.session.commit()
    click.echo('init tiltData success!')


if __name__ == '__main__':
    addArticle()

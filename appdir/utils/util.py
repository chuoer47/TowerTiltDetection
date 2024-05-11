from datetime import datetime

from flask import flash, redirect, url_for, session

from appdir import db
from appdir.models import User, Question, Answer, TiltRecord, Tower, Article
from appdir.utils.algorithm import cal


def datetime2day(datetime):
    # 处理一下日期格式
    datetime = str(datetime)
    datetime = datetime.split(" ")[0]
    return datetime


# ——————————————————————————————————————
# 下面为注册登录所需方法
def validate_register(username, password, repassword):
    if password != repassword:
        flash('Passwords do not match!', 'error')
        return redirect(url_for('register'))
    if User.query.filter(User.username == username).first():
        flash('The username has been used!', 'error')
        return redirect(url_for('register'))
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    flash('User registered with username: {}'.format(username), 'success')
    return redirect(url_for('index'))


def validate_login(username, password):
    user_in_db = User.query.filter(User.username == username).first()
    if not user_in_db:
        flash('No user found with username: {}'.format(username), 'error')
        return redirect(url_for('login'))
    if user_in_db.password == password:
        flash('Login successfully!', 'success')
        session["USERNAME"] = user_in_db.username
        session["USERID"] = user_in_db.id
        return redirect(url_for('root'))
    flash('Incorrect Password', 'error')
    return redirect(url_for('login'))


# ——————————————————————————————


# ——————————————————————————————
# 添加问题到数据库
def addQuestion(title, question):
    if not title and not question:
        flash("Please fill in all the required fields", 'error')
        return redirect(url_for('consult'))
    now_time = datetime.now()
    question = Question(title=title, question=question, datetime=now_time)
    db.session.add(question)
    db.session.commit()
    flash("success question with title:{}".format(title), 'success')
    return


# ——————————————————————————————


# ————————————————————————————————————
# 下面为论坛的开发模块需要的方法
def get_all_questions():
    questions = Question.query.all()
    question_data = []
    for question in questions:
        datetime = datetime2day(question.datetime)
        question_data.append({
            'id': question.id,
            'title': question.title,
            'question': question.question,
            'datetime': datetime,
            'user_id': question.user_id
        })
    return question_data


def getAnswerById(questionId):
    answers = Answer.query.filter(Answer.question_id == questionId)

    answer_data = []
    for answer in answers:
        answer_data.append({
            'id': answer.id,
            'content': answer.content,
            'user_id': answer.user_id,
            'question_id': answer.question_id
        })
    return answer_data


# ——————————————————————————————————


# ——————————————————————————————————
# 下面是杆塔中心表单的处理函数:

def solveTowerTiltRecord(request):
    towerId = request.form.get('towerId')
    towerUpperE = request.form.get('towerUpperE')
    towerUpperS = request.form.get('towerUpperS')
    towerUpperW = request.form.get('towerUpperW')
    towerUpperN = request.form.get('towerUpperN')
    towerBottomE = request.form.get('towerBottomE')
    towerBottomS = request.form.get('towerBottomS')
    towerBottomW = request.form.get('towerBottomW')
    towerBottomN = request.form.get('towerBottomN')
    if not towerId and not towerUpperE and not towerUpperS and not towerUpperW and not towerUpperN and not towerBottomE and not towerBottomS and not towerBottomW and not towerBottomN:
        flash("请填写完整,注意数据要1个空格隔开", 'error')
        return redirect(url_for('towerTiltForm'))
    now_time = datetime.now()
    towerTilt = cal(towerUpperE=towerUpperE,
                    towerUpperS=towerUpperS,
                    towerUpperW=towerUpperW,
                    towerUpperN=towerUpperN,
                    towerBottomE=towerBottomE,
                    towerBottomS=towerBottomS,
                    towerBottomW=towerBottomW,
                    towerBottomN=towerBottomN)
    if None:
        flash("请填写正确的格式", 'error')
        return redirect(url_for('towerTiltForm'))
    tiltRecord = TiltRecord(datetime=now_time,
                            towerId=towerId,
                            towerUpperE=towerUpperE,
                            towerUpperS=towerUpperS,
                            towerUpperW=towerUpperW,
                            towerUpperN=towerUpperN,
                            towerBottomE=towerBottomE,
                            towerBottomS=towerBottomS,
                            towerBottomW=towerBottomW,
                            towerBottomN=towerBottomN,
                            towerTilt=towerTilt
                            )
    db.session.add(tiltRecord)
    db.session.commit()
    flash("记录成功", 'success')
    return


def get_all_tower():
    """
    获取所有杆塔，返回杆塔可迭代表格
    :return:
    """
    towers = Tower.query.all()
    tower_data = []
    for tower in towers:
        tower_data.append({
            'id': tower.id,
            'name': tower.name,
            'description': tower.description,
        })
    return tower_data


def solveAddTower(name, description):
    if not name and not description:
        flash("请填写完整", 'error')
        return redirect(url_for('addTower'))
    tower = Tower(name=name, description=description)
    db.session.add(tower)
    db.session.commit()
    flash("记录成功", 'success')
    return


def getTowerInfoById(towerId):
    towers = TiltRecord.query.filter(TiltRecord.towerId == int(towerId))
    data = []
    for t in towers:
        data.append({
            'id': t.id,
            'datetime': t.datetime,
            'towerId': t.towerId,
            'towerUpperE': t.towerUpperE,
            'towerUpperS': t.towerUpperS,
            'towerUpperW': t.towerUpperW,
            'towerUpperN': t.towerUpperN,
            'towerBottomE': t.towerBottomE,
            'towerBottomS': t.towerBottomS,
            'towerBottomW': t.towerBottomW,
            'towerBottomN': t.towerBottomN,
            'towerTilt': t.towerTilt
        })
    return data


# ——————————————————————————————————


# 获得所有文章
def get_all_articles():
    datas = Article.query.all()
    resultList = []
    for data in datas:
        resultList.append({
            'id': data.id,
            'title': data.title,
            'path': data.path
        })
    return resultList

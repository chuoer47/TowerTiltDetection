"""业务逻辑工具函数"""

from datetime import datetime

from flask import flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from appdir import db
from appdir.models import User, Question, Answer, TiltRecord, Tower, Article
from appdir.utils.algorithm import cal


def datetime_to_day(dt):
    """将 datetime 对象格式化为日期字符串"""
    return str(dt).split(" ")[0]


# ——————————————————————————————————————
# 注册登录
def validate_register(username, password, repassword):
    if password != repassword:
        flash('Passwords do not match!', 'error')
        return redirect(url_for('register'))
    if User.query.filter(User.username == username).first():
        flash('The username has been used!', 'error')
        return redirect(url_for('register'))
    user = User(username=username, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    session["USERNAME"] = user.username
    session["USERID"] = user.id
    flash('注册成功！欢迎 {}'.format(username), 'success')
    return redirect(url_for('index'))


def validate_login(username, password):
    user_in_db = User.query.filter(User.username == username).first()
    if not user_in_db:
        flash('No user found with username: {}'.format(username), 'error')
        return redirect(url_for('login'))
    if check_password_hash(user_in_db.password, password):
        flash('Login successfully!', 'success')
        session["USERNAME"] = user_in_db.username
        session["USERID"] = user_in_db.id
        return redirect(url_for('root'))
    flash('Incorrect Password', 'error')
    return redirect(url_for('login'))


# ——————————————————————————————————————
# 论坛问题
def add_question(title, question):
    if not title or not question:
        flash("Please fill in all the required fields", 'error')
        return redirect(url_for('consult'))
    now_time = datetime.now()
    new_question = Question(title=title, question=question, datetime=now_time)
    db.session.add(new_question)
    db.session.commit()
    flash("success question with title:{}".format(title), 'success')
    return


def get_all_questions():
    questions = Question.query.all()
    question_data = []
    for q in questions:
        date_str = datetime_to_day(q.datetime)
        question_data.append({
            'id': q.id,
            'title': q.title,
            'question': q.question,
            'datetime': date_str,
            'user_id': q.user_id
        })
    return question_data


def get_answer_by_id(question_id):
    answers = Answer.query.filter(Answer.question_id == question_id)
    answer_data = []
    for answer in answers:
        answer_data.append({
            'id': answer.id,
            'content': answer.content,
            'user_id': answer.user_id,
            'question_id': answer.question_id
        })
    return answer_data


# ——————————————————————————————————————
# 杆塔中心
def solve_tower_tilt_record(req):
    tower_id = req.form.get('towerId')
    tower_upper_e = req.form.get('towerUpperE')
    tower_upper_s = req.form.get('towerUpperS')
    tower_upper_w = req.form.get('towerUpperW')
    tower_upper_n = req.form.get('towerUpperN')
    tower_bottom_e = req.form.get('towerBottomE')
    tower_bottom_s = req.form.get('towerBottomS')
    tower_bottom_w = req.form.get('towerBottomW')
    tower_bottom_n = req.form.get('towerBottomN')

    # 校验：任一字段为空则报错
    if not all([tower_id, tower_upper_e, tower_upper_s, tower_upper_w, tower_upper_n,
                tower_bottom_e, tower_bottom_s, tower_bottom_w, tower_bottom_n]):
        flash("请填写完整,注意数据要1个空格隔开", 'error')
        return redirect(url_for('tower_tilt_form', tower_id=tower_id or 0))

    now_time = datetime.now()
    tower_tilt = cal(towerUpperE=tower_upper_e,
                     towerUpperS=tower_upper_s,
                     towerUpperW=tower_upper_w,
                     towerUpperN=tower_upper_n,
                     towerBottomE=tower_bottom_e,
                     towerBottomS=tower_bottom_s,
                     towerBottomW=tower_bottom_w,
                     towerBottomN=tower_bottom_n)
    if tower_tilt is None:
        flash("请填写正确的格式", 'error')
        return redirect(url_for('tower_tilt_form', tower_id=tower_id))

    tilt_record = TiltRecord(
        datetime=now_time,
        towerId=tower_id,
        towerUpperE=tower_upper_e,
        towerUpperS=tower_upper_s,
        towerUpperW=tower_upper_w,
        towerUpperN=tower_upper_n,
        towerBottomE=tower_bottom_e,
        towerBottomS=tower_bottom_s,
        towerBottomW=tower_bottom_w,
        towerBottomN=tower_bottom_n,
        towerTilt=tower_tilt
    )
    db.session.add(tilt_record)
    db.session.commit()
    flash("记录成功", 'success')
    return


def get_all_tower():
    """获取所有杆塔，返回杆塔可迭代表格"""
    towers = Tower.query.all()
    tower_data = []
    for tower in towers:
        tower_data.append({
            'id': tower.id,
            'name': tower.name,
            'description': tower.description,
        })
    return tower_data


def solve_add_tower(name, description):
    if not name or not description:
        flash("请填写完整", 'error')
        return redirect(url_for('add_tower'))
    tower = Tower(name=name, description=description)
    db.session.add(tower)
    db.session.commit()
    flash("记录成功", 'success')
    return


def get_tower_info_by_id(tower_id):
    towers = TiltRecord.query.filter(TiltRecord.towerId == int(tower_id))
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


def get_all_articles():
    """获得所有文章"""
    articles = Article.query.all()
    result = []
    for data in articles:
        result.append({
            'id': data.id,
            'title': data.title,
            'path': data.path
        })
    return result

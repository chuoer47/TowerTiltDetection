"""
该类设置路由
"""

from flask import render_template, request

from appdir import app
from appdir.forms import AnswerForm
from appdir.models import *
from appdir.utils.dataset import dic_article
from appdir.utils.util import validate_register, validate_login, addQuestion, get_all_questions, getAnswerById, \
    solveTowerTiltRecord, solveAddTower, get_all_tower, getTowerInfoById, get_all_articles


# 根路由
@app.route('/', methods=['GET', 'POST'])
def root():
    return index()


# 首页
@app.route('/index', methods=['GET', 'POST'])
def index():  # put application's code here
    return render_template('index.html')


# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
        validate_login(username, password)
        return render_template('other/login.html')
    else:
        return render_template('other/login.html')


# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        validate_register(username, password, repassword)
        return render_template('other/register.html')
    else:
        return render_template('other/register.html')


# 文章信息
@app.route('/info', methods=['GET', 'POST'])
def info():  # put application's code here
    return render_template('info.html',
                           articles=get_all_articles())


# ——————————————————————————————————————————————————
# 下面为杆塔中心 & 杆塔倾斜表格
# 杆塔中心
@app.route('/towerCenter', methods=['GET', 'POST'])
def towerCenter():  # put application's code here
    return render_template('TowerTiltCenter/towerCenter.html', towers=get_all_tower())


# 杆塔倾斜表格
@app.route('/towerTiltForm<towerId>', methods=['GET', 'POST'])
def towerTiltForm(towerId):  # put application's code here
    if request.method == 'POST':
        towerId = request.form.get('towerId')
        towerUpperE = request.form.get('towerUpperE')
        towerUpperS = request.form.get('towerUpperS')
        towerUpperW = request.form.get('towerUpperW')
        towerUpperN = request.form.get('towerUpperN')
        towerBottomE = request.form.get('towerBottomE')
        towerBottomS = request.form.get('towerBottomS')
        towerBottomW = request.form.get('towerBottomW')
        towerBottomN = request.form.get('towerBottomN')
        solveTowerTiltRecord(request)
        return render_template('TowerTiltCenter/towerTiltForm.html',
                               towerId=towerId,
                               towerUpperE=towerUpperE,
                               towerUpperS=towerUpperS,
                               towerUpperW=towerUpperW,
                               towerUpperN=towerUpperN,
                               towerBottomE=towerBottomE,
                               towerBottomS=towerBottomS,
                               towerBottomW=towerBottomW,
                               towerBottomN=towerBottomN)
    return render_template('TowerTiltCenter/towerTiltForm.html',
                           towerId=towerId)


# 添加杆塔
@app.route('/addTower', methods=['GET', 'POST'])
def addTower():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        solveAddTower(name, description)
        return render_template('TowerTiltCenter/addTower.html',
                               name=name,
                               description=description)
    return render_template('TowerTiltCenter/addTower.html')


@app.route('/towerDetail<towerId>', methods=['GET', 'POST'])
def towerDetail(towerId):
    tower = Tower.query.filter(Tower.id == towerId).first()
    if not tower:
        tower = []
    towerTilt = getTowerInfoById(towerId)
    if not towerTilt:
        towerTilt = []
    return render_template('TowerTiltCenter/towerDetail.html',
                           tower=tower,
                           towerTilt=towerTilt)


# ——————————————————————————————————————————————————————————————————————

# 关于我们
@app.route('/aboutUs', methods=['GET', 'POST'])
def aboutUs():  # put application's code here
    return render_template('other/aboutUs.html')


# ————————————————————————————————————————————————————
# 下面为论坛部分

# 添加论坛问题
@app.route('/consult', methods=['GET', 'POST'])
def consult():  # put application's code here
    if request.method == 'POST':
        title = request.form.get('title')
        question = request.form.get('question')
        addQuestion(title, question)  # 数据库添加论坛问题
        return render_template('consult.html', title=title, question=question, message="success")
    else:
        return render_template('consult.html')


# 访问论坛
@app.route('/forum', methods=['GET', 'POST'])
def forum():
    return render_template('forum.html', questions=get_all_questions())


# 问题详情页
@app.route('/question<question_id>', methods=['GET', 'POST'])
def question(question_id):
    current_question = Question.query.filter(Question.id == question_id).first()
    answers = getAnswerById(question_id)
    answer_form = AnswerForm()
    return render_template('question.html',
                           question=current_question, answers=answers,
                           answer_form=answer_form)


# —————————————————————————————————————————————————————————————

# ————————————————————————————————————————————————————————————
# 以下为文章的路由地址

@app.route('/article<id>', methods=['GET', 'POST'])
def article(id):
    link = dic_article[int(id)]
    return render_template(link)

# ——————————————————————————————————————————————————————————

"""路由定义"""

from flask import render_template, request, session, redirect, url_for

from appdir import app
from appdir.forms import AnswerForm
from appdir.models import Question, Tower
from appdir.utils.dataset import dic_article
from appdir.utils.util import (
    validate_register, validate_login, add_question, get_all_questions,
    get_answer_by_id, solve_tower_tilt_record, solve_add_tower,
    get_all_tower, get_tower_info_by_id, get_all_articles
)


# 根路由
@app.route('/', methods=['GET', 'POST'])
def root():
    return index()


# 首页
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        return validate_login(username, password)
    return render_template('other/login.html')


# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        return validate_register(username, password, repassword)
    return render_template('other/register.html')


# 退出登录
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# 文章信息
@app.route('/info', methods=['GET', 'POST'])
def info():
    return render_template('info.html', articles=get_all_articles())


# ——————————————————————————————————————————————————
# 杆塔中心
@app.route('/towerCenter', methods=['GET', 'POST'])
def tower_center():
    return render_template('TowerTiltCenter/towerCenter.html', towers=get_all_tower())


# 杆塔倾斜表格
@app.route('/towerTiltForm/<int:tower_id>', methods=['GET', 'POST'])
def tower_tilt_form(tower_id):
    if request.method == 'POST':
        solve_tower_tilt_record(request)
        # 用提交的数据重新渲染页面
        return render_template('TowerTiltCenter/towerTiltForm.html',
                               towerId=request.form.get('towerId'),
                               towerUpperE=request.form.get('towerUpperE'),
                               towerUpperS=request.form.get('towerUpperS'),
                               towerUpperW=request.form.get('towerUpperW'),
                               towerUpperN=request.form.get('towerUpperN'),
                               towerBottomE=request.form.get('towerBottomE'),
                               towerBottomS=request.form.get('towerBottomS'),
                               towerBottomW=request.form.get('towerBottomW'),
                               towerBottomN=request.form.get('towerBottomN'))
    return render_template('TowerTiltCenter/towerTiltForm.html',
                           towerId=tower_id)


# 添加杆塔
@app.route('/addTower', methods=['GET', 'POST'])
def add_tower():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        solve_add_tower(name, description)
        return render_template('TowerTiltCenter/addTower.html',
                               name=name,
                               description=description)
    return render_template('TowerTiltCenter/addTower.html')


@app.route('/towerDetail/<int:tower_id>', methods=['GET', 'POST'])
def tower_detail(tower_id):
    tower = Tower.query.filter(Tower.id == tower_id).first()
    if not tower:
        tower = []
    tower_tilt = get_tower_info_by_id(tower_id)
    if not tower_tilt:
        tower_tilt = []
    return render_template('TowerTiltCenter/towerDetail.html',
                           tower=tower,
                           towerTilt=tower_tilt)


# ——————————————————————————————————————————————————————————————————————

# 关于我们
@app.route('/aboutUs', methods=['GET', 'POST'])
def about_us():
    return render_template('other/aboutUs.html')


# ————————————————————————————————————————————————————
# 论坛部分

# 添加论坛问题
@app.route('/consult', methods=['GET', 'POST'])
def consult():
    if request.method == 'POST':
        title = request.form.get('title')
        question = request.form.get('question')
        add_question(title, question)
        return render_template('consult.html', title=title, question=question, message="success")
    return render_template('consult.html')


# 访问论坛
@app.route('/forum', methods=['GET', 'POST'])
def forum():
    return render_template('forum.html', questions=get_all_questions())


# 问题详情页
@app.route('/question/<int:question_id>', methods=['GET', 'POST'])
def question_detail(question_id):
    current_question = Question.query.filter(Question.id == question_id).first()
    answers = get_answer_by_id(question_id)
    answer_form = AnswerForm()
    return render_template('question.html',
                           question=current_question, answers=answers,
                           answer_form=answer_form)


# —————————————————————————————————————————————————————————————

# 文章路由
@app.route('/article/<int:article_id>', methods=['GET', 'POST'])
def article(article_id):
    link = dic_article[int(article_id)]
    return render_template(link)

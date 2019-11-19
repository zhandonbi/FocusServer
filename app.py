# coding=UTF-8
from flask import Flask, request, render_template
from UserLogin.UserOperator import StudentMessageCenter as SMC
from userDB.DB_user import FocusUserDB as FUD
from userDB.DB_class import FocusClassDB as FCD

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


# 用户登录
@app.route('/login/', methods=['GET', 'POST'])
def login():
    login_or_success = False
    login_message = 'null'
    username = request.form['username']
    password = request.form['password']
    JL = SMC(username, password)
    db = FUD()

    login_or_success, login_message = JL.login_vpn()
    return {
        'login_status': login_or_success,
        'username': JL.find_userInfo(),
        'login_message': login_message}


# 获取课表
@app.route('/get_schedule/', methods=['POST'])
def schedule():
    username = request.form['username']
    password = request.form['password']
    # school_year = request.form['school_year']
    JL = SMC(username, password)
    JL.login_vpn()
    body, extra = JL.get_schedule('2019-2020-1')
    return {
        'schedule_body': body,
        "schedule_extra": extra
    }


# 获取已注册用户信息
@app.route('/get_user_message/', methods=['POST'])
def search_user():
    user_id = request.form['study_number']
    db_operator = FUD()
    status, message = db_operator.search_user(user_id)
    db_operator.close()
    return {
        'search_status': status,
        'search_message': message
    }


# 新用户注册
@app.route('/sign_in/', methods=['POST'])
def sign_in():
    name = request.form['name']
    message = {
        'study_number': request.form['study_number'],
        'nickname': request.form['nickname'],
        'name': name,
        'sex': request.form['sex'],
        'major': request.form['major']
    }
    db_operator = FUD()
    status, add_message = db_operator.add_user(message)
    db_operator.close()
    return {
        'sign_in_status': status,
        'sign_in_message': add_message
    }


# 编辑已注册用户信息
@app.route('/edit_user_message/', methods=['POST'])
def edit_user_message():
    messages = {
        'study_number': request.form['study_number'],
        'nickname': request.form['nickname'],
        'name': request.form['name'],
        'sex': request.form['sex'],
        'major': request.form['major']
    }
    db_operator = FUD()
    status, message = db_operator.update_user(messages)
    db_operator.close()
    return {
        'sign_in_status': status,
        'sign_in_message': message
    }


# 增加新的课表用户
@app.route('/creat_new_user_class/', methods=['POST'])
def creat_new_user_class():
    db_operator = FCD()
    status, message = db_operator.add_user(request.form['study_number'])
    db_operator.close()
    return {
        'status': status,
        'message': message
    }

# 查找指定用户课程计时
@app.route('/get_class_status/', methods=['POST'])
def get_class_status():
    db_operator = FCD()
    status, messages = db_operator.read_class(request.form['study_number'])
    db_operator.close()
    return {
        'status': status,
        'subjects': messages['subjects'],
        'time': messages['time']
    }

# 编辑
@app.route('/edit_class_status/', methods=['POST'])
def edit_class_status():
    study_number = request.form['study_number']
    subjects = request.form['subjects']
    time = request.form['time']
    db_operator = FCD()
    status, message = db_operator.update_class(study_number, subjects, time)
    db_operator.close()
    return {'status': status,
            'message': message}

#读取论坛信息
@app.route('/talk_message/', methods=['POST'])
def talk_message():
    ID = request.form['study_number']
    fud = FUD()
    status, message = fud.read_message(ID)
    return {
        'status': status,
        'message': message
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)

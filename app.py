# coding=UTF-8
from flask import Flask, request, render_template
from UserLogin.UserOperator import StudentMessageCenter as SMC
from userDB.DBoperator import FocusUserDB as FUD

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/login/', methods=['GET', 'POST'])
def login():
    login_or_success = False
    login_message = 'null'
    username = request.form['username']
    password = request.form['password']
    JL = SMC(username, password)
    login_or_success, login_message = JL.login_vpn()
    return {
        'login_status': login_or_success,
        'username': JL.find_userInfo(),
        'login_message': login_message}


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


@app.route('/get_user_message', methods=['POST'])
def search_user():
    user_id = request.form['studynumber']
    db_operator = FUD()
    status, message = db_operator.search_user(user_id)
    return {
        'search_status': status,
        'search_message': message
    }


@app.route('/sign_in/', methods=['POST'])
def sign_in():
    message = {
        'studynumber': request.form['studynumber'],
        'nickname': request.form['nickname'],
        'name': request.form['name'],
        'sex': request.form['sex'],
        'major': request.form['major']
    }
    db_operator = FUD()
    status, add_message = db_operator.add_user(message)
    return {
        'sign_in_status': status,
        'sign_in_message': add_message
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)

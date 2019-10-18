# coding=UTF-8
from flask import Flask, request, render_template
from UserLogin.UserOperator import StudentMessageCenter as SMC

app = Flask(__name__)


@app.route('/')
def FSS():
    return render_template('login.html')


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


@app.route('/get_schedule/', methods=['GET', 'POST'])
def schedule():
    username = request.form['username']
    password = request.form['password']
    JL = SMC(username, password)
    JL.login_vpn()
    return JL.get_schedule()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

# coding=UTF-8
from flask import Flask, request, render_template
from UserLogin.UserOperator import StudentMessageCenter as SMC

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

import pymysql
import json


class FocusUserDB():
    def __init__(self):
        self.DB_hosts = ''
        self.DB_port = ''
        self.DB_user = ''
        self.DB_password = ''
        self.DB = ''
        self.load_db_link()
        self.DB_operator = pymysql.connect(host=self.DB_hosts, port=self.DB_port, user=self.DB_user,
                                           passwd=self.DB_password,
                                           db=self.DB)
        self.cur = self.DB_operator.cursor()

    # 读取数据库连接信息
    def load_db_link(self):
        with open('./Focus_DB.json') as file_obj:
            group = json.load(file_obj)
        self.DB_hosts = group['hosts']
        self.DB_port = group['port']
        self.DB_user = group['user']
        self.DB_password = group['password']
        self.DB = group['db']
    # 关闭连接
    def close(self):
        self.DB_operator.close()

    # 添加用户
    def add_user(self, user_messages):
        ID = '"' + user_messages['studynumber'] + '",'
        nick = '"' + user_messages['nickname'] + '",'
        name = '"' + user_messages['name'] + '",'
        sex = '"' + user_messages['sex'] + '",'
        major = '"' + user_messages['major'] + '"'
        values = ID + nick + name + sex + major
        sql = "insert into user_message(studynumber, nickname, name, sex, major) values(" + values + ")"
        status, message = self.search_user(user_messages['studynumber'])
        if status:
            return False, "添加失败，用户已存在"
        self.cur.execute(sql)
        self.DB_operator.commit()
        return True, "SUCCESS"

    # 搜索指定ID信息
    def search_user(self, user_id):
        sql = 'select ' + '*' + ' from user_message where studynumber=' + user_id
        self.cur.execute(sql)
        results = self.cur.fetchall()
        if len(results) == 0:
            return False, 'Null'
        return True, \
               {"studynumber": results[0][0],
                "nickname": results[0][1],
                "name": results[0][2],
                "sex": results[0][3],
                "major": results[0][4]}

'''
test_p = {
    "studynumber": '182210711206',
    "nickname": 'xhy',
    "name": '徐海艺',
    "sex": '女',
    "major": '计算机科学与技术'}

test = FocusUserDB()
print(test.add_user(test_p))
test.close()
'''
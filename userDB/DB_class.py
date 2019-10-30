import pymysql
import json


class FocusClassDB():
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
        with open('./userDB/Focus_DB.json') as file_obj:
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
    def add_user(self, user_id):
        id = '"' + user_id + '"'
        sql = "insert into user_class(study_number) values(" + id + ")"
        status, message = self.read_class(user_id)
        if not status and message['subjects'] == 'Null_user':
            self.cur.execute(sql)
            self.DB_operator.commit()
            return True, "添加成功"
        elif not status and message['subjects'] == 'Null_message':
            return False, "添加失败，用户已存在"
        elif status:
            return False, "添加失败，用户已存在"

    # 读取课程时间相关信息
    def read_class(self, user_id):
        sql = 'select subjects,time from user_class where study_number=' + user_id
        self.cur.execute(sql)
        results = self.cur.fetchall()
        if len(results) == 0:
            return False, \
                   {
                       "subjects": "Null_user",
                       "time": "Null_user"
                   }
        else:
            if (results[0][0] is None and results[0][0] is None) or (results[0][0] == '' and results[0][0] == ''):
                return False, \
                       {
                           "subjects": "Null_message",
                           "time": "Null_message"
                       }
            else:
                return True, \
                       {
                           "subjects": results[0][0],
                           "time": results[0][1]
                       }

    # 修改课程时间相关
    def update_class(self, user_id, class_name, class_time):
        values = 'subjects="' + class_name + '",time="' + class_time + '"'
        sql = 'update user_class set ' + values + ' where study_number="' + user_id + '"'
        status, message = self.read_class(user_id)
        if (not status and message['subjects'] == 'Null_message') or status:
            try:
                self.cur.execute(sql)
                self.DB_operator.commit()
            except Exception as e:
                raise Exception("写入课程相关信息异常：{}".format(e))
            return True, '修改成功'
        else:
            return False, '修改失败'+message['subjects']


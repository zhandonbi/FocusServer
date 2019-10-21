import pymysql
import json


class FocusUserDB():
    def __init__(self):
        self.DB_hosts = ''
        self.DB_port = ''
        self.DB_user = ''
        self.DB_password = ''
        self.load_db_link()
        self.DB_operator = pymysql.connect()

    def load_db_link(self):
        with open('./Focus_DB.json') as file_obj:
            group = json.load(file_obj)
        self.DB_hosts = group['hosts']
        self.DB_port = group['port']
        self.DB_user = group['user']
        self.DB_password = group['password']

    def link(self):
        try:
            self.DB_operator(host=self.DB_hosts, port=self.DB_port, user=self.DB_user, passwd=self.DB_password)
        except Exception as e:
            raise Exception('连接失败数据库失败:{}'.format(e))
        print(self.DB_operator)



from userDB.load_db import Load


class TalkHome:
    def __init__(self):
        self.DB_load = Load('./userDB/talk_home_DB.json')
        self.DB_operator = self.DB_load.get_DB_operator()
        self.DB_cur = self.DB_load.get_DB_cur()

    # 关闭连接
    def close(self):
        self.DB_load.close()

    # 搜索帖子
    def search_talk(self, talk_name):
        sql = 'select * from que_list where talk_name="' + talk_name + '"'
        self.DB_cur.execute(sql)
        res = self.DB_cur.fetchall()
        if len(res) == 0:
            return True
        else:
            return False

    #  获取话题列表
    def get_talk_list(self, post_NUM):
        talk_list = []
        for i in range(1, 11):
            sql = 'select * from que_list'
            self.DB_cur.execute(sql)
            ress = self.DB_cur.fetchall()
            for res in ress:
                temp_dir = {
                    'talk_name': res[1],
                    'que_usr': res[2],
                    'que_text': res[3],
                    'que_time': res[4],
                    'ans_num': res[5]
                }
                talk_list.append(temp_dir)
        return talk_list

    # 读取某一个话题
    def read_talk(self, talk_name):
        or_exits = self.search_talk(talk_name)
        dir = {}
        if not or_exits:
            sql = 'SELECT * FROM ' + talk_name
            self.DB_cur.execute(sql)
            res = self.DB_cur.fetchall()
            for i in range(0, len(res)):
                base_dir = {
                    'ans_usr': res[i][1],
                    'ans_time': res[i][2],
                    'ans_text': res[i][3]
                }
                dir[str(i)] = base_dir
        return dir

    # 读取指定用户发布话题
    def read_user_talk(self, user_name):
        talk_list = []
        sql = 'select * from que_list where que_user = "' + user_name + '"'
        self.DB_cur.execute(sql)
        ress = self.DB_cur.fetchall()
        if len(ress) != 0:
            for res in ress:
                temp_dir = {
                    'talk_name': res[1],
                    'que_usr': res[2],
                    'que_text': res[3],
                    'que_time': res[4],
                    'ans_num': res[5]
                }
                talk_list.append(temp_dir)
        return talk_list

    # 创建话题
    def creat_talk(self, talk_name, que_user, que_text, que_time):
        values = '"' + talk_name + '","' + que_user + '","' + que_text + '","' + que_time + '","0"'
        sql = 'insert into que_list(talk_name, que_user,que_text , que_time , ans_num ) values (' + values + ')'
        or_exist = self.search_talk(talk_name)
        if or_exist:
            self.DB_cur.execute(sql)
            self.DB_operator.commit()
            self.creat_table(talk_name)
            return True, '话题创建成功'
        else:
            return False, '该话题已存在'

    # 删除话题
    def delete_talk(self, talk_name):
        res = self.search_talk(talk_name)
        sql = 'DELETE FROM que_list where talk_name="' + talk_name + '"'
        if not res:
            self.DB_cur.execute(sql)
            self.DB_operator.commit()
            self.delete_table(talk_name)
            return True
        return True

    # 更新话题
    def update_talk(self, talk_name, ans_user, ans_time, ans_text):
        ans_num = int(self.get_a_message('ans_num', talk_name))
        ans_num += 1
        value = 'ans_num = "' + str(ans_num) + '"'
        value2 = '"' + ans_user + '","' + ans_time + '","' + ans_text + '"'
        sql = 'UPDATE que_list SET ' + value + 'where talk_name="' + talk_name + '"'
        sql2 = 'INSERT INTO ' + talk_name + '(ans_usr, ans_time, ans_text)VALUES(' + value2 + ')'
        if not self.search_talk(talk_name):
            self.DB_cur.execute(sql)
            self.DB_operator.commit()
            self.DB_cur.execute(sql2)
            self.DB_operator.commit()
            return True, '更新话题成功'
        else:
            return False, '话题不存在'

    def get_a_message(self, object, talk_name):
        sql = 'select ' + object + ' from que_list where talk_name="' + talk_name + '"'
        self.DB_cur.execute(sql)
        res = self.DB_cur.fetchall()
        return res[0][0]

    def creat_table(self, talk_name):
        sql = 'CREATE TABLE IF NOT EXISTS ' + talk_name + '(ID INT PRIMARY KEY AUTO_INCREMENT,' \
                                                          'ans_usr VARCHAR(255) NOT NULL,' \
                                                          'ans_time VARCHAR(255) NOT NULL,' \
                                                          'ans_text VARCHAR(255) NOT NULL)'
        self.DB_cur.execute(sql)
        self.DB_operator.commit()

    def delete_table(self, talk_name):
        sql = 'DROP TABLE ' + talk_name
        self.DB_cur.execute(sql)
        self.DB_operator.commit()

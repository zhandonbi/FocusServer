from userDB.load_db import Load


class FocusUserDB():
    def __init__(self):
        self.DB_Load = Load('./userDB/Focus_DB.json')
        self.DB_operator = self.DB_Load.get_DB_operator()
        self.cur = self.DB_Load.get_DB_cur()

    # 关闭连接
    def close(self):
        self.DB_Load.close()

    # 添加用户
    def add_user(self, user_messages):
        id = '"' + user_messages['study_number'] + '",'
        nick = '"' + user_messages['nickname'] + '",'
        name = '"' + user_messages['name'] + '",'
        sex = '"' + user_messages['sex'] + '",'
        major = '"' + user_messages['major'] + '"'
        values = id + nick + name + sex + major
        sql = "insert into user_message(study_number, nickname, name, sex, major) values(" + values + ")"
        status, message = self.search_user(user_messages['study_number'])
        if status:
            return False, "添加失败，用户已存在"
        self.cur.execute(sql)
        self.DB_operator.commit()
        return True, "添加成功"

    # 搜索指定ID信息
    def search_user(self, user_id):
        sql = 'select ' + '*' + ' from user_message where study_number=' + user_id
        self.cur.execute(sql)
        results = self.cur.fetchall()
        if len(results) == 0:
            return False, '此ID不存在'
        return True, \
               {"study_number": results[0][0],
                "nickname": results[0][1],
                "name": results[0][2],
                "sex": results[0][3],
                "major": results[0][4]}

    # 修改用户信息
    def update_user(self, user_messages):
        id = 'study_number="' + user_messages['study_number'] + '"'
        nick = 'nickname="' + user_messages['nickname'] + '",'
        name = 'name="' + user_messages['name'] + '",'
        sex = 'sex="' + user_messages['sex'] + '",'
        major = 'major="' + user_messages['major'] + '"'
        values = nick + name + sex + major
        sql = "update user_message set " + values + " where " + id
        search_status, search_messages = self.search_user(user_messages['study_number'])
        if search_status:
            try:
                self.cur.execute(sql)
                self.DB_operator.commit()
            except Exception as e:
                raise Exception("修改用户数据异常：{}".format(e))
        else:
            return False, search_messages
        return True, "修改成功"

from userDB.load_db import Load


class FocusClassDB():
    def __init__(self):
        self.DB_Load = Load('./userDB/Focus_DB.json')
        self.DB_operator = self.DB_Load.get_DB_operator()
        self.cur = self.DB_Load.get_DB_cur()

    def close(self):
        self.DB_Load.close()

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
            if not status and message['subjects'] == 'Null_user':
                creat_status, creat_message = self.add_user(user_id)
                try:
                    self.cur.execute(sql)
                    self.DB_operator.commit()
                except Exception as e:
                    raise Exception("写入课程相关信息异常：{}".format(e))
                return True, '修改成功{添加了新词条}'



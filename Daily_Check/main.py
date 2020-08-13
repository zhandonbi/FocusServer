import requests
from bs4 import BeautifulSoup
import logging
import json
from http.cookiejar import CookieJar
from Daily_Check import loadExcel
from Daily_Check import getTime

# 模拟一个请求头
headers1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}
headers2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
            "Content-Type": "application/json"}
url_menhu = 'http://ids2.just.edu.cn/cas/login?service=http%3A%2F%2Fmy.just.edu.cn%2F'
url_menhu_old = 'http://my2.just.edu.cn/_web/fusionportal/index.jsp?_p=YXM9MSZwPTEmbT1OJg__'
url_survey = 'http://ehall.just.edu.cn/default/work/jkd/jkxxtb/jkxxcj.jsp'
url_survey_post = 'http://ehall.just.edu.cn/default/work/jkd/jkxxtb/com.sudytech.portalone.base.db.queryBySqlWithoutPagecond.biz.ext'

time = getTime.getTime()
params = {"params": {"empcode": "162210702110", "tbrq": time},
          "querySqlId": "com.sudytech.work.suda.jkxxtb.jkxxtb.queryToday"}


class Login:

    def __init__(self, username, password):
        self.__session = requests.session()
        self.__session.cookies = CookieJar()
        self.__username = username
        self.__password = password
        # 去掉警告
        logging.captureWarnings(True)

    def login(self):
        try:
            response = self.__session.get(url=url_menhu, headers=headers1, verify=False)
            dic = {}
            # 获取表单中的一些参
            lt = BeautifulSoup(response.text, 'html.parser')
            dic['execution'] = lt.select('input[name="execution"]')[0].get("value")
            dic['_eventId'] = lt.select('input[name="_eventId"]')[0].get("value")
            dic['loginType'] = lt.select('input[name="loginType"]')[0].get("value")
            dic['submit'] = lt.select('input[name="execution"]')[0].get("submit")
            dataMenhu = {
                'username': self.__username,
                'password': self.__password,
                'execution': dic['execution'],
                '_eventId': dic['_eventId'],
                'loginType': dic['loginType'],
                'submit': dic['submit']}
            self.__session.post(url=url_menhu, data=dataMenhu, headers=headers1, verify=False)
            self.__session.get(url=url_menhu, headers=headers1, verify=False)
            response = self.__session.get(url=url_menhu, headers=headers1, verify=False)
            if "统一身份认证登录" in response.text:
                return False, self.__session
            else:
                return True, self.__session
        except Exception as e:
            return False, self.__session


def run_check():
    res = ''
    llogin = Login("182210711235", "252414")
    flag, session = llogin.login()
    if flag:
        session.get(url=url_survey, headers=headers2, stream=True)
        data = loadExcel.loadData()
        temp_i = 0
        for i in data:
            userID = i['userID']
            params["params"]["empcode"] = userID
            response = session.post(url_survey_post, data=str(params), headers=headers2, verify=False)
            res_list = json.loads(response.text)
            if len(res_list["list"]) == 0:
                temp_i += 1
                print(i['name'])
                res += '[{}]{}--未填写<br/>'.format(time, i['name'])
        temp_res = res
        res = '未填写人数:{}<br/>' \
              '{}' \
              '------------------------------<br/>' \
              '!!!此网络接口仅供1822107112使用!!!<br/>' \
              'API上次更新日期[2020/08/13]'.format(temp_i, temp_res)
    return res

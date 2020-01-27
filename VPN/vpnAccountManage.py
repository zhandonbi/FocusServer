import requests
import json
import re
import random

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    , 'Origin': 'https://vpn.just.edu.cn',
    'Upgrade-Insecure-Requests': '1'
}
cookies = {
    'lastRealm': 'LDAP-REALM',
    'DSSIGNIN': 'url_default',
    'WWHTJIKTLSN_Impl': 'javascript',
    'DSLastAccess': '1510459958'
}


class VpnAccountGet():
    def __init__(self):
        self.account_list = {}
        self.load_account_list()
        self.session = requests.session()
        self.session.keep_alive = False

    def load_account_list(self):
        with open('./VPN/vpn_account.json') as file_read:
            self.account_list = json.load(file_read)

    def vpn_account_or_using(self, username, password):
        '''

        :param username: 学号
        :param password: 密码（学校vpn为身份证后六位）
        :return: 如果账户在使用返回True
        '''

        url = "https://vpn.just.edu.cn/dana-na/auth/url_default/login.cgi"
        login_out_url = 'https://vpn.just.edu.cn/dana-na/auth/logout.cgi'
        vpn_data = {
            'tz_offset': '480',
            'username': username,
            'password': password,
            'realm': 'LDAP-REALM',
            'btnSubmit': '登录'
        }
        self.session.close()
        try:
            requests.packages.urllib3.disable_warnings()
            link = self.session.post(url=url, data=vpn_data, cookies=cookies, headers=headers, verify=False)
        except Exception as e:
            raise Exception('连接失败:{}'.format(e))
            return True
        TEXT = link.text
        if TEXT.find('There are already other user sessions in progress') != -1 or TEXT.find('已经有其它用户会话正在进行中') != -1:
            return True
        else:
            try:
                self.session.post(url=login_out_url, data=vpn_data, cookies=cookies, headers=headers, verify=False)
                self.session.close()
            except Exception as e:
                raise Exception('账户使用测试还原失败:{}'.format(e))
            return False

    def force_logout(self, username, password):
        url = "https://vpn.just.edu.cn/dana-na/auth/url_default/login.cgi"
        login_out_url = 'https://vpn.just.edu.cn/dana-na/auth/logout.cgi'
        vpn_data = {
            'tz_offset': '480',
            'username': username,
            'password': password,
            'realm': 'LDAP-REALM',
            'btnSubmit': '登录'
        }
        self.session.close()
        response = self.session.post(url=url, data=vpn_data, cookies=cookies, headers=headers, verify=False)
        DSIDFormDataStr = \
            re.findall(r'<input id="DSIDFormDataStr" type="hidden" name="FormDataStr" value="(.*?)">',
                       response.text)[0]
        self.session.post(url=url, data={
            'btnContinue': '继续会话',
            'FormDataStr': DSIDFormDataStr
        })
        self.session.post(url=login_out_url, data=vpn_data, cookies=cookies, headers=headers, verify=False)
        self.session.close()

    def get_can_use_account(self):
        username = ''
        password = ''
        # 如果都处于使用状态，随机抽取一个账户强制登出
        i = 0
        ran = random.randint(0, len(self.account_list))
        for username, password in self.account_list.items():
            if i == ran:
                return username, password
            i = i + 1

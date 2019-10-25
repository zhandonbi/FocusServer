# coding=UTF-8
from bs4 import BeautifulSoup
from VPN.vpnAccountManage import VpnAccountGet as VAG
import requests
import re

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


class StudentMessageCenter():
    def __init__(self, username='', password=''):
        self.headers = headers
        self.session = requests.session()
        self.cookies = cookies
        self.username = username
        self.password = password
        self.vpnpassword = ''

    def setAccount(self, username, password):
        self.username = username
        self.password = password
        self.vpnpassword = ''

    def login_vpn(self):
        url = "https://vpn.just.edu.cn/dana-na/auth/url_default/login.cgi"
        VA = VAG()
        v_username, v_password = VA.get_can_use_account()
        VPNdata = {
            'tz_offset': '480',
            'username': v_username,
            'password': v_password,
            'realm': 'LDAP-REALM',
            'btnSubmit': '登录'
        }
        VPNcookies = {
            'lastRealm': 'LDAP-REALM',
            'DSSIGNIN': 'url_default',
            'WWHTJIKTLSN_Impl': 'javascript',
            'DSLastAccess': '1510459958'

        }
        requests.packages.urllib3.disable_warnings()
        self.session.post(url=url, data=VPNdata, cookies=VPNcookies, headers=self.headers, verify=False)
        try:
            requests.packages.urllib3.disable_warnings()
            response = self.session.post(url=url, data=VPNdata, headers=headers, verify=False)
            if response.text.find('DSIDFormDataStr') != -1:  # 已登录
                DSIDFormDataStr = \
                    re.findall(r'<input id="DSIDFormDataStr" type="hidden" name="FormDataStr" value="(.*?)">',
                               response.text)[0]
                self.session.post(url=url, data={
                    'btnContinue': '继续会话',
                    'FormDataStr': DSIDFormDataStr
                })
                print("已登录")
            else:
                print("未登录")
            html = self.session.get('https://vpn.just.edu.cn/dana/home/index.cgi', verify=False)
            if html.text.find('江苏科技大学VPN服务') != -1:  # 登录失败
                raise Exception('校园vpn连接失败')
                return False, '登录失败,校园vpn连接失败,请稍后再试'
            self.session.post('https://vpn.just.edu.cn/jsxsd/xk/,DanaInfo=jwgl.just.edu.cn,Port=8080+LoginToXk',
                              headers=headers, data={'USERNAME': self.username, 'PASSWORD': self.password},
                              verify=False)
        except Exception as e:
            raise Exception("【】未知异常】:{}".format(e))
            return False, '登陆失败，请检查账号密码是否正确'
        return True, 'SUCCESS'

    # 获取登录者姓名
    def find_userInfo(self):
        text = ''
        try:
            html = self.session.get('https://vpn.just.edu.cn/jsxsd/kscj/,DanaInfo=jwgl.just.edu.cn,Port=8080+cjcx_list',
                                    headers=self.headers, verify=False).text
            BS = BeautifulSoup(html, 'lxml')
            text = BS.find('div', attrs={'id': 'Top1_divLoginName'}).text
            text = text[0:text.rfind('(', 1)]
        except Exception as e:
            raise Exception("获取失败")
        return text

    # 获取课表
    def get_schedule(self, school_year):
        try:
            response = self.session.post(
                'https://vpn.just.edu.cn/jsxsd/xskb/,DanaInfo=jwgl.just.edu.cn,Port=8080+xskb_list.do',
                headers=self.headers, verify=False, data={'xnxq01id': school_year})
            html = response.text
        except Exception as e:
            raise Exception("获取失败")
        class_list = ''
        bs = BeautifulSoup(html, 'lxml')
        table = bs.find('table', attrs={'id': 'kbtable'})
        class_message = table.find_all('div', attrs={'class': 'kbcontent'})
        class_tip = table.find('td', attrs={'align': 'left', 'colspan': '7'}).text
        for item in class_message:
            class_list = class_list + str(item)
        return class_list, str(class_tip)



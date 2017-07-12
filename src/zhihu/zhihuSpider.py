# -*- coding=utf-8 -*-
import requests
import re
import time
import http.cookiejar
from PIL import Image

class zhihuSpider(object):
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'}
        self.datas = {
            '_xsrf': '',
            'password': '',
            'captcha': '',
            'phone_num': ''
            }
        self.session = requests.Session()
        self.session.headers = self.headers
        self.session.cookies = http.cookiejar.LWPCookieJar('cookies')
        try:
            self.session.cookies.load('cookies', ignore_discard=True)
        except:
            print('cookies 不能加载')

    # 获取xsrf
    def get_xsrf(self):
        login_url = 'https://www.zhihu.com/' # 登录界面URL
        res = self.session.get(login_url)
        pattern = re.compile('<input type="hidden" name="_xsrf" value="(.*?)"/>')
        p = pattern.findall(res.text)
        self.datas['_xsrf'] = p[0]

    # 获取验证码
    def get_captcha(self):
        t = str(int(time.time() * 1000))
        captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
        # 获取验证码，并将验证码写入captcha.gif
        captcha = self.session.get(captcha_url)
        with open('captcha.gif', 'wb') as f:
            f.write(captcha.content)
        f.close()
        # 显示验证码
        im = Image.open('captcha.gif')
        im.show()
        im.close()
        # 手动输入验证码
        login_captcha = input('input captcha:\n')
        self.datas['captcha'] = login_captcha

    def already_login(self):
        url = 'https://www.zhihu.com/settings/profile'
        login_code = self.session.get(url, allow_redirects=False).status_code
        if login_code == 200:
            return True
        else:
            return False

    def login(self, account, password):
        post_url = 'https://www.zhihu.com/login/phone_num' # post请求提交的URL
        # 获取xsrf
        self.get_xsrf()
        # 获取验证码
        self.get_captcha()
        self.datas['phone_num'] = account
        self.datas['password'] = password
        # 提交post请求，并且打印出json
        result = self.session.post(post_url, data=self.datas)
        print(result.text)
        # 保存cookies
        self.session.cookies.save(ignore_discard=True, ignore_expires=True)

if __name__ == "__main__":
    spider = zhihuSpider()
    if spider.already_login():
        print('用户已经登录')
    else:
        account = input('请输入用户名 \n> ')
        password = input('请输入密码 \n> ')
        spider.login(account, password)

# -*- coding=utf-8 -*-
import requests
import re
import http.cookiejar

class PixivSpider(object):
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'}
        self.session.headers = self.headers
        self.session.cookies = http.cookiejar.LWPCookieJar(filename='cookies')
        try:
            # 加载cookie
            self.session.cookies.load(filename='cookies', ignore_discard=True)
        except:
            print('cookies不能加载')

        self.params ={
            'lang': 'en',
            'source': 'pc',
            'view_type': 'page',
            'ref': 'wwwtop_accounts_index'
        }
        self.datas = {
            'pixiv_id': '',
            'password': '',
            'captcha': '',
            'g_reaptcha_response': '',
            'post_key': '',
            'source': 'pc',
            'ref': 'wwwtop_accounts_indes',
            'return_to': 'https://www.pixiv.net/'
            }

    def get_postkey(self):
        login_url = 'https://accounts.pixiv.net/login' # 登陆的URL
        # 获取登录页面
        res = self.session.get(login_url, params=self.params)
        # 获取post_key
        pattern = re.compile(r'name="post_key" value="(.*?)">')
        r = pattern.findall(res.text)
        self.datas['post_key'] = r[0]

    def already_login(self):
        # 请求用户配置界面，来判断是否登录
        url = 'https://www.pixiv.net/setting_user.php'
        login_code = self.session.get(url, allow_redirects=False).status_code
        if login_code == 200:
            return True
        else:
            return False

    def login(self, account, password):
        post_url = 'https://accounts.pixiv.net/api/login?lang=en' # 提交POST请求的URL
        # 设置postkey
        self.get_postkey()
        self.datas['pixiv_id'] = account
        self.datas['password'] = password
        # 发送post请求模拟登录
        result = self.session.post(post_url, data=self.datas)
        print(result.json())
        # 储存cookies
        self.session.cookies.save(ignore_discard=True, ignore_expires=True)

if __name__ == "__main__":
    spider = PixivSpider()
    if spider.already_login():
        print('用户已经登录')
    else:
        account = input('请输入用户名\n> ')
        password = input('请输入密码\n> ')
        spider.login(account, password)

# -*- coding=utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pickle
import re

# 用户名
username = input('请输入用户名\n > ')
try:
    re.match(r'^((?!@163).)*$', username).group()
except:
    username = re.sub('@163.com$','',username)
# 密码
password = input('请输入密码\n > ')

browser = webdriver.Chrome()
# 最大化窗口
browser.maximize_window()
browser.get('http://mail.163.com/')
time.sleep(2)

# 切换到登录表单
browser.switch_to.frame("x-URS-iframe")
# 填写用户名
browser.find_element_by_name("email").send_keys(username)
# 填写密码
browser.find_element_by_name("password").send_keys(password)
# 选中10天后免录
browser.find_element_by_id('un-login').send_keys(Keys.SPACE)
browser.find_element_by_id("dologin").click()

#获取cookie
cookies = browser.get_cookies()
#保存cookie到本地
with open('cookie.txt','wb') as f:
    pickle.dump(cookies,f)
f.close()

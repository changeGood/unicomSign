# coding=utf-8
# author: pbbqdd
# modify: wfion
import http.cookiejar
import json
import os
import time
import urllib.request as urllib2


class Qiandao():

    def __init__(self):
        self.timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.cookie = http.cookiejar.CookieJar()
        self.handler = urllib2.HTTPCookieProcessor(self.cookie)
        opener = urllib2.build_opener(self.handler)
        urllib2.install_opener(opener)

    def sign(self, url_add, user_phone):
        req2 = urllib2.Request("http://m.client.10010.com/mobileService/login.htm",
                               url_add.encode('utf-8') + self.timestamp.encode('utf-8'))
        if urllib2.urlopen(req2).getcode() == 200:
            print('login success!')
        try:
            for item1 in self.cookie:
                if item1.name == 'a_token':
                    a = item1.value
        except:
            print("cant get cookies")
        req3 = urllib2.Request("https://act.10010.com/SigninApp/signin/querySigninActivity.htm?token=" + a)
        if urllib2.urlopen(req3).getcode() == 200:
            print('querySigninActivity success!')
        req4 = urllib2.Request("https://act.10010.com/SigninApp/signin/daySign.do", "btnPouplePost".encode('utf-8'))
        if urllib2.urlopen(req4).getcode() == 200:
            print('daySign success!')
        req5 = urllib2.Request("https://act.10010.com/SigninApp/signin/goldTotal.do")
        print('phone: ' + user_phone + ' coin: ' + urllib2.urlopen(req5).read().decode('utf-8'))


if __name__ == '__main__':
    path = os.path.dirname(os.path.abspath(__file__))
    try:
        with open(path + '/config_unicom.json', 'r', encoding='utf-8') as f:
            dict_config = json.loads(f.read())
        try:
            account_list = dict_config['accounts']
        except KeyError as e:
            print('当前路径' + path + ' 配置文件错误，请检查config_unicom.json', e)
        i = 0
        datalist = []

        for item in account_list:
            i += 1
            try:
                phone = item['phone']
                url = item['url']
            except KeyError as e:
                print('第%d个账户实例配置出错，跳过该账户' % i, e)
                continue

            user = Qiandao()
            user.sign(url, phone)

    except ValueError as e:
        print('出错了', e)
    except FileNotFoundError as e:
        print('当前路径' + path + ' 未找到config_unicom.json配置文件', e)
    except json.JSONDecodeError as e:
        print('config_unicom.json格式有误', e)

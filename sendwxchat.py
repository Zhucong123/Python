# -*- coding: utf-8 -*-
# @Author Cong.zhu  #

from __future__ import unicode_literals

import json
import os
import time
from threading import Timer

import requests
from wxpy import *

#

# linux执行登陆请调用下面的这句
# bot = Bot(console_qr=2,cache_path="botoo.pkl")

# 获取One(一个)的每一天的句子和图片
class SendWx:
    
    def __init__(self):
        self.bot = Bot()
        self.content = ''
        self.imgurl = ''
        self.nowdate = time.strftime('%Y-%m-%d')

    #获取One每天返回的第一条数据
    def GetToken(self):
        print("**********************************")
        url = "http://m.wufazhuce.com/one"
        data = requests.get(url)

        _token = data.text.split("One.token = '")[1].split("'")[0]
        #先要得到cookies，然后请求的时候带进去，不然请求异常
        cookie = data.cookies["PHPSESSID"]
        headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36',
            'Cookie': 'PHPSESSID='+cookie
        }
        responsestr = requests.get(
            url+"/ajaxlist/0?_token="+_token, headers=headers)
        jsonstr = responsestr.text.encode('utf-8').decode('unicode_escape')
        jsonstr = jsonstr.replace('\\', '').replace('\r\n', '')
        # print(json.loads(jsonstr)["data"][0])#jsonstr.replace('\/','').
        onecontent = json.loads(jsonstr)["data"][0]
        self.content = onecontent['content']
        self.imgurl = onecontent['img_url']
    #下载图片到本地
    def downimage(self):
        if not os.path.exists('E:/Image/'):
            print("cces")
            os.makedirs('E:/Image/')
        try:
            print(self.imgurl)
            response=requests.get(self.imgurl)
            print(response.status_code)
            if response.status_code==200:
                file_path='E:/Image/{0}.{1}'.format(self.nowdate,'jpg')
                if not os.path.exists(file_path):
                    with open(file_path,'wb') as f:
                        f.write(response.content)
        except:
            print('失败')

    def send_news(self):
        try:
            contents=self.content
            # 你朋友的微信名称，不是备注，也不是微信帐号。
            my_friend=self.bot.friends().search(u'混得最水的武汉人。')[0]
            my_friend.send(contents)
            my_friend.send_image('E:/Image/{0}.jpg'.format(self.nowdate))
            my_friend.send(u"--来自 One·一个 摘取")
            print(self.nowdate+"发送成功")
            # 每86400秒（1天），发送1次
            #t=Timer(86400, self.send_news)
            t=Timer(60,self.send_news)
            t.start()
        except:
            # 你的微信名称，不是微信帐号。
            my_friend=self.bot.friends().search('混得最水的武汉人。')[0]
            my_friend.send(u"今天消息发送失败了")


if __name__ == "__main__":
    SendWx=SendWx()
    SendWx.GetToken()
    SendWx.downimage()
    SendWx.send_news()
    # send_news()

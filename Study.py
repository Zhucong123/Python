#!/usr/local/bin/python3
# coding=utf-8

import requests
import json
import smtplib
import jinja2
import os.path as pth
import time
from email.mime.text import MIMEText
from email.header import Header

HEFEN_D = pth.abspath(pth.dirname(__file__))
LOCATION = '杭州'
ORIGINAL_URL = 'https://free-api.heweather.com/s6/weather?parameters'
TO = ['291396486@qq.com']


def sendEmail(content, title, from_name, from_address, to_address, serverport, serverip, username, password):
    msg = MIMEText(content, _subtype='html', _charset='utf-8')
    msg['Subject'] = Header(title, 'utf-8')
    # 这里的to_address只用于显示，必须是一个string
    msg['To'] = ','.join(to_address)
    msg['From'] = from_name
    try:
        s = smtplib.SMTP_SSL(serverip, serverport)
        s.login(username, password)
        # 这里的to_address是真正需要发送的到的mail邮箱地址需要的是一个list
        s.sendmail(from_address, to_address, msg.as_string())
        s.quit()
        print('%s----发送邮件成功' %
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    except Exception as err:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(err)


def get_data():
    Alldata = {}
    new_data = []
    life_data = []
    parametres = {
        'location': LOCATION,
        'key': 'efcaae04f77a40ff94ecd9a664398465',  # 注册和风天气会给你一个KEY
        'lang': 'zh-cn',
        'unit': 'm'
    }

    try:
        response = requests.get(ORIGINAL_URL, params=parametres)
        r = json.loads(json.dumps(response.text, ensure_ascii=False, indent=1))
        r = json.loads(response.text)
    except Exception as err:
        print(err)

    weather_forecast = r['HeWeather6'][0]['daily_forecast']
    weather_lifestyle = r['HeWeather6'][0]['lifestyle']
    for data in weather_forecast:
        new_obj = {}
        # 日期
        new_obj['date'] = data['date']
        # 最高温度
        new_obj['tmp_max'] = data['tmp_max']
        # 最低温度
        new_obj['tmp_min'] = data['tmp_min']
        # 白天天气描述
        new_obj['cond_txt_d'] = data['cond_txt_d']
        # 晚上天气描述
        new_obj['cond_txt_n'] = data['cond_txt_n']
        # 白天天气状况描述
        new_obj['cond_txt_d'] = data['cond_txt_d']

        new_data.append(new_obj)
    for data in weather_lifestyle:
        liftstyle_obj = {}
        if data['type'] == 'comf':
            liftstyle_obj['comf'] = data['txt']
        if data['type'] == 'drsg':
            liftstyle_obj['drsg'] = data['txt']
        if liftstyle_obj:
            life_data.append(liftstyle_obj)

    Alldata['new_data'] = new_data
    Alldata['life_data'] = life_data
    return json.dumps(Alldata, ensure_ascii=False)


def render_mail(new_data, life_data):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(HEFEN_D)
    )
    return env.get_template('hefentianqi.html').render({'new_data': new_data, 'life_data': life_data})


def main():
    config = {
        "from": "1902726060@qq.com",
        "from_name": '来自爸爸的爱',
        "to": TO,
        "serverip": "smtp.qq.com",
        "serverport": "465",
        "username": "1902726060@qq.com",
        "password": "ybiiqxzcpowydeec"  # QQ邮箱的SMTP授权码
    }

    title = ".."

    data = get_data()
    print(data)
    body = render_mail(json.loads(
        data)['new_data'], json.loads(data)['life_data'])
    sendEmail(body, title, config['from_name'], config['from'], config['to'], config[
              'serverport'], config['serverip'], config['username'], config['password'])


main()

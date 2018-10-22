# -*- coding: utf-8 -*-
# @Author Cong.zhu  #

import requests
from bs4 import BeautifulSoup
import re
import redis
import json
class Music163:

    def __init__(self):
        self.r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
        self.headers = {
            "Referer":
            "https://music.163.com/",
            "Host":
            "music.163.com",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        }
    #下载歌单页面
    def DownLoadHtml(self,url):
        urls = "https://music.163.com/playlist?id=2318367080"
        music_html = requests.get(urls, headers=self.headers)
        soup = BeautifulSoup(music_html.text, "lxml")
        return soup
    #获取歌单里面歌曲列表
    def get_music_list(self,html):
        #keyid=html.find("div",class_="n-cmt").get("data-tid")
        mm = html.find("ul",class_='f-hide').find_all("li")
        gedanname = html.find_all("link")[0].get('href')
        self.r.hset("歌单",html.title.get_text(),gedanname)
        for li in mm:
            #print(li.find("a").get_text())
            #self.r.hmset(li.find("a").get_text(),{'name':li.find("a").get_text(),'id':li.find("a").get('href')})
            self.r.hset(html.title.get_text(),li.find("a").get_text(),li.find("a").get('href'))

    #获取评论JSON数据
    def GetComments(self,songid):
        url='http://music.163.com/api/v1/resource/comments/R_SO_4_%s'%songid
        commentsjoin=requests.get(url,headers=self.headers)
        return commentsjoin.json() #[1]["content"]
    
    #获取热门评论
    def Get_HotComments(self,data,songname):
        for ent in data["hotComments"]:
            print(ent["content"])
            self.writefile(songname,ent["content"])
        
    #写入文本数据
    def writefile(self,filename,content):
        filename=self.validateTitle(filename)
        path='E:\网易云音乐歌曲评论\%s.txt'%filename
        with open(path,'a+',encoding='utf-8') as fileobject: #使用‘w’来提醒python用写入的方式打开
            fileobject.writelines(content+"\n")

    def RedisHelp(self):
        return self.r.hgetall("歌单")

    def validateTitle(self,title):
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_title = re.sub(rstr, "_", title)  # 替换为下划线
        return new_title

if __name__ == "__main__":
    music=Music163()
    # url=""
    # html=music.DownLoadHtml(url)
    # music.get_music_list(html)
    #jsss=music.GetComments('516997458')
    #music.Get_HotComments(jsss)
    for key in music.RedisHelp():
        print("*****************************************\n")
        for kv in (music.r.hgetall(key).items()):
            songname=kv[0]
            songid=kv[1].split("=")[1]
            data=music.GetComments(songid)
            music.Get_HotComments(data,songname)

            
            
   
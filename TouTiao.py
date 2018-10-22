import os  #Python系统编程模块 ，可以处理文件和目录

import re  #正则表达式模块

from multiprocessing.pool import Pool  #多进程管理包，pool类可以提供指定数量的进程供用户调用

import requests #Python HTTP客户端库 请求网络

from urllib.parse import urlencode #将字段转换为url的参数

from hashlib import md5 #转换md5的值

#import PySqlHelp as comm

import time
import sys
keyword = '耐克'
#请求页面，获得json格式数据
def get_page(offset):
	#定义参数
	para={
		'offset':offset,
		'format':'json',
		'keyword':keyword,
		'autoload':'true',
		'count':'20',
		'cur_tab':'1',
		'from':'search_tab',
	}

	headers={
		'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
		'referer':'https://www.toutiao.com/search/?keyword=%E8%80%90%E5%85%8B',#+urlencode(keyword),
		'accept-language':'zh-CN,zh;q=0.9,en;q=0.8'
	}
	#请求连接
	#https://www.toutiao.com/search_content/
	# ?offset=0&format=json&keyword=%E8%80%90%E5%85%8B&autoload=true&count=20&cur_tab=1&from=search_tab
	url="https://www.toutiao.com/search_content/?"+urlencode(para)
	print(url)
	try:
		#请求定义好的url
		response=requests.get(url,headers=headers)	
		#如果请求成功返回json
		if response.status_code==200:
			return response.json()
	except requests.ConnectionError:
		return None

#获取图片url
#json是请求得到的json对象
#解析json对象里面的图片url和title
def get_image(json):
	if json.get('data'):
		#print (json.get('data'))
		for dataitem in json.get('data'):
			if dataitem.get('title')==None:
				continue
			else:
				title=dataitem.get('title')
				images=dataitem.get('image_list')
				if images == None:
					continue
				else:
					for image in images:
					#yield 就是return 的返回值，并且记住返回的位置，下次返回的时候，就从当前位置的下一个位置去返回，可用于for 循环当中
						yield{
							'image':image.get('url'),
							'title':title
						}
							
				
				
						
					

#保存图片到本地
#item 是yield对象
def save_image(item):
	#查找文件夹
	if not os.path.exists('E:/Python/TouTiao/'+item.get('title')):
		try:
			nostr=validateTitle(item.get('title'))
			print(nostr)
			os.makedirs('E:/Python/TouTiao/{0}'.format(nostr))
		except OSError:
			print(item.get('title'))
	try:
		imageurl=item.get('image')
		responseimage=requests.get('http:'+imageurl)
		if responseimage.status_code==200:
			file_path='E:/Python/TouTiao/{0}/{1}.{2}'.format(validateTitle(item.get('title')),md5(responseimage.content).hexdigest(),'jpg')
			if not os.path.exists(file_path):
				with open(file_path,'wb') as f:
					f.write(responseimage.content)
					#comm.InsertTouTiao('INSERT TouTiao VALUES ('"'{0}'"','"'{1}'"','"'{2}'"','"'{3}'"')'.format(validateTitle(item.get('title')),item.get('image'), time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),keyword))
			else:
				print('Already Downloaded',file_path)
	except requests.ConnectionError:
		print('Failed to Save Image')


#替换字符串里面的反斜杠
def replaceAll(old,new,str):
	while str.find(old)>-1:
		str=str.replace(old,new)
	return str

#去除文件名当中不能包含的字符串
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title


#主函数
def main(offset):
	json=get_page(offset)
	for item in get_image(json):
		#print(item)
		save_image(item)

GROUP_START = 1
GROUP_END = 20



if __name__=='__main__':
	#实例化进程类
	# pool=Pool()
	# #groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
	# groups=('0')

	# pool.map(main,groups)
	# pool.close()
	# pool.join()
	main(0)


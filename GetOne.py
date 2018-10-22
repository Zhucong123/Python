import requests
import json

def GetToken():
    print("**********************************")
    url="http://m.wufazhuce.com/one"
    data=requests.get(url)
    #print (data.text.split("One.token = '")[1].split("'")[0])
    _token=data.text.split("One.token = '")[1].split("'")[0]
    #print(data.cookies["PHPSESSID"])
    #http://m.wufazhuce.com/one/ajaxlist/0?_token=6128122e011b8f8ee850da5c9acc4b4bbb7b3b3e
    cookie=data.cookies["PHPSESSID"]
    headers={
        'user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36',
        'Cookie':'PHPSESSID='+cookie
    }
    responsestr=requests.get(url+"/ajaxlist/0?_token="+_token,headers=headers)
    jsonstr=responsestr.text.encode('utf-8').decode('unicode_escape')
    jsonstr=jsonstr.replace('\\','').replace('\r\n', '')
    #print(json.loads(jsonstr)["data"][0])#jsonstr.replace('\/','').
    return json.loads(jsonstr)["data"][0]

#One.token


if __name__ == "__main__":
    GetToken()
    


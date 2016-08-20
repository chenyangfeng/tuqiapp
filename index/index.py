#!/usr/bin/env python
#-*- coding:utf-8 -*-
from bae.core.wsgi import WSGIApplication
import hashlib
import web
import lxml
import time
import requests
import os
import urllib2
import json
import urllib
from lxml import etree
import cookielib
import re
import random
import sys
import traceback
from qiniu import Auth
from qiniu import BucketManager

web.config.debug = True

urls = ( 
    '/', 'Index'
)
class Index:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        #获取输入参数
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr = data.echostr
        #自己的token
        token="tuqi" #这里改写你在微信公众平台里输入的token
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        #sha1加密算法

        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr

    def POST(self):
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        #content=xml.find("Content").text#获得用户所输入的内容
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        #picurl = xml.find('PicUrl').text
        #return self.render.reply_text(fromUser,toUser,int(time.time()), content)
        if msgType == 'image':#判断接受的微信消息是不是图片
            try:
                picurl = xml.find('PicUrl').text#从微信反馈XML数据包里面获取图片网址
                access_key = "kZOOkjCVeikohNP85sSPLJeX1FM49dVz0kPaVbzc"
                secret_key = "1zCp0e7X4SJGGKOv9r4jaPwfv5YN-_ZxjJOVzA5w"
                bucket_name = 'danpic'
                q = Auth(access_key, secret_key)
				
                bucket = BucketManager(q)

                key = fromUser[-4:]+ '/' + picurl[80:88]+'.jpg'#文件名重命名
                cont = requests.get(picurl).content
                if sys.getsizeof(cont)>102400:
                    ret, info = bucket.fetch(picurl, bucket_name, key)
                    return self.render.reply_text(fromUser, toUser, int(time.time()), '上传成功'+'（客户码'+ fromUser[-4:]+'）')
		    		#给客户发送消息 上传成功
                else:
                    return self.render.reply_text(fromUser,toUser, int(time.time()), '【上传失败 ，图片像素过低】  请确认上传的是原图。（想知道怎么上传原图？回复“原图”')
            except:
                for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
                    s += "%-23s:%s '%s' in %s()" % (filename, linenum, source, funcname)
                return self.render.reply_text(fromUser, toUser, int(time.time()), s)
                return self.render.reply_text(fromUser, toUser, int(time.time()),  '识别失败，换张图片试试吧')
        else:
            content = xml.find("Content").text  # 获得用户所输入的内容
            if content[0:2] == u"快递":
                danhao = str(content[2:])
                try:
					data = {}
					data["appkey"] = "df3e25009c85cf92"
					data["type"] = "auto"
					data["number"] = danhao
					#data["number"] = "3929900405482"
					url_values = urllib.urlencode(data)
					url = "http://api.jisuapi.com/express/query" + "?" + url_values
					request = urllib2.Request(url, url_values)
					result = urllib2.urlopen(request)
					jsonarr = json.loads(result.read())
					result = jsonarr["result"]
					for val in result["list"]:
					    kuaidi = val["time"]+val["status"]
					    return self.render.reply_text(fromUser, toUser, int(time.time()),  '物流信息'+kuaidi)
                except:
                    return self.render.reply_text(fromUser, toUser, int(time.time()),  '暂时查不到相关信息')

            else:
                if content[0:2] == u"原图":
			
                    #post = str(content[2:])
                    return self.render.reply_text(fromUser,toUser,int(time.time()), '【1】选择一张或者多张图片~~【2】点击右下角的 ”预览“~ 【3】在图片预览窗口选中”原图“~~~ 【 温馨提醒 】上传原图能极大提高冲印质量，但可能会耗费较多手机流量，最好在wifi下给我们发图片')

                else:
                    return self.render.reply_text(fromUser,toUser,int(time.time()), '本公众号仅接受图片。')

				
if __name__ == "__main__": 
    app.run()	

app = web.application(urls, globals()).wsgifunc()

from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)

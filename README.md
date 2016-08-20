# tuqiapp
功能：公众号接受用户照片后上传至七牛云，并为每个用户创建一个文件夹。

使用方法：

注册微信公众号并启用开发者模式

注册BAE 选择Python 2.7版本 

注册七牛云存储 获得AK 与SK  

将七牛AK与SK 以及空间名 写入index.py

                picurl = xml.find('PicUrl').text#从微信反馈XML数据包里面获取图片网址
                access_key = "********"
                secret_key = "********"
                bucket_name = '****'
                q = Auth(access_key, secret_key)

将微信token写入index.py以通过微信开发验证。

        #自己的token
        token="tuqi" #这里改写你在微信公众平台里输入的token
        #字典序排序
其他：若用户发送图片质量过差 会给用户返回消息提示其注意上传原图。

                if sys.getsizeof(cont)>52400:#限制低于500K图片不能上传
                    ret, info = bucket.fetch(picurl, bucket_name, key)
                    return self.render.reply_text(fromUser, toUser, int(time.time()), '上传成功'+'（客户码'+ fromUser[-4:]+'）')
    	    		#给客户发送消息 上传成功
                else:
                    return self.render.reply_text(fromUser,toUser, int(time.time()), '【上传失败 ，图片像素过低】  请确认上传的是原图。



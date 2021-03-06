#!/usr/bin/env python 
# -*- coding:utf-8 -*-
#需求：解析下载图片数据 http://pic.netbian.com/4kmeinv/
import requests
from lxml import etree
import os
if __name__ == "__main__":
    url = 'http://pic.netbian.com/4kmeinv/'
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    response = requests.get(url=url,headers=headers)
    #手动设定响应数据的编码格式
    # response.encoding = 'utf-8'
    #给响应数据设置'utf-8'乱码现象仍然存在
    page_text = response.text

    #数据解析：src的属性值  alt属性
    tree = etree.HTML(page_text)
    li_list = tree.xpath('//div[@class="slist"]/ul/li')


    #创建一个文件夹
    if not os.path.exists('./picLibs'):
        os.mkdir('./picLibs')

    for li in li_list:
        img_src = 'http://pic.netbian.com'+li.xpath('./a/img/@src')[0]
        #作局部解析的时候，相对的内容一定要带一个'.'，列表之中只有一个元素
        img_name = li.xpath('./a/img/@alt')[0]+'.jpg'
        #通用处理中文乱码的解决方案
        print('img_src = ')
        print(img_src)
        print('img_name = ')
        print(img_name)
        img_name = img_name.encode('iso-8859-1').decode('gbk')
        #这里输入的img_name会出现乱码，
        #通用处理中文乱码的解决方法1.使用img_name.encode().decode...
        #2.在上面拿到数据之后使用response.encoding = 'utf-8'

        # print(img_name,img_src)
        #请求图片进行持久化存储
        img_data = requests.get(url=img_src,headers=headers).content
        #响应得到的是对应的二进制数据，使用.content获得对应的内容
        img_path = 'picLibs/'+img_name
        with open(img_path,'wb') as fp:
            fp.write(img_data)
            print(img_name,'下载成功！！！')

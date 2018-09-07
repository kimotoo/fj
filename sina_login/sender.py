#encoding:utf-8

import requests
import json
import re
import urllib
import base64
import rsa
import binascii
import time
import math
import random
import cv2
import numpy as np


# 获取mid
def get_mid(url,session):

    print("正在获取mid...")
    resp = session.get(url)
    print(resp.content)
    list = re.findall(r'mid=\d+', resp.content.decode('utf-8'))
    return (list[-1].split('='))[-1]


# 转发
def repost(session, mid, url, str_list):

    # 获取domain用于refer及请求url
    print("正在转发...")
    s1 = re.findall(r'page_\d+',url)
    str = s1[0].split("_")
    domain = re.findall(r'\d\d\d\d\d\d', str[1])[0]

    # 请求post url
    req_url = "https://weibo.com/aj/v6/mblog/forward?ajwvr=6&domain=%s&__rnd=%d" % (domain, time.time())

    post_data = {
        "pic_src": "",
        "pic_id": "",
        "appkey": "",
        "style_type": 2, # 定值
        "mark": "",
        "mid": mid,   #必需
        "reason": "test",  #必需
        "location": "page_%s_single_weibo" % domain,   #必需
        "pdetail": str[1],    #必需
        "module": "",
        "page_module_id": "",
        "refer_sort": "",
        "rank": 0, # 定值
        "rankid": "",
        "isReEdit": "",
        "_t": 0 # 定值
    }

    session.headers['Referer'] = url
    resp = session.post(req_url, data=post_data)

    pa = r'"code":"(.*?)"'
    code = re.findall(pa, resp.text, re.S)[0]

    return code





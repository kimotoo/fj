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

import login
import sender
import pickle
from keras.models import load_model
import time
import re

MODEL_FILENAME = "captcha_model.hdf5"
MODEL_LABELS_FILENAME = "model_labels.dat"
com_url = "https://weibo.com/aj/v6/comment/add?ajwvr=6&__rnd=1536468318371"


def get_mid(url,session):

    print("正在获取mid...")
    resp = session.get(url)
    print(resp.content)
    list = re.findall(r'mid=\d+', resp.content.decode('utf-8'))
    return (list[-1].split('='))[-1]


if __name__ == '__main__':

    url = "https://weibo.com/6632894984/GyxpGgGcF?from=page_1005056632894984_profile&wvr=6&mod=weibotime&type=comment"

    pde = re.findall(r'page_(.*?)_', url)[0]

    # 登录
    name1 = "425306911@qq.com"
    pw1 = "pi31415926"

    sess1 = login.get_session()

    # 启动识别模型
    with open(MODEL_LABELS_FILENAME, "rb") as f:
        lb = pickle.load(f)

    model = load_model(MODEL_FILENAME)

    # 登录
    uid = login.login_post(name1, pw1, sess1, model, lb)

    code1 = 0

    mid = get_mid(url, sess1)
    print(mid)

    data = {

        "act": "post",
        "mid": mid,  #必需
        "uid": uid,  #必需
        "content": "test",
        "location": "page_100505_single_weibo",
        "module": "bcommlist",
        "pdetail": pde,
        "_t": 0,
    }

    sess1.headers['Referer'] = url

    req = sess1.post(com_url, data=data)
    print(req.text)








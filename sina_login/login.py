#encoding:utf-8

import requests
import json
import re
import urllib
import base64

import rsa
import binascii
import math
import random
import cv2
import numpy as np
import captcha_model


# 初始post
post_data = {
    'entry': 'weibo',
    'gateway': '1',
    'from': '',
    'savestate': '7',
    'useticket': '1',
    'pagerefer': "http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl",
    'vsnf': '1',
    'service': 'miniblog',
    'pwencode': 'rsa2',
    'sr': '1366*768',
    'encoding': 'UTF-8',
    'prelt': '115',
    'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
    'returntype': 'META'
}

content_text = [""]

# 登陆入口url
login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'


def get_session():
    sess = requests.session()
    sess.headers['User-Agent'] = (
      'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) '
      'Chrome/20.0.1132.57 Safari/536.11'
)
    return sess


# 获取经base64编码的用户名
def encode_name(username):

    username_urllike = urllib.request.quote(username)
    username_encrypted = base64.b64encode(bytes(username_urllike, encoding='utf-8'))
    return username_encrypted.decode('utf-8')


# 获取预登陆返回的信息
def get_prelogin_info(prelogin_url, session):
    json_pattern = r'.*?\((.*)\)'
    repose_str = session.get(prelogin_url).text
    m = re.match(json_pattern, repose_str)
    return json.loads(m.group(1))


# 获取加密后的密码
def encrypted_pw(password, data):
    rsa_e = 65537  # 0x10001
    pw_string = str(data['servertime']) + '\t' + str(data['nonce']) + '\n' + str(password)
    key = rsa.PublicKey(int(data['pubkey'], 16), rsa_e)
    pw_encypted = rsa.encrypt(pw_string.encode('utf-8'), key)
    password = ''
    passwd = binascii.b2a_hex(pw_encypted)
    return passwd

# 获取验证码url
def get_pincode_url(pcid):
    size = 0
    url = "http://login.sina.com.cn/cgi/pin.php"
    pincode_url = '{}?r={}&s={}&p={}'.format(url, math.floor(random.random() * 100000000), size, pcid)
    return pincode_url


# 获取验证码图片 pcid_url = "http://login.sina.com.cn/cgi/pin.php?r=40222527&s=0&p=1"
def get_pcid_image(pcid_url):

    resp = requests.get(pcid_url, stream=True)
    image = np.asarray(bytearray(resp.content), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    return image


# 登陆并获取重定向session
def login_post(uname, pwrod, session, model, lb):

    #uname = js['uname']
    #pwrod = js['pwrod']

    print("%s正在登陆..."%uname)
    su = encode_name(uname)

    prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&' \
                   'su=' + su + '&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)'

    while(True):

        pre_obj = get_prelogin_info(prelogin_url, session)
        sp = encrypted_pw(pwrod, pre_obj)
        print(pre_obj)

        post_data['su']=su
        post_data['servertime'] = pre_obj['servertime']
        post_data['nonce'] = pre_obj['nonce']
        post_data['rsakv'] = pre_obj['rsakv']
        post_data['sp'] = sp


        print(pre_obj)

        if ('showpin' in pre_obj ):

            if(pre_obj['showpin'] == 1):

                pcid = pre_obj['pcid']
                img_url = get_pincode_url(pcid)
                image = get_pcid_image(img_url)

                # 验证码识别
                cap = captcha_model.cap_model(image, model, lb)

                post_data['pcid'] = pcid
                post_data['door'] = cap

        login_page = session.post(login_url, data=post_data)
        login_loop = (login_page.content.decode("GBK"))
        pa = r'location\.replace\([\'"](.*?)[\'"]\)'
        loop_url = re.findall(pa, login_loop)[0]

        pa_1 = r'retcode=(.*?)&'
        retcode = re.findall(pa_1, loop_url)

        if (len(retcode) == 0):
            login_index = session.get(loop_url)
            uuid_pa = r'"uniqueid":"(.*?)"'
            uid = re.findall(uuid_pa, login_index.text, re.S)[0]
            print(login_index.text)
            print("%s登陆成功" % uid)

            return session

        else:

            print(retcode)

            if (retcode[0] == 101):
                print("%s 密码错误" % uname)

                break

            else:
                print("验证码错误")
                #js['other'] = False







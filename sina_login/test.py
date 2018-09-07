#encoding:utf-8

import login
import sender
import pickle
from keras.models import load_model
import time
import re


MODEL_FILENAME = "captcha_model.hdf5"
MODEL_LABELS_FILENAME = "model_labels.dat"

str_last = ""

if __name__ == '__main__':

    url = "https://weibo.com/5473085545/Gqn21cJwJ?from=page_1005055473085545_profile&wvr=6&mod=weibotime&type=comment#_rnd1531839476120"

    name1 = "15899726233"
    pw1 = "Ifwpo0105"

    sess1 = login.get_session()


    # 启动识别模型
    with open(MODEL_LABELS_FILENAME, "rb") as f:
        lb = pickle.load(f)

    model = load_model(MODEL_FILENAME)

    # 登录
    login.login_post(name1,pw1, sess1, model, lb)

    code1 = 0

    mid1 = sender.get_mid(url, sess1)

    while(code1 != 100001):

        print("正在转发...")
        s1 = re.findall(r'page_\d+', url)
        str = s1[0].split("_")
        domain = re.findall(r'\d\d\d\d\d\d', str[1])[0]

        # 请求post url
        req_url = "https://weibo.com/aj/v6/mblog/forward?ajwvr=6&domain=%s&__rnd=%d" % (domain, time.time())

        post_data = {
            "pic_src": "",
            "pic_id": "",
            "appkey": "",
            "style_type": 2,  # 定值
            "mark": "",
            "mid": mid1,  # 必需
            "reason": "test",  # 必需
            "location": "page_%s_single_weibo" % domain,  # 必需
            "pdetail": str[1],  # 必需
            "module": "",
            "page_module_id": "",
            "refer_sort": "",
            "rank": 0,  # 定值
            "rankid": "",
            "isReEdit": "",
            "_t": 0  # 定值
        }

        sess1.headers['Referer'] = url
        resp = sess1.post(req_url, data=post_data)

        pa = r'"code":"(.*?)"'
        code1 = int(re.findall(pa, resp.text, re.S)[0])

        str_last = resp.text

        print("转发成功")
        time.sleep(300)

    with open('test.txt', 'w') as f:
        f.write(str_last)
        f.close()



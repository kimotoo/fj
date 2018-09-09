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


    url = "https://weibo.com/6632894984/GyxpGgGcF?from=page_1005056632894984_profile&wvr=6&mod=weibotime&type=comment"

    name1 = "425306911@qq.com"
    pw1 = "pi31415926"

    sess1 = login.get_session()

    # 启动识别模型
    with open(MODEL_LABELS_FILENAME, "rb") as f:
        lb = pickle.load(f)

    model = load_model(MODEL_FILENAME)

    # 登录
    uid = login.login_post(name1,pw1, sess1, model, lb)






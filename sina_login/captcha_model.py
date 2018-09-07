#encoding:utf-8
from keras.models import load_model
import numpy as np
import pickle
import image_pro, md

MODEL_FILENAME = "captcha_model.hdf5"
MODEL_LABELS_FILENAME = "model_labels.dat"

map = {'0':'2', '1':'3', '2':'4', '3':'5', '4':'6', '5':'7','6':'8','7':'a', '8':'b', '9' :'c',  '10':'e',
       '11':'f', '12':'g', '13':'h', '14':'k', '15' :'m', '16':'n', '17':'p', '18':'q','19' :'r',  '20':'q',
       '21':'u', '22':'v', '23':'w', '24' :'x', '25':'y',  '26' :'z',  '27':'b', '28' :'d', '29':'e',
       '30':'f',  '31':'m', '32':'n','33':'q', '34':'w', '35':'y', '36':'h'}

# 图片输入格式为png
def cap_model(image, model, lb):

    imgs = image_pro.img_pro(image)

    if len(imgs) != 5:
        print("图像切割失败")
        return 0

    lables = []
    for img in imgs:
        img = md.resize_to_fit(img, 40, 40)
        img = np.expand_dims(img, axis=2)
        img = np.expand_dims(img, axis=0)

        pred = model.predict(img)
        letter = lb.inverse_transform(pred)[0]
        lables.append(map[letter])

    # 图片验证码
    captcha = "".join(lables)

    return captcha






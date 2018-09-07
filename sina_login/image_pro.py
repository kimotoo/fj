#encoding:utf-8
import cv2
import numpy as np
from keras.models import load_model
from imutils import paths
import imutils
import md
import pickle


# 对图像进行预处理

def img_pro(image):

    w,h = image.shape[:2]

    x = int(w / 2)
    y = int(h / 2)
    re=0
    while (True):
        px = image[x + 1][y]
        if (px[0] < px[2]):
            re = 150
            break
        elif (px[0] > px[2]):
            re = 120
            break
        else:
            y += 1

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = md.drop(image, re)
    image = md.dr(image)
    image_T = np.transpose(image)
    w0, w1 = md.edge(image)
    h0, h1 = md.edge(image_T)
    image = image[w0:w1, h0:h1]

    img = md.m(image)
    imgs = md.cut(img, image)

    return imgs






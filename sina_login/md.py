#encoding:utf-8

import cv2
import numpy as np
import imutils

# 去边界
def edge(image):

    w, h = image.shape[0], image.shape[1]
    x0 = 0
    x1 = w

    for i in range(w):
        sum_1 = sum_2 = 0
        for j in range(h):
            if image[i][j] != 255:
                sum_1 += 1
            if image[w-i-1][j] != 255:
                sum_2 += 1
        if sum_1 < 3:
            x0 = i
        if sum_2 < 3:
            x1 = w-i-1
        if (sum_1 > 3 and sum_2 > 3):
            break

    if x0 != 0:
        x0 += 1
    if x1 == h-1:
        x1 += 1

    return x0,x1


# 去干扰线
def drop(image,re):
    w, h = image.shape[0], image.shape[1]

    for i in range(w):
        for j in range(h):
            if (image[i][j] > re and image[i][j] != 255):
                image[i][j] = 0
    im = image.copy()
    i = j = 0

    for i in range(1, w - 1):
        for j in range(1, h - 1):
            if (image[i][j] != 0):
                a = image[i - 1][j]
                b = image[i][j - 1]
                c = image[i + 1][j]
                d = image[i][j + 1]
                sum = (a != 0 and b != 0 and c != 0 and d != 0)
                sum_1 = (a == 255 or b == 255 or c == 255 or d == 255)
                if sum and sum_1:
                    im[i][j] = 255


    ret, thresh = cv2.threshold(im, 200, 255, cv2.THRESH_BINARY)

    return thresh


# 去零散噪点
def dr(image):

    w,h = w, h = image.shape[0], image.shape[1]
    for i in range(1, w-1):
        for j in range(1, h-1):
            a = (image[i - 1][j] == 255)
            b = (image[i][j - 1] == 255)
            c = (image[i + 1][j] == 255)
            d = (image[i][j + 1] == 255)
            if (a and b and c and d):
                image[i][j] = 255
    return image


# 填充
def m(image):

    w, h = image.shape[0], image.shape[1]
    im = image.copy()

    for i in range(h):
        for j in range(w):
            if (image[j][i] != 0):
                im[j][i] = 0
            else:
                break
    i = j = 0

    for i in range(h):
        for j in range(w):
            if (image[w-j-1][i] != 0):
                im[w-j-1][i] = 0
            else:
                break

    i = j = 0

    for i in range(w):
        for j in range(h):
            if (image[i][j] != 0):
                im[i][j] = 0
            else:
                break

    i = j = 0

    for i in range(w):
        for j in range(h):
            if (image[i][h-j-1] != 0):
                im[i][h-j-1] = 0
            else:
                break

    return im


#投影法求分割点
def count(image):
    w, h = image.shape[0], image.shape[1]
    cou = 0
    for i in range(w):
        for j in range(h):
            if image[i][j] == 0:
                cou += 1
    return cou


def cut(image,im):
    w, h = image.shape[0], image.shape[1]
    array = []
    l = []
    cut = []

    for i in range(h):
        sum = 0
        for j in range(w):
            if image[j][i] == 255:
                sum += 1
        array.append(sum)
        if (sum == 0):
            cut.append(i)
    _cut = []
    sum = 0

    for k in range(len(cut) - 1):
        if (cut[k + 1] - cut[k] < 10):
            sum += 1
        else:
            _cut.append(cut[k] - sum + int(sum / 2))
            sum = 0

    if (_cut[0] == 0):
        _cut[0] = 1

    _cut.append(h - 1)
    imgs = []

    for n in range(len(_cut) - 1):
        ima = im[:, _cut[n] - 1:_cut[n + 1] + 1]
        imgs.append(ima)


    x = len(imgs)
    if x == 4:
        max = 0
        num = 0
        for y in range(4):
            cou = count(imgs[y])
            if (cou > max):
                max = cou
                num = y
        img = imgs[num]
        imgs.insert(num+1, img[:, 0 : int(img.shape[1] / 2) + 1])
        imgs.insert(num+2, img[:, int(img.shape[1] / 2) + 1:img.shape[1]])
        imgs.pop(num)
        return imgs

    elif x == 5:
        return imgs

    else :
        return []

def resize_to_fit(image, width, height):

    (h, w) = image.shape[:2]

    if w > h:
        image = imutils.resize(image, width=width)

    # otherwise, the height is greater than the width so resize
    # along the height
    else:
        image = imutils.resize(image, height=height)


    # determine the padding values for the width and height to
    # obtain the target dimensions
    padW = int((width - image.shape[1]) / 2.0)
    padH = int((height - image.shape[0]) / 2.0)

    # pad the image then apply one more resizing to handle any
    # rounding issues
    image = cv2.copyMakeBorder(image, padH, padH, padW, padW,
        cv2.BORDER_CONSTANT,value=255)
    image = cv2.resize(image, (width, height))

    # return the pre-processed image
    return image
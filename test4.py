import cv2
import numpy as np


def get_histogram_array(arr, max_num):
    hist = np.zeros(max_num + 1, dtype=np.int32)

    for i in range(max_num + 1):
        hist[i] = arr[arr == i].shape[0]

    return hist


for i in range(10):
    img = cv2.imread("resources/room ({}).png".format(i+1))
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h, s, v = cv2.split(hsv_img)
    h_raveled = h.ravel()
    s_raveled = s.ravel()
    v_raveled = v.ravel()

    h_hist = get_histogram_array(h_raveled, 180)
    s_hist = get_histogram_array(s_raveled, 255)
    v_hist = get_histogram_array(v_raveled, 255)

    # 一番多い色相に近しい色を探す (HSVマスク)
    h_max = np.argmax(h_hist)
    s_max = np.argmax(s_hist)
    v_max = np.argmax(v_hist)

    print("{}.png, h={}, s={}, v={}".format(i+1, h_max, s_max, v_max))

    range_min = np.array([
        h_max - 30 if h_max - 30 >= 0 else 0,
        0,
        0
    ])
    range_max = np.array([
        h_max + 30 if h_max + 30 <= 180 else 0,
        255,
        255
    ])

    masked = cv2.inRange(hsv_img, range_min, range_max)

    # copy the original image
    masked_img = img.copy()
    masked_img[masked == 0] = [0, 0, 0]

    hsv_img = cv2.cvtColor(masked_img, cv2.COLOR_BGR2HSV)

    h, s, v = cv2.split(hsv_img)
    s_raveled = s.ravel()
    s_hist = get_histogram_array(s_raveled, 255)

    s_hist_sorted = s_hist.argsort()[::-1]

    # 二番目に多い色相に近しい色を探す (HSVマスク)
    s_max = 0
    if s_hist_sorted[0] == 0:
        s_max = s_hist_sorted[1]
    else:
        s_max = s_hist_sorted[0]

    print("{}.png, s={}".format(i+1, s_max))

    range_min = np.array([
        h_max - 30 if h_max - 30 >= 0 else 0,
        s_max - 30 if s_max - 30 >= 0 else 0,
        0
    ])
    range_max = np.array([
        h_max + 30 if h_max + 30 <= 180 else 0,
        s_max + 30 if s_max + 30 <= 255 else 0,
        255
    ])

    masked = cv2.inRange(hsv_img, range_min, range_max)

    # マスクした領域を青で塗りつぶす
    img[masked > 0] = [255, 0, 0]

    cv2.imwrite("results/D_{}.png".format(i+1), img)
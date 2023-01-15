import cv2
import numpy as np

for i in range(10):
    img = cv2.imread("resources/room ({}).png".format(i+1))
    ksize = 51
    blur = cv2.blur(img, (ksize, ksize))

    rij = img/blur
    index_1 = np.where(rij >= 1.00)  # 1以上の値があると邪魔なため
    rij[index_1] = 1
    rij_int = np.array(rij*255, np.uint8)  # 除算結果が実数値になるため整数に変換
    rij_HSV = cv2.cvtColor(rij_int, cv2.COLOR_BGR2HSV)
    ret, thresh = cv2.threshold(rij_HSV[:, :, 2], 0, 255, cv2.THRESH_OTSU)
    rij_HSV[:, :, 2] = thresh
    rij_ret = cv2.cvtColor(rij_HSV, cv2.COLOR_HSV2BGR)
    cv2.imwrite("results/{}.png".format(i+1), rij_ret)

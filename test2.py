import cv2
import numpy as np

for i in range(10):
    img = cv2.imread("results/{}.png".format(i+1))
    # グレースケールに変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 平滑化 (ガウシアンフィルタを適応)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # エッジを検出 (Canny法)
    edges = cv2.Canny(blurred, 50, 150)

    # エッジを輪郭として抽出
    contours, hierarchy = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # エッジが大きい順にソート
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # 輪郭を様々な色で塗りつぶす
    # 一番大きい輪郭: 赤
    # 2番目に大きい輪郭: 青
    # 3番目に大きい輪郭: 緑
    # それ以外: 黒
    for j, cnt in enumerate(contours):
        if j == 0:
            color = (0, 0, 255)
        elif j == 1:
            color = (255, 0, 0)
        elif j == 2:
            color = (0, 255, 0)
        else:
            color = (0, 0, 0)
        cv2.drawContours(img, [cnt], -1, color, -1)

    cv2.imwrite("results/B_{}.png".format(i+1), img)

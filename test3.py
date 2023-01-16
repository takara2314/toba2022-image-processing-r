import cv2
import numpy as np

for i in range(10):
    img = cv2.imread("resources/room ({}).png".format(i+1))

    # グレースケールに変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 平滑化 (ガウシアンフィルタを適応)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # エッジを検出 (Canny法)
    edges = cv2.Canny(blurred, 50, 150)

    # エッジを輪郭として抽出
    contours, hierarchy = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 検出したエッジを描画
    img = cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

    cv2.imwrite("results/C_{}.png".format(i+1), img)
